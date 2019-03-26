# Generated by Django 2.1.7 on 2019-03-24 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clothStore', '0003_auto_20190323_1201'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('U', 'Unisex')], default='U', max_length=1),
            preserve_default=False,
        ),
    ]