# Generated by Django 2.1.7 on 2019-03-26 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bagify', '0008_auto_20190326_1331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carouselimage',
            name='subtitle',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]