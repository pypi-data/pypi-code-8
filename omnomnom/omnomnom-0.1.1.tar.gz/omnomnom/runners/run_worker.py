import signal
import argparse

from omnomnom import utils
from omnomnom.generics.taskqueue import LycheeWorker


parser = argparse.ArgumentParser(description='Omnomnom Worker Runner')

parser.add_argument(
    '--address', dest='address', type=str,
    help='Socket to connect to', default='tcp://127.0.0.1:7105'
)
parser.add_argument(
    '--name', dest='name', type=str,
    help='Worker name'
)
parser.add_argument(
    '--log-level', dest='log_level', type=str,
    default='INFO'
)
parser.add_argument(
    '--standalone', dest='standalone', action='store_true',
    help='Enables to run worker in standalone mode (without queue as a proxy)'
)
parser.add_argument(
    '--max-workers', dest='max_workers', type=int,
    help='Number of workers to define when runnning in standalone mode',
    default=4
)


def shutdown(worker_instance):
    worker_instance.stop()


def get_options():
    arguments = parser.parse_args()
    return arguments


def main():
    args = get_options()
    utils.setup_loghandlers(args.log_level)

    worker = LycheeWorker(
        address=args.address, name=args.name,
        standalone=args.standalone, max_workers=args.max_workers
    )

    shutdown_handler = lambda sig, frame: shutdown(worker)
    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)

    worker.start()