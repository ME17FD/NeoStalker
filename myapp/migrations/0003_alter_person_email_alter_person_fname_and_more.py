# Generated by Django 4.2.5 on 2023-10-17 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_remove_person_id_alter_person_cin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='email',
            field=models.EmailField(max_length=1254),
        ),
        migrations.AlterField(
            model_name='person',
            name='fname',
            field=models.CharField(max_length=51),
        ),
        migrations.AlterField(
            model_name='person',
            name='lname',
            field=models.CharField(max_length=51),
        ),
    ]
