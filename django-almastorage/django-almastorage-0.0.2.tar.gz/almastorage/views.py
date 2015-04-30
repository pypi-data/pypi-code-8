from django.shortcuts import render, render_to_response
from django.views.generic import ListView
from .models import SwiftFile, SwiftContainer
from .forms import UploadFileForm
from django.http import HttpResponseRedirect
from .models import *
import swiftclient
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper

class ContainerListView(ListView):
    model = SwiftContainer
    paginate_by = 10
    queryset = SwiftFile.objects.all()
    template_name='swift_file/templates/swift_file/swiftfile_list.html'
    context_object_name = 'container'

def upload_file(request):
    if request.method == 'GET':
        return render(request, 'swift_file/upload_form.html',{'form':UploadFileForm()})
    elif request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        conn = swiftclient.Connection(user=USER, key=KEY, authurl=AUTHURL)
        SwiftFile.upload_file(User.objects.first(), conn, request.FILES['file'].read(), request.FILES['file'].name, request.FILES['file'].content_type)
        if form.is_valid():
            return HttpResponseRedirect('/')
        pass

def download_file(request, file_id):
    if request.method == 'GET':
        base_file = SwiftFile.objects.get(id=file_id)
        filename = base_file.filename.split('.')[0]+'_'+base_file.date.time().__str__()+'.'+base_file.filename.split('.')[1]
        conn = swiftclient.Connection(user=USER, key=KEY, authurl=AUTHURL)
        obj_tuple = conn.get_object('images', filename)
        response = HttpResponse(obj_tuple[1], content_type=base_file.content_type)
        response['Content-Disposition'] = 'attachment; filename='+base_file.filename
        return response

