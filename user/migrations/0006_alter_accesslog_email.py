# Generated by Django 4.2.1 on 2023-05-09 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_accesslog_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accesslog',
            name='email',
            field=models.CharField(max_length=30, verbose_name='email address'),
        ),
    ]