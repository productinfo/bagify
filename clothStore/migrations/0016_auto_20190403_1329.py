# Generated by Django 2.1.7 on 2019-04-03 13:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clothStore', '0015_auto_20190403_1246'),
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=30)),
                ('value', models.CharField(max_length=20)),
                ('stock', models.IntegerField(default=0)),
                ('sold_units', models.IntegerField(default=0)),
            ],
        ),
        migrations.RenameField(
            model_name='item',
            old_name='sold_units',
            new_name='total_units_sold',
        ),
        migrations.RemoveField(
            model_name='item',
            name='colors',
        ),
        migrations.RemoveField(
            model_name='item',
            name='stock',
        ),
        migrations.AddField(
            model_name='image',
            name='main_display',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='color',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='colors', to='clothStore.Item'),
        ),
    ]
