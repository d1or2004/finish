# Generated by Django 5.0.6 on 2024-06-15 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermadel',
            name='telegram_id',
            field=models.PositiveBigIntegerField(default=1, unique=True, verbose_name='Telegram Id'),
            preserve_default=False,
        ),
    ]
