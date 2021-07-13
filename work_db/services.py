from work_db.models import Bank
import requests
from django.core.management.base import CommandError
from django.core.files.base import ContentFile
from django.conf import settings
import zipfile


class WorkWiBanks:

    URL = settings.URL
    file_name = 'bnkseek.txt'
    media_url = 'media/'

    @staticmethod
    def getContent():
        response = requests.get(WorkWiBanks.URL)
        if response.status_code != requests.codes.ok:
            raise CommandError('Cannot download file')
        print(response.content)
        return response.content

    @staticmethod
    def extract_zip(content):
        content = ContentFile(content)
        with zipfile.ZipFile(content.file) as zf:
            zf.extract(WorkWiBanks.file_name, WorkWiBanks.media_url)

    @staticmethod
    def saveInfoBanks():
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

    @classmethod
    def load_and_save_infoBank(cls):
        content = cls.getContent()
        cls.extract_zip(content)
        cls.saveInfoBanks()
