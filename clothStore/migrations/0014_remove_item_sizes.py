# Generated by Django 2.1.7 on 2019-04-03 12:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clothStore', '0013_auto_20190401_1106'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='sizes',
        ),
    ]
