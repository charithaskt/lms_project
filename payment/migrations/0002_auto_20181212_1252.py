# Generated by Django 2.0 on 2018-12-12 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='paytmhistory',
            name='user',
            field=models.CharField(max_length=50, null=True, verbose_name='UNAME'),
        ),
        migrations.AlterField(
            model_name='paytmhistory',
            name='TXNID',
            field=models.CharField(max_length=999, verbose_name='TXN ID'),
        ),
    ]