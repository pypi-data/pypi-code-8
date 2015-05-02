from serializers import CommandSerializer, ProjectSerializer
from models import Project, Command
from rest_framework import viewsets, routers
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer, BrowsableAPIRenderer, JSONRenderer, HTMLFormRenderer
from permissions import ObjectOwnerPermission, ProjectOwnerPermission
from filters import ObjectOwnerFieldPermissionsFilter, ProjectOwnerFieldPermissionsFilter


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions, ObjectOwnerPermission)
    filter_backends = (ObjectOwnerFieldPermissionsFilter, )

    def perform_create(self, serializer):
        print "saving as %s" % self.request.user
        serializer.save(owner=self.request.user)


class CommandViewSet(viewsets.ModelViewSet):
    queryset = Command.objects.all()
    serializer_class = CommandSerializer
    permission_classes = (IsAuthenticated, DjangoModelPermissions, ProjectOwnerPermission)
    filter_backends = (ProjectOwnerFieldPermissionsFilter, )
    # TODO: Add html output as a renderer
    # renderer_classes = (BrowsableAPIRenderer, JSONRenderer, TemplateHTMLRenderer)
    # template_name = 'analystnotes/cmd.html'

    # def list(self, request, *args, **kwargs):
    #     if request.accepted_renderer.format == 'html':
    #         return Response('test.txt')

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'cmd', CommandViewSet)
router.register(r'project', ProjectViewSet)