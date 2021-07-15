# Generated by Django 3.2.5 on 2021-07-15 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work_db', '0004_auto_20210715_1107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bank',
            name='account',
            field=models.CharField(blank=True, max_length=20, verbose_name='Счет'),
        ),
        migrations.AlterField(
            model_name='bank',
            name='city',
            field=models.CharField(blank=True, max_length=50, verbose_name='Город'),
        ),
        migrations.AlterField(
            model_name='bank',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='bank',
            name='update_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата обновления'),
        ),
    ]
