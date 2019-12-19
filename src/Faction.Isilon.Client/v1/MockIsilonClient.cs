using System.Threading.Tasks;
using Faction.Grpc.Core.v1;
using Grpc.Core;
using Grpc.Health.V1;
using Server;

namespace Faction.Isilon.Client.v1
{
    public class MockIsilonClient : IIsilonClient
    {
        public Task<InfoResponse> InfoAsync(InfoRequest request)
        {
            return Task.FromResult(new InfoResponse
            {
                Message = "result"
            });
        }

        public Task<HealthCheckResponse> HealthAsync(HealthCheckRequest request)
        {
            return Task.FromResult(new HealthCheckResponse
            {
                Status = HealthCheckResponse.Types.ServingStatus.Serving
            });
        }
    }
}
