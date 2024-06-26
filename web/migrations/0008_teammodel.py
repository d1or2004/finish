# Generated by Django 5.0.6 on 2024-06-16 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0007_costumer_testimonial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=443)),
                ('image', models.ImageField(upload_to='media/team/')),
                ('description', models.TextField()),
            ],
        ),
    ]
