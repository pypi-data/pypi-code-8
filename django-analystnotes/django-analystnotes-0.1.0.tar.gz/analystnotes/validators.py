from rest_framework.exceptions import ValidationError


def validate_project(self, attrs):
    user = self.context['request'].user
    if user != attrs['project'].owner:
        raise ValidationError('Invalid Project ID')
    print user, attrs['project'].owner
    # if attrs['user'].id != user.id:
    #     raise ValidationError('Invalid Project ID')
    return attrs