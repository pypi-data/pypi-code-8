from . import commands


def process_cmds(args):
    if args.cmd == 'login':
        commands.login(args.username, args.password, args.cloud, args.endpoint)
    elif args.cmd == 'logout':
        commands.logout()
    elif args.cmd == 'service':
        if args.subcmd == 'create':
            commands.service_create(image=args.image, name=args.name, do_not_start=args.do_not_start, target_num_instances=args.target_num_instances,
                                    instance_size=args.instance_size, run_command=args.run_command, env=args.env, ports=args.expose)
        elif args.subcmd == 'update':
            commands.service_update(args.name, target_num_instances=args.target_num_instances)
        elif args.subcmd == 'get':
            commands.service_get(args.name)
        elif args.subcmd == 'start':
            commands.service_start(args.name)
        elif args.subcmd == 'stop':
            commands.service_stop(args.name)
        elif args.subcmd == 'delete':
            commands.service_delete(args.name)
        elif args.subcmd == 'list':
            commands.service_list()
