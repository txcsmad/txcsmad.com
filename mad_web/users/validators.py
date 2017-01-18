import os
from django.template.defaultfilters import filesizeformat
from django.core.exceptions import ValidationError

def validate_file_extension(value):    
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension. Only %s file types are supported'  % (''.join(valid_extensions)))

def validate_file_size(value):
    ONE_MB = 1048576
    if value.size > ONE_MB:
        raise ValidationError('Please use a file smaller than %s. Current filesize %s' % (filesizeformat(ONE_MB), filesizeformat(value.size)))