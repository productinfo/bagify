# Generated by Django 2.1.7 on 2019-04-11 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bagify', '0025_secondarycarousel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='secondarycarousel',
            name='url',
            field=models.CharField(blank=True, max_length=800, null=True),
        ),
    ]