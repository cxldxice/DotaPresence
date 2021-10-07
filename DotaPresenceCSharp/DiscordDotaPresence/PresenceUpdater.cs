using System;
using System.IO;
using DiscordRPC;
using DiscordRPC.Logging;
using Newtonsoft.Json.Linq;

namespace DiscordDotaPresence
{
    public sealed class PresenceUpdater
    {
        private readonly string _appId;

        private readonly JObject _heroesDict =
            JObject.Parse(File.ReadAllText(
                "./Resources/heroes_names.json"));

        private readonly ILogger _logger;
        private DiscordRpcClient _client;


        public PresenceUpdater(string appId, ILogger logger)
        {
            _appId = appId;
            _logger = logger;
        }

        public void Initialize()
        {
            _client = new DiscordRpcClient(_appId, pipe: 0)
            {
                Logger = _logger
            };

            _client.Initialize();
        }

        public void SetDotaPresenceListener(JObject data)
        {
            if (_client == null || _client.IsDisposed)
            {
                _logger.Warning("Not Initialized!");
                return;
            }

            if (data["hero"]?.ToString() == null)
            {
                _client.SetPresence(new RichPresence
                {
                    Assets = new Assets
                    {
                        LargeImageKey = "logo",
                        LargeImageText = "Dota 2",
                    },
                    Details = "Main menu",
                    Timestamps =
                        new Timestamps(
                            new DateTime(1970, 1, 1).AddMilliseconds(
                                Int64.Parse(data["start"]?.ToString() ?? string.Empty)))
                });

                return;
            }

            var currentHeroName = _heroesDict[data["hero"]["name"]?.ToString() ?? "Unknown Hero"];
            var mapName = data["map"]["name"]?.ToString();
            string currentGameMap;

            switch (mapName)
            {
                case "hero_demo_main":
                    currentGameMap = "Testing hero " + currentHeroName;
                    break;
                case "start":
                    currentGameMap = "Playing game for " + currentHeroName;
                    break;
                default:
                    currentGameMap = mapName;
                    break;
            }

            // ReSharper disable once PossibleLossOfFraction
            var time = DateTime.UtcNow.AddSeconds(-Int32.Parse(data["map"]["game_time"]?.ToString() ?? string.Empty));

            _client.SetPresence(new RichPresence
            {
                Assets = new Assets
                {
                    LargeImageKey = data["hero"]["name"]?.ToString(),
                    LargeImageText = currentHeroName?.ToString(),
                    SmallImageKey = data["hero"]["level"]?.ToString(),
                    SmallImageText = "Level " + data["hero"]["level"],
                },

                State = data["player"]["kills"] + "/" + data["player"]["deaths"] + "/" + data["player"]["assists"] +
                        "; GPM/XPM: " + data["player"]["gpm"] + "/" + data["player"]["xpm"],
                Details = "Now: " + currentGameMap,
                Timestamps = new Timestamps(time),

                // Buttons = new Button[]
                // {
                //     new Button { Label = "", Url = "" }
                // }
            });
        }

        public void Stop()
        {
            _client.Dispose();
        }
    }
}