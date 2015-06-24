from django.utils.text import slugify


def create_path(menu):
    roots = ['/', menu.title]

    while True:
        menu = menu.parent
        if not menu:
            break

        roots.append(menu.title)
    roots.append('/')

    return '/'.join(slugify(_) for _ in roots[::-1])
