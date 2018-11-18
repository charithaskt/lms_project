# Generated by Django 2.0.7 on 2018-11-11 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intranet', '0004_auto_20181111_1101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actionlogs',
            name='action',
            field=models.CharField(choices=[('CREATE', 'Create'), ('ADDCHILD', 'Add child record'), ('MODCHILD', 'Modify child record'), ('DELCHILD', 'Delete child record'), ('MODIFY', 'Modify or edit record'), ('ISSUE', 'Issue'), ('RETURN', 'Return'), ('RENEW', 'Renew'), ('DELETE', 'Delete'), ('CHANGE PASS', 'Change Password Through OPAC'), ('RESERVE', 'Reserve'), ('FINE', 'Collect fine'), ('WRITEOFF', 'Write off fine'), ('RUN', 'Run report'), ('RENEWSELF', 'Renew self'), ('RESERVESELF', 'Reserve self')], max_length=11),
        ),
    ]
