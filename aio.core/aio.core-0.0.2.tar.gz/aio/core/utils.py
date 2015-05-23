import asyncio


@asyncio.coroutine
def exit_on_error(task, on_error=None):
    loop = asyncio.get_event_loop()
    try:
        yield from task
    except:
        if on_error:
            on_error()
        loop.stop()
