using System.Threading.Tasks;
using Faction.Grpc.Core.v1;
using Grpc.Core;
using Grpc.Health.V1;
using Server;

namespace Faction.Isilon.Client.v1
{
    public class IsilonClient : Client, IIsilonClient
    {
        private readonly GrpcHostConfiguration<IIsilonClient> _configuration;

        private Channel _channel;

        public IsilonClient(GrpcHostConfiguration<IIsilonClient> configuration)
        {
            _configuration = configuration;
        }

        public async Task<InfoResponse> InfoAsync(InfoRequest request)
        {
            return await ExecuteWithInternalClientAsync(async isilonClient => await isilonClient.InfoAsync(request), GetInternalClient);
        }

        public async Task<HealthCheckResponse> HealthAsync(HealthCheckRequest request)
        {
            return await ExecuteWithInternalClientAsync(async healthClient => await healthClient.CheckAsync(request), GetHealthClient);
        }

        protected virtual Server.Isilon.IsilonClient GetInternalClient()
        {
            ConnectWithChannel();
            return new Server.Isilon.IsilonClient(_channel);
        }

        protected virtual Health.HealthClient GetHealthClient()
        {
            ConnectWithChannel();
            return new Health.HealthClient(_channel);
        }

        private void ConnectWithChannel()
        {
            if (_channel == null || _channel.State == ChannelState.Shutdown)
            {
                _channel = new Channel(_configuration.Host, _configuration.Port, ChannelCredentials.Insecure);
            }
        }
    }
}
