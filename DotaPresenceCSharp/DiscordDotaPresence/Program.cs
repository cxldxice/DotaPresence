using DiscordRPC.Logging;
using DotaHandler;

namespace DiscordDotaPresence
{
    static class Program
    {
        private static readonly ILogger Logger = new ConsoleLogger();
        
        static void Main()
        {
            // Discord presence init
            var presence = new PresenceUpdater("868402263314563073", Logger);
            presence.Initialize();
            
            // Dota http listener init
            var listener = new DotaListener("http://localhost:6768/");
            
            // Subscribe on request event
            listener.OnRequestProcessed += presence.SetDotaPresenceListener;
            
            listener.Start();
        }
    }
}
