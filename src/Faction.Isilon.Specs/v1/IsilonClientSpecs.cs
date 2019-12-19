using System;
using System.Threading.Tasks;
using Faction.Isilon.Client.v1;
using Grpc.Core;
using Moq;
using Moq.Protected;
using NUnit.CompareNetObjects;
using NUnit.Framework;
using Server;

namespace Faction.Isilon.Specs.v1
{
    [TestFixture]
    public class IsilonClientSpecs
    {
        private Mock<Server.Isilon.IsilonClient> _internalClientMock;
        private Mock<IsilonClient> _clientMock;

        private IIsilonClient Client => _clientMock.Object;

        private static readonly string ServiceUnavailableMessage = "Service unavailable";

        [SetUp]
        public void Setup()
        {
            _internalClientMock = new Mock<Server.Isilon.IsilonClient> { CallBase = true };
            _clientMock = new Mock<IsilonClient>(null) { CallBase = true };

            _clientMock.Protected()
                .Setup<Server.Isilon.IsilonClient>("GetInternalClient")
                .Returns(_internalClientMock.Object);
        }

        [Test]
        public async Task ShouldReturnResultWithoutIssuesOnSuccessInfoCall()
        {
            // Mock InfoAsync() method in the internal grpc client to return InfoResponse message.
            _internalClientMock
                .Setup(x => x.InfoAsync(It.IsAny<InfoRequest>(), It.IsAny<CallOptions>()))
                .Returns(CreateGrpcResponse(new InfoResponse(), Status.DefaultSuccess));

            var result = await Client.InfoAsync(new InfoRequest
            {
                CredentialsId = "TestCredentialsId"
            });

            _internalClientMock.Verify(x => x.InfoAsync(It.IsAny<InfoRequest>(), It.IsAny<CallOptions>()), Times.Once());
            Assert.IsNotNull(result);
        }

        [Test]
        public async Task ShouldRethrowException()
        {
            // Mock InfoAsync() method in the internal grpc client to throw an RPC exception.
            var rpcException = new RpcException(new Status(StatusCode.Unavailable, string.Empty), ServiceUnavailableMessage);
            _internalClientMock
                .Setup(x => x.InfoAsync(It.IsAny<InfoRequest>(), It.IsAny<CallOptions>()))
                .Throws(rpcException);

            Exception checkedException = null;
            try
            {
                await Client.InfoAsync(new InfoRequest
                {
                    CredentialsId = "TestCredentialsId",
                });
            }
            catch (Exception e)
            {
                checkedException = e;
            }

            Assert.That(checkedException, Is.Not.Null);
            Assert.That(checkedException, Is.TypeOf<IsilonClientException>());
            Assert.That(checkedException.Message, Is.EqualTo("Exception during accessing isilon grpc server"));
            _internalClientMock.Verify(x => x.InfoAsync(It.IsAny<InfoRequest>(), It.IsAny<CallOptions>()), Times.Once());
        }

        private AsyncUnaryCall<T> CreateGrpcResponse<T>(T response, Status status)
        {
            var metadata = new Metadata();

            return new AsyncUnaryCall<T>(
                Task.FromResult(response),
                Task.FromResult(metadata),
                () => status,
                () => metadata,
                () => {});
        }
    }
}
