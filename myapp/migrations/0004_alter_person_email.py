# Generated by Django 4.2.5 on 2023-10-17 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_alter_person_email_alter_person_fname_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='email',
            field=models.CharField(max_length=54),
        ),
    ]
