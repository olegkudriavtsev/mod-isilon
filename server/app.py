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


def start_app():
    args = _get_arguments()

    if args.help:
        _print_help()
        return

    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARN)

    if _is_port_in_use():
        raise SystemError('Port {port} is already in use'.format(port=repr(int(PORT))))

    health_service, server = _init_server(args)
    _acknowledge_health(health_service)
    server.start()
    if args.verbose:
        logging.info("Isilon server started on port %s", PORT)
    server.wait_for_termination()


def _init_server(args):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    health_service = health.HealthServicer(experimental_non_blocking=False, experimental_thread_pool=None)
    health_pb2_grpc.add_HealthServicer_to_server(health_service, server)
    isilon_pb2_grpc.add_IsilonServicer_to_server(isilon_service.IsilonService(), server)
    if args.reflection:
        _enable_server_reflection(args, server)
    server.add_insecure_port(HTTP2_ADDRESS)
    return health_service, server


class _Arguments:
    verbose = False
    reflection = False
    help = False


def _get_arguments():
    import sys, getopt
    args = _Arguments()

    unix_options = "hrv"
    gnu_options = ["help", "reflection", "verbose"]
    try:
        arguments, values = getopt.getopt(sys.argv[1:], unix_options, gnu_options)
    except getopt.error as err:
        logging.error("Error parsing arguments list %s" % str(err))
        sys.exit(2)
    for current_argument, current_value in arguments:
        if current_argument in ("-v", "--verbose"):
            args.verbose = True
        elif current_argument in ("-h", "--help"):
            args.help = True
        elif current_argument in ("-r", "--enable_reflection"):
            args.reflection = True
    return args


def _enable_server_reflection(args, server):
    from grpc_reflection.v1alpha import reflection
    service_names = (
        isilon_pb2.DESCRIPTOR.services_by_name[isilon_pb2._ISILON.name].full_name, reflection.SERVICE_NAME,
        health_pb2.DESCRIPTOR.services_by_name[health_pb2._HEALTH.name].full_name, reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(service_names, server)
    if args.verbose:
        logging.info("Server reflection enabled for:")
        for service_name in service_names:
            if service_name != reflection.SERVICE_NAME: logging.info(service_name)


def _print_help():
    print('Mod-isilon grpc server that connects to Isilon Instance using specified credentials')
    print('To use verbose pass -v or --verbose argument')
    print('To use server reflection use -r or --enable_reflection argument')
    print('Use -h to see this help text')


def _is_port_in_use():
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((HOST, PORT)) == 0


def _acknowledge_health(health_service):
    health_service.set('', health_pb2.HealthCheckResponse.SERVING)
    health_service.set(isilon_pb2._ISILON.name, health_pb2.HealthCheckResponse.SERVING)
