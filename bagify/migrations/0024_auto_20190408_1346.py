# Generated by Django 2.1.7 on 2019-04-08 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bagify', '0023_auto_20190408_1316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='state',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='address',
            name='zip',
            field=models.CharField(max_length=100),
        ),
    ]