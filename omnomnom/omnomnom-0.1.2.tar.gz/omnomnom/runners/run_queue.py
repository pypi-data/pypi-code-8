import signal
import argparse

from omnomnom import utils
from omnomnom.generics import taskqueue


parser = argparse.ArgumentParser(description='Omnomnom Queue Runner')
parser.add_argument(
    '--frontend', dest='frontend', type=str,
    help='Frontend socket address', default='tcp://127.0.0.1:7104'
)
parser.add_argument(
    '--backend', dest='backend', type=str,
    help='Backend socket address', default='tcp://127.0.0.1:7105'
)
parser.add_argument(
    '--log-level', dest='log_level', type=str,
    default='INFO'
)


def shutdown(queue_instance):
    queue_instance.stop()


def get_options():
    arguments = parser.parse_args()
    return arguments


def main():
    args = get_options()
    utils.setup_loghandlers(args.log_level)

    queue = taskqueue.OmnomnomQueue(
        pull_address=args.frontend,
        push_address=args.backend
    )

    shutdown_handler = lambda sig, frame: shutdown(queue)
    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)

    queue.start()