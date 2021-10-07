using System;
using System.Diagnostics;
using System.IO;
using System.Net;
using Newtonsoft.Json.Linq;

namespace DotaHandler
{
    public class DotaListener
    {
        private readonly string _address;

        private DateTime _startTime;

        public delegate void ResponseArgs(JObject data);

        public event ResponseArgs OnRequestProcessed;

        public DotaListener(string address)
        {
            _address = address;
        }
        
        public void Start()
        {
            var listener = new HttpListener();
            listener.Prefixes.Add(_address);
            _startTime = DateTime.UtcNow;

            while (true)
            {
                Process[] pName = Process.GetProcessesByName("dota2");
                if (pName.Length != 0)
                {
                    listener.Start();
                    
                    while (listener.IsListening)
                    {
                        var context = listener.GetContext();
                        ProcessRequest(context);
                    }

                    listener.Close();
                }
                else
                {
                    // Sleep for 60 sec while waiting for the process
                    System.Threading.Thread.Sleep(60000);
                    _startTime = DateTime.UtcNow;
                }
            }
        }

        private void ProcessRequest(HttpListenerContext context)
        {
            // Get the data from the HTTP stream
            var data = JObject.Parse(new StreamReader(context.Request.InputStream).ReadToEnd());
            data["start"] = new DateTimeOffset(_startTime).ToUnixTimeMilliseconds();
            OnRequestProcessed?.Invoke(data);
        }
    }
}