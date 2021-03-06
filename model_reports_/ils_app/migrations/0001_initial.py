# Generated by Django 2.1.3 on 2018-12-08 04:54

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Authors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=200, verbose_name='First Name')),
                ('lastname', models.CharField(max_length=200, verbose_name='Last Name')),
            ],
            options={
                'ordering': ('firstname', 'lastname'),
                'verbose_name_plural': 'Personal Authors',
                'verbose_name': 'Personal Author',
            },
        ),
        migrations.CreateModel(
            name='Biblio',
            fields=[
                ('biblionumber', models.AutoField(primary_key=True, serialize=False)),
                ('isbn', models.CharField(blank=True, max_length=13, null=True, verbose_name='ISBN')),
                ('callnumber', models.CharField(blank=True, max_length=15, null=True)),
                ('title', models.CharField(max_length=250, verbose_name='Biblio Title')),
                ('edition', models.CharField(blank=True, max_length=50, null=True)),
                ('copyrightdate', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Copyright Date')),
                ('series', models.CharField(blank=True, max_length=250, null=True)),
                ('volume', models.CharField(blank=True, max_length=20, null=True)),
                ('pages', models.CharField(max_length=10)),
                ('size', models.CharField(blank=True, max_length=5, null=True)),
                ('contents_url', models.URLField(blank=True, null=True)),
                ('index_url', models.URLField(blank=True, null=True)),
                ('itemtype', models.CharField(choices=[('BK', 'Book'), ('PR', 'Project Report'), ('TD', 'Theses'), ('XM', 'Xerox Material'), ('RB', 'Reference Book')], db_index=True, default='BK', max_length=2, verbose_name='Item Type')),
                ('totalissues', models.IntegerField(blank=True, default=0, null=True)),
                ('totalholds', models.IntegerField(blank=True, default=0, null=True)),
                ('timestamp_lastupdated', models.DateTimeField(auto_now=True, db_index=True)),
                ('timestamp_added', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('authors', models.ManyToManyField(blank=True, related_name='additional_authors', to='ils_app.Authors', verbose_name='all authors')),
            ],
            options={
                'ordering': ('title',),
                'verbose_name_plural': 'Biblios',
                'verbose_name': 'Biblio',
            },
        ),
        migrations.CreateModel(
            name='Borrowers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('cardnumber', models.CharField(max_length=16, unique=True, verbose_name='Cardnumber')),
                ('surname', models.CharField(max_length=100, verbose_name='Last name')),
                ('firstname', models.CharField(max_length=100, verbose_name='First name')),
                ('birth_date', models.DateField(db_index=True, verbose_name='Birth date')),
                ('mobile', models.CharField(blank=True, max_length=32, null=True)),
                ('dateenrolled', models.DateField(auto_now_add=True)),
                ('dateexpiry', models.DateField()),
                ('gonenoaddress', models.BooleanField(default=False, verbose_name='Is Left')),
                ('lost', models.BooleanField(default=False, verbose_name='Is Card Lost')),
                ('debarred', models.DateField(blank=True, null=True, verbose_name='Is Suspended')),
                ('debarredcomment', models.CharField(blank=True, max_length=100, null=True)),
                ('borrowernote', models.CharField(blank=True, max_length=255, null=True, verbose_name='Borrower Intranet Note')),
                ('opacnote', models.CharField(blank=True, max_length=255, null=True, verbose_name='Borrower OPAC Note')),
                ('timestamp_lastupdated', models.DateTimeField(auto_now=True)),
                ('timestamp_added', models.DateTimeField(auto_now_add=True)),
                ('borrower', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='djk_borrower', to='accounts.Profile')),
            ],
            options={
                'ordering': ('firstname', 'surname', 'birth_date'),
                'verbose_name_plural': 'Borrower Records',
                'verbose_name': 'Borrower Record',
            },
        ),
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categorycode', models.CharField(max_length=10, unique=True, verbose_name='Borrower Category Code')),
                ('description', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ('categorycode',),
                'verbose_name_plural': 'Patron Categories',
                'verbose_name': 'Patron Category',
            },
        ),
        migrations.CreateModel(
            name='CollectionDepartments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deptcode', models.CharField(max_length=50, unique=True)),
                ('description', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ('deptcode',),
                'verbose_name_plural': 'Collection Departments',
                'verbose_name': 'Collection Department',
            },
        ),
        migrations.CreateModel(
            name='CorporateAuthor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Corporate Author')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name_plural': 'Corporate Bodies',
                'verbose_name': 'Corporate Body',
            },
        ),
        migrations.CreateModel(
            name='Departments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deptcode', models.CharField(max_length=50, unique=True)),
                ('description', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ('deptcode',),
                'verbose_name_plural': 'Patron Departments',
                'verbose_name': 'Patron Department',
            },
        ),
        migrations.CreateModel(
            name='Designations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('designation', models.CharField(max_length=10, unique=True)),
                ('description', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ('description',),
                'verbose_name_plural': 'Patron Designations',
                'verbose_name': 'Patron Designation',
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, unique=True, verbose_name='Subject Name')),
            ],
            options={
                'ordering': ('name',),
                'verbose_name_plural': 'Subjects',
                'verbose_name': 'Subject',
            },
        ),
        migrations.CreateModel(
            name='Items',
            fields=[
                ('itemnumber', models.AutoField(primary_key=True, serialize=False)),
                ('barcode', models.CharField(max_length=25, unique=True, verbose_name='Accession Number Barcode')),
                ('dateaccessioned', models.DateField(default=django.utils.timezone.now)),
                ('booksellerid', models.CharField(blank=True, max_length=25, null=True, verbose_name='Source of acquisition')),
                ('invoicenumber', models.CharField(blank=True, max_length=15, null=True)),
                ('invoicedate', models.DateField(blank=True, default=django.utils.timezone.now, null=True)),
                ('totalissues', models.PositiveSmallIntegerField(blank=True, default=0, null=True)),
                ('itemstatus', models.CharField(choices=[('AV', 'Available'), ('OL', 'On Loan'), ('DM', 'Damaged'), ('LO', 'Lost'), ('LP', 'Lost and Paid for'), ('MI', 'Missing'), ('WD', 'Withdrawn'), ('BD', 'In Bindery')], db_index=True, default='AV', max_length=2, verbose_name='Item Availability Status')),
                ('location', models.CharField(choices=[('GEN', 'General Shelf'), ('REF', 'Reference Shelf'), ('OD', 'On-Display'), ('PROC', 'Processing Center'), ('SO', 'Staff Office'), ('BC', 'Book Cart'), ('NMS', 'New Materials Shelf')], default='GEN', max_length=4, verbose_name='Shelf location')),
                ('notforloan', models.CharField(blank=True, choices=[('1', 'Not for loan'), ('2', 'Staff Copy'), ('3', 'Ordered')], max_length=1, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('replacementprice', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('timestamp_lastupdated', models.DateTimeField(auto_now=True)),
                ('timestamp_added', models.DateTimeField(auto_now_add=True)),
                ('biblionumber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ils_app.Biblio', verbose_name='Biblio')),
                ('collectiondepartment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ils_app.CollectionDepartments')),
            ],
            options={
                'verbose_name_plural': 'Biblio Items',
                'verbose_name': 'Biblio Item',
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text="Enter the biblio item's natural language.", max_length=30, unique=True, verbose_name='Language')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name_plural': 'Biblio Languages',
                'verbose_name': 'Biblio Language',
            },
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Publisher Name')),
            ],
            options={
                'ordering': ('name',),
                'verbose_name_plural': 'Publishers',
                'verbose_name': 'Publisher',
            },
        ),
        migrations.CreateModel(
            name='Reserves',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reservedate', models.DateTimeField(auto_now_add=True, verbose_name='Reserved On')),
                ('cancellationdate', models.DateTimeField(blank=True, null=True, verbose_name='Reservation Cancelled On')),
                ('priority', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Hold Priority')),
                ('found', models.BooleanField(default=False, verbose_name='Reserve Found?')),
                ('notificationdate', models.DateTimeField(blank=True, null=True, verbose_name='Notified On')),
                ('waitingdate', models.DateTimeField(blank=True, null=True, verbose_name='Date Waiting')),
                ('timestamp_lastupdated', models.DateTimeField(auto_now=True)),
                ('biblio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ils_app.Biblio', verbose_name='Biblio Reserved')),
                ('borrower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ils_app.Borrowers', verbose_name='Library Patron')),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ils_app.Items', verbose_name='Item Waiting')),
            ],
            options={
                'verbose_name_plural': 'Biblio Level Reservation',
                'verbose_name': 'Biblio Level Reservation',
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=64, unique=True, verbose_name='Company name')),
                ('direct_shipping', models.BooleanField(verbose_name='Direct shipping')),
            ],
            options={
                'ordering': ('company_name',),
                'verbose_name_plural': 'Book Suppliers',
                'verbose_name': 'Book Supplier',
            },
        ),
        migrations.AddField(
            model_name='borrowers',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ils_app.Categories', verbose_name='Patron Category'),
        ),
        migrations.AddField(
            model_name='borrowers',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ils_app.Departments', verbose_name='Patron Department'),
        ),
        migrations.AddField(
            model_name='borrowers',
            name='designation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ils_app.Designations', verbose_name='Patron Desingation'),
        ),
        migrations.AddField(
            model_name='biblio',
            name='corporateauthor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ils_app.CorporateAuthor', verbose_name='Corporate Author'),
        ),
        migrations.AddField(
            model_name='biblio',
            name='first_author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ils_app.Authors', verbose_name='Primary Author'),
        ),
        migrations.AddField(
            model_name='biblio',
            name='genre',
            field=models.ManyToManyField(blank=True, related_name='Topical_Terms', to='ils_app.Genre', verbose_name='Topical Term(s)'),
        ),
        migrations.AddField(
            model_name='biblio',
            name='language',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ils_app.Language'),
        ),
        migrations.AddField(
            model_name='biblio',
            name='publisher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ils_app.Publisher', verbose_name='Publication Details'),
        ),
        migrations.AddField(
            model_name='biblio',
            name='subject_heading',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ils_app.Genre', verbose_name='Subject Heading'),
        ),
        migrations.AlterUniqueTogether(
            name='authors',
            unique_together={('firstname', 'lastname')},
        ),
        migrations.AlterUniqueTogether(
            name='reserves',
            unique_together={('borrower', 'biblio')},
        ),
        migrations.AlterUniqueTogether(
            name='borrowers',
            unique_together={('firstname', 'surname', 'birth_date')},
        ),
    ]
