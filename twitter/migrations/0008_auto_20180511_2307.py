# Generated by Django 2.0.5 on 2018-05-11 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0007_auto_20180511_2306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, to='twitter.Tag'),
        ),
    ]
