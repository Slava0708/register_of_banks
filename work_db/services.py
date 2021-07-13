from work_db.models import Bank
import requests
from django.core.management.base import CommandError
from django.core.files.base import ContentFile
from django.conf import settings
import zipfile


class Work_with_Banks(object):
    def load_the_archive_of_banks(self):
        url = settings.URL
        resp = requests.get('https://its.1c.ru/download/bank/download')
        if resp.status_code != requests.codes.ok:
            raise CommandError('Cannot download file')
        content_file = ContentFile(resp.content)
        with zipfile.ZipFile(content_file.file) as zf:
            zf.extract('bnkseek.txt', 'media/')
        with open('media/bnkseek.txt', encoding='Windows-1251') as file:
            for line in file:
                _, city, _, name, _, bik, account = line.split('\t')  # 5 - bik
                account = account.strip()
                Bank.objects.get_or_create(
                    city=city,
                    name=name,
                    bik=bik,
                    account=account,
                )
        return True
