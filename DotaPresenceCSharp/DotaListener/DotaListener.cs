using System;
using System.IO;
using System.Net;
using Newtonsoft.Json.Linq;

namespace DotaListener
{
    public static class DotaListener
    {
        public delegate void ProcessHandler(HttpListenerContext context);

        public static event ProcessHandler onRequest = ProcessRequest;
        
        public static void Start()
        {
            var listener = new HttpListener();
            listener.Prefixes.Add("http://localhost:6768/");

            listener.Start();

            while (listener.IsListening)
            {
                Console.WriteLine("Recived");
                var context = listener.GetContext();
                ProcessRequest(context);
            }
            
            listener.Close();
        }

        private static void ProcessRequest(HttpListenerContext context)
        {
            // Get the data from the HTTP stream
            var res = JObject.Parse(new StreamReader(context.Request.InputStream).ReadToEnd());

            Console.WriteLine(res);
            Console.WriteLine(res["provider"]);
        }
    }
}