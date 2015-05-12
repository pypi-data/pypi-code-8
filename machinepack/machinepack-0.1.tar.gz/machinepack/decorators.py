# -*- coding: utf-8 -*-

import sys
from functools import wraps


def machinepack_required(func):
    @wraps(func)
    def wrapper(ctx, *args, **kwargs):

        if not ctx.machinepack_viewer.initialization:
            ctx.echo.error('Invalid machinepack folder!')
            sys.exit(1)

        return func(ctx, *args, **kwargs)

    return wrapper


# def check_folder():
#     def wrapper(ctx):
#         if ctx.machinepack_viewer.initialization:
#             ctx.echo.error('You are in other machinepack folder!')
#             sys.exit(1)
#     return wrapper
