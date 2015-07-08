from helga import log, settings
from helga.plugins import command, preprocessor


USAGE = 'helga ignore (list|(add|remove) <nick>)'

# Set of ignored nicks
ignored = set()

logger = log.getLogger(__name__)


def ignore_preprocessor(channel, nick, message):
    global ignored

    if nick in ignored:
        logger.info('Ignored message from %s', nick)
        message = u''

    return channel, nick, message


def ignore_command(client, channel, nick, message, cmd, args):
    global ignored

    if args[0] == 'list':
        return 'Currently ignoring the following users: {0}'.format(', '.join(sorted(ignored)))
    elif args[0] == 'add':
        ignore_nick = args[1]

        if ignore_nick == client.nickname:
            return "I'm sorry {0}, but I can't ignore myself".format(nick)

        if ignore_nick == nick:
            return "I'm sorry {0}, but you can't ignore yourself".format(nick)

        if ignore_nick in settings.OPERATORS:
            return "I'm sorry {0}, but I can't ignore an operator".format(nick)

        if ignore_nick in ignored:
            return "I'm already ignoring {0}".format(ignore_nick)

        ignored.add(ignore_nick)
        logger.info('Added %s to ignore list', ignore_nick)
        return "Added {0} to the ignore list".format(ignore_nick)
    elif args[0] == 'remove':
        ignore_nick = args[1]

        ignored.discard(ignore_nick)
        logger.info('Removed %s from ignore list', ignore_nick)
        return "Removed {0} from the ignore list".format(ignore_nick)

    return 'Unrecognized ignore command: {0!r}. Usage: {1}'.format(args[0], USAGE)


@preprocessor
@command('ignore', help="Tell the bot to ignore some users. Usage: {0}".format(USAGE))
def ignore(client, channel, nick, message, *args):
    global ignored

    # Handle the message preprocesor
    if len(args) == 0:
        return ignore_preprocessor(channel, nick, message)
    elif len(args) == 2:
        return ignore_command(client, channel, nick, message, *args)
