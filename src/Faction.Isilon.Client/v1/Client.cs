using System;
using System.Threading.Tasks;

namespace Faction.Isilon.Client.v1
{
    public abstract class Client
    {
        protected async Task<TResult> ExecuteWithInternalClientAsync<TResult, TClient>(
            Func<TClient, Task<TResult>> method,
            Func<TClient> getClient)
        {
            var client = getClient();
            return await method(client);
        }
    }
}
