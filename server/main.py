import logging
import os
from concurrent import futures

import grpc
from grpc_health.v1 import health
from grpc_health.v1 import health_pb2
from grpc_health.v1 import health_pb2_grpc
import isilon_pb2
import isilon_pb2_grpc
from service import isilon_service

HOST = os.getenv('HOST', 'localhost')
PORT = os.getenv('PORT', 50053)
HTTP2_ADDRESS = '[::]:%i' % PORT


def serve(args):
    if args.help:
        print_help()
        return
    if is_port_in_use():
        raise SystemError('Port {port} is already in use'.format(port=repr(int(PORT))))
    health_service, server = init_server(args)
    acknowledge_health(health_service)
    server.start()
    server.wait_for_termination()
    if args.verbose:
        print("Isilon server started on port %s" % PORT)


def init_server(args):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    health_service = health.HealthServicer(experimental_non_blocking=False, experimental_thread_pool=None)
    health_pb2_grpc.add_HealthServicer_to_server(health_service, server)
    isilon_pb2_grpc.add_IsilonServicer_to_server(isilon_service.IsilonService(), server)
    if args.reflection:
        enable_server_reflection(args, server)
    server.add_insecure_port(HTTP2_ADDRESS)
    return health_service, server


class Arguments:
    verbose = False
    reflection = False
    help = False


def get_arguments():
    import sys, getopt
    args = Arguments()

    unix_options = "hrv"
    gnu_options = ["help", "reflection", "verbose"]
    try:
        arguments, values = getopt.getopt(sys.argv[1:], unix_options, gnu_options)
    except getopt.error as err:
        # output error, and return with an error code
        print("Error parsing arguments list %s" % str(err))
        sys.exit(2)
    for current_argument, current_value in arguments:
        if current_argument in ("-v", "--verbose"):
            print("Verbose mode enabled")
            args.verbose = True
        elif current_argument in ("-h", "--help"):
            print("Help will be printed")
            args.help = True
        elif current_argument in ("-r", "--enable_reflection"):
            print("Server reflection will be enabled")
            args.reflection = True
    return args


def enable_server_reflection(args, server):
    from grpc_reflection.v1alpha import reflection
    service_names = (
        isilon_pb2.DESCRIPTOR.services_by_name[isilon_pb2._ISILON.name].full_name, reflection.SERVICE_NAME,
        health_pb2.DESCRIPTOR.services_by_name[health_pb2._HEALTH.name].full_name, reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(service_names, server)
    if args.verbose:
        print("Server reflection enabled for:")
        for service_name in service_names:
            if service_name != reflection.SERVICE_NAME: print(service_name)


def print_help():
    print('Mod-isilon grpc server that connects to Isilon Instance using specified credentials')
    print('To use verbose pass -v or --verbose argument')
    print('To use server reflection use -r or --enable_reflection argument')
    print('Use -h to see this help text')


def is_port_in_use():
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((HOST, PORT)) == 0


def acknowledge_health(health_service):
    health_service.set('', health_pb2.HealthCheckResponse.SERVING)
    health_service.set(isilon_pb2._ISILON.name, health_pb2.HealthCheckResponse.SERVING)


if __name__ == '__main__':
    logging.basicConfig()
    serve(get_arguments())
