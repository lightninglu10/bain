# Generated by Django 2.0.6 on 2018-06-12 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthset', '0003_auto_20180612_0407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inpatient',
            name='avg_covered_charges',
            field=models.IntegerField(db_index=True, default=0),
        ),
        migrations.AlterField(
            model_name='inpatient',
            name='avg_medicare_payments',
            field=models.IntegerField(db_index=True, default=0),
        ),
        migrations.AlterField(
            model_name='inpatient',
            name='avg_total_payments',
            field=models.IntegerField(db_index=True, default=0),
        ),
    ]
