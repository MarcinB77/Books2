# Generated by Django 4.0.4 on 2022-04-30 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_list', '0006_alter_book_pub_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='language',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
