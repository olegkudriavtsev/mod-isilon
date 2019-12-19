using System;
using System.Diagnostics;
using System.IO;
using System.Reflection;
using System.Threading.Tasks;
using Faction.Grpc.Core.v1;
using Faction.Isilon.Client.v1;
using Grpc.Health.V1;
using Microsoft.Extensions.Configuration;
using NUnit.Framework;
using Server;
using static Grpc.Health.V1.HealthCheckResponse.Types.ServingStatus;

namespace Faction.Isilon.EndToEndSpecs.v1
{
    [TestFixture]    
    public class IsilonClientEndToEndSpecs
    {
        private static readonly string AspNetCorePrefix = "ASPNETCORE_";
        private static readonly string AspNetCoreEnvVarKey = "ASPNETCORE_ENVIRONMENT";
        private static readonly string AppsettingBase = "appsettings.json";
        private static readonly string AppsettingEnv = "appsettings.{0}.json";
        private static readonly string DefaultCredentialId = "isilonDev";

        private IIsilonClient _client;

        [OneTimeSetUp]
        public async Task OneTimeSetUp()
        {
            runGrpcServer();
            
            var environment = Environment.GetEnvironmentVariable(AspNetCoreEnvVarKey);
            var configuration = new ConfigurationBuilder()
                .AddEnvironmentVariables(AspNetCorePrefix)
                .AddJsonFile(AppsettingBase)
                .AddJsonFile(string.Format(AppsettingEnv, environment), true)
                .Build();

            var hostConfiguration = new GrpcHostConfiguration<IIsilonClient>();
            configuration.Bind(hostConfiguration);
            _client = new IsilonClient(hostConfiguration);
        }

        private static void runGrpcServer()
        {
            var directoryName = Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location);
            var directoryInfo = new DirectoryInfo(directoryName);
            var parent = directoryInfo.Parent.Parent.Parent.Parent.Parent;
            var directoryInfos = parent.GetDirectories("server");
            var path = directoryInfos[0];
            var pathToPy = $"{path.FullName}/main.py";
            LocalProcessStartHelper.run_cmd_in_shell("/usr/local/bin/python3.7", pathToPy, "-v");
        }

        [Test]
        public async Task ShouldReturnInfo()
        {
            var info = await _client.InfoAsync(new InfoRequest
            {
                CredentialsId = DefaultCredentialId
            });

            Assert.That(info, Is.Not.Null);
        }
        
        [Test]
        public async Task ShouldReturnHealthStatus()
        {
            var health = await _client.HealthAsync(new HealthCheckRequest
            {
                Service = "Isilon"
            });


            Assert.That(health.Status, Is.EqualTo(Serving));
        }
    }
}
