"""Functions, which generates HTML code for Web page."""


def generate_action_buttons_html(object_id, name, description, modal_id,
                                 delete_function_name):
    """Generates HTML for action buttons.

    Action button - 'Edit' and 'Delete' used in
    pictures' management tab and albums' management tab
    in administrator's panel.
    """
    edit_button = '<button {}>Edit</button>'.format(
        'type="button" ' +
        'class="btn-xs btn-default" ' +
        'data-toggle="modal" ' +
        'data-target="#' + modal_id + '" ' +
        'data-id="' + str(object_id) + '" ' +
        'data-name="' + str(name) + '" ' +
        'data-description="' + str(description) + '" ')
    delete_button = '<button {}>Delete</button>'.format(
        'class="btn-xs btn-danger" ' +
        'onclick="' + delete_function_name + '(' + str(object_id) + ')"')
    return '<div class="container-fluid">' + \
           '<div class="btn-toolbar" role="toolbar">' + \
           '<div class="btn-group" role="group">' + \
           edit_button + \
           '</div>' + \
           '<div class="btn-group" role="group">' + \
           delete_button + \
           '</div>' + \
           '</div>' + \
           '</div>'


def generate_thumbnail_html(path_to_thumbnail):
    """Generates HTML code for image thumbnail."""
    return '<img src="{}">'.format(
        path_to_thumbnail
    )
