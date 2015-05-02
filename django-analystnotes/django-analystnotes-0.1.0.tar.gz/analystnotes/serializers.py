from rest_framework import serializers
from models import Project, Command
from validators import validate_project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        exclude = ('owner', )
        # fields = ('name', 'id')


class CommandSerializer(serializers.ModelSerializer):
    validate = validate_project

    class Meta:
        model = Command



