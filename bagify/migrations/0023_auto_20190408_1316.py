# Generated by Django 2.1.7 on 2019-04-08 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bagify', '0022_auto_20190408_1047'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='customer_number',
        ),
        migrations.AddField(
            model_name='order',
            name='name',
            field=models.CharField(default='Joao', max_length=100),
            preserve_default=False,
        ),
    ]
