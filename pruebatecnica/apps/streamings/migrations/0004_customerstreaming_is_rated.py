# Generated by Django 4.2.1 on 2023-05-07 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streamings', '0003_alter_streamings_num_visualizations_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerstreaming',
            name='is_rated',
            field=models.BooleanField(default=False),
        ),
    ]