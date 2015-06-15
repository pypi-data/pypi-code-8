from django.core.exceptions import ValidationError


def validate_mp3_extension(value):
    if not value.name.endswith('.mp3'):
        raise ValidationError('Only able to upload mp3 file')
