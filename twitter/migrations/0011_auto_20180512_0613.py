# Generated by Django 2.0.5 on 2018-05-12 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0010_auto_20180512_0603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=40),
        ),
    ]
