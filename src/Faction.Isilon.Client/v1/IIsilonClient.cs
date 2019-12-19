using System.Threading.Tasks;
using Grpc.Health.V1;
using Server;

namespace Faction.Isilon.Client.v1
{
    public interface IIsilonClient
    {
        Task<InfoResponse> InfoAsync(InfoRequest request);

        Task<HealthCheckResponse> HealthAsync(HealthCheckRequest request);
    }
}
