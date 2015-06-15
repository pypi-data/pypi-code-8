import mythicals


def parsers(commands, parents):
    parser = commands.add_parser(
        'shell',
        parents=parents,
        description='interactive shell',
    )
    parser.add_argument(
        'type',
        nargs='?',
        default='auto',
        choices=['auto', 'native', 'ipython'],
        metavar='TYPE',
    )
    parser.add_argument(
        '-d', '--domain', action='store_true', default=False,
    )
    parser.set_defaults(command=command)


def command(args):
    namespace = {}
    namespace.update(dict(
        (attr, getattr(mythicals, attr)) for attr in mythicals.__all__
    ))
    if args.domain:
        namespace.update(
            (attr, getattr(mythicals.domain, attr))
            for attr in mythicals.domain.__all__
        )
    if args.type == 'native':
        return native(namespace)
    elif args.type == 'ipython':
        return ipython(namespace)
    elif args.type == 'auto':
        try:
            return ipython(namespace)
        except ImportError:
            return native(namespace)


def native(namespace):
    # http://stackoverflow.com/a/5597918
    try:
        import readline
    except ImportError:
        pass
    import code
    shell = code.InteractiveConsole(namespace)
    return shell.interact()


def ipython(namespace):

    def embed_13():
        from IPython import embed
        return embed(user_ns=namespace)

    def embed_11():
        from IPython.terminal.embed import InteractiveShellEmbed
        return InteractiveShellEmbed(user_ns=namespace)()

    def embed_0():
        from IPython.Shell import IPShellEmbed
        return IPShellEmbed(user_ns=namespace)()

    embeds = [embed_13, embed_11, embed_0]
    while True:
        embed = embeds.pop()
        try:
            return embed()
        except Exception:
            if  embeds:
                continue
            raise
