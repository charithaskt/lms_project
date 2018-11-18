# Generated by Django 2.0.7 on 2018-11-15 06:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('intranet', '0012_auto_20181114_0441'),
    ]

    operations = [
        migrations.CreateModel(
            name='PatronBulkPhotos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='patron_bulk_photos/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('patron_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='intranet.Borrowers')),
            ],
        ),
    ]
