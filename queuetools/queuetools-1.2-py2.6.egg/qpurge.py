import getpass
import optparse
import functional
import sys
from queuetools.options import add_connection_options
from amqplib import client_0_8 as amqp

def purge_options(args):
    options = optparse.OptionParser(
        prog="qpurge",
        usage="%prog -Q QUEUE",
        description="Purges messages from an AMQP queue."
    )
    options.add_option("-Q", "--queue",
                       action="store",
                       help="the queue to purge")
    add_connection_options(options)
    return options.parse_args(args)


def main(
    args=sys.argv[1:],
    optparse=purge_options,
    getpassword=getpass.getpass,
    connect=amqp.Connection
):
    options, args = optparse(args)
    if options.password is None:
        options.password = getpassword()

    con = connect(
        host=options.host,
        userid=options.userid,
        password=options.password,
        virtual_host=options.vhost
    )
    try:
        chan = con.channel()
        try:
            purged_count = chan.queue_purge(
                queue=options.queue
            )
            print "Successfully purged %d messages!" % purged_count
        finally:
            chan.close()
    finally:
        con.close()
