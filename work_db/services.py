from django.conf import settings
import requests
from django.core.management.base import CommandError
from django.core.files.base import ContentFile
from work_db.models import Files
from django.conf import settings


def load():
    url = settings.URL
    resp = requests.get(url)
    if resp.status_code != requests.codes.ok:
        raise CommandError('Cannot download file')
    content_file = ContentFile(resp.content, name='some_name.rar')
    f = Files.objects.create(file_field=content_file)
    return f
