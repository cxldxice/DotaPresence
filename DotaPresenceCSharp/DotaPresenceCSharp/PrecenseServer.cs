using DotaListener;
using Newtonsoft.Json.Linq;

namespace DotaPresenceCSharp
{
    public static class PrecenseServer
    {
        public delegate void ProcessHandler(JObject result);

        public static event ProcessHandler onRequest;
        
        static void Main()
        {
            // var server = new DotaServerListener(onRequest);
            // server.Start();
            
            
            
        }
    }
}