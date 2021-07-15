from work_db.models import Bank
import requests
from django.core.management.base import CommandError
from django.conf import settings
import zipfile
import io


class WorkWithBanks:
    URL = settings.URL

    @staticmethod
    def getContent():
        response = requests.get('https://its.1c.ru/download/bank/download')
        if response.status_code != requests.codes.ok:
            raise CommandError('Cannot download file')
        return response.content

    @staticmethod
    def read_zip_bytes(content):
        byte: bytes
        b_bytes = io.BytesIO(content)
        with zipfile.ZipFile(b_bytes) as zf:
            with zf.open('bnkseek.txt') as file:
                byte = file.read()
                text = byte.decode('windows-1251')
        return text

    @staticmethod
    def saveInfoBanks(text):
        text = text.split('\n')
        text.pop(-1)  # delete because last line text = ['']
        for line in text:
            line = line.split('\t')
            _, city, _, name, _, bik, account = line
            Bank.objects.get_or_create(
                city=city,
                name=name,
                bik=bik,
                account=account,
            )

    @classmethod
    def load_and_save_infoBank(cls):
        content = cls.getContent()
        text = cls.read_zip_bytes(content)
        cls.saveInfoBanks(text)
