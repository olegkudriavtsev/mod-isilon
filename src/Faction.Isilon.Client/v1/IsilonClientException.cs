using System;

namespace Faction.Isilon.Client.v1
{
    public class IsilonClientException : Exception
    {
        public IsilonClientException(Exception exception)
            : base("Exception during accessing isilon grpc server", exception)
        {
        }
    }
}