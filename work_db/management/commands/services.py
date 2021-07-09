import zipfile
import requests
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError

from work_db.models import Bank
from work_db.models import Files


class Command(BaseCommand):
    help = 'Adding banks to the database'

    def handle(self, *args, **options):
        url = settings.URL
        resp = requests.get(url)
        if resp.status_code != requests.codes.ok:
            CommandError('Cannot download file')
        content_file = ContentFile(resp.content, name='some_name.rar')
        f = Files.objects.create(file_field=content_file)
        with zipfile.ZipFile(f.file_field.name) as zf:
            zf.extract('bnkseek.txt', 'media/')

        with open('media/bnkseek.txt') as file:
            for line in file:
                _, city, _, name, _, bik, account = line.split('\t')  # 5 - bik
                account = account.split('\n')
                Bank.objects.get_or_create(
                    city=city,
                    name=name,
                    bik=bik,
                    account=account[0]
                )
