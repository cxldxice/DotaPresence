using System;
using System.IO;
using System.Net;
using Newtonsoft.Json.Linq;

namespace DotaListener
{
    public class DotaServerListener
    {
        public DotaServerListener()
        {
            
        }
        
        public void Start()
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

        private void ProcessRequest(HttpListenerContext context)
        {
            // Get the data from the HTTP stream
            // onRequest?.Invoke(JObject.Parse(new StreamReader(context.Request.InputStream).ReadToEnd()));
        }
    }
}