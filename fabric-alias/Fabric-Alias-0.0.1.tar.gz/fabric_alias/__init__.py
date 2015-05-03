

def set_alias(modules={}, seen_clear=False):
    from fabric.main import load_tasks_from_module, is_task_module, _seen
    from fabric import state
    import os
    dirname, _ = os.path.split(__file__)

    c = {}
    for import_name, module in modules.items():
        if is_task_module(module):
            docs, newstyle, classic, defaul = load_tasks_from_module(module)
            c[import_name] = newstyle

    state.commands.update(c)

    if seen_clear:
        _seen.clear()
