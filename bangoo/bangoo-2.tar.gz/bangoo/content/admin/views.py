from .forms import EditContentForm
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render


@permission_required('content.add_content')
def edit_content(request, template_name='content/admin/edit_content.html'):
    form = EditContentForm(author=request.user)
    return render(request, template_name, {'form': form, 'menu': request.act_menu})
