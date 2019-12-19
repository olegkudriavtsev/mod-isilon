import isilon_pb2
import isilon_pb2_grpc


class IsilonService(isilon_pb2_grpc.IsilonServicer):
    """Provides methods that implement functionality of isilon server."""

    def Info(self, request, context):
        return isilon_pb2.InfoResponse(message='Isilon data tbd')
        # TODO: implement mod-secrets client and use request.CredentialsId to access isilon and retrieve data
