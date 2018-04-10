
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('year', models.IntegerField()),
                ('season', models.CharField(choices=[('Fall', 'Fall'), ('Spring', 'Spring'), ('Summer', 'Summer'), ('Winter', 'Winter')], max_length=100)),
                ('position', models.CharField(max_length=500)),
                ('received_offer', models.BooleanField()),
                ('offer_details', models.TextField(blank=True, null=True)),
                ('difficult', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('industry', models.CharField(max_length=100)),
                ('website', models.URLField(blank=True, null=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='')),
                ('structure', models.CharField(choices=[('Startup', 'Startup'), ('Boutique', 'Boutique'), ('Small', 'Small'), ('Medium', 'Medium'), ('Large', 'Large')], max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_pic', models.URLField(blank=True, null=True)),
                ('graduation_year', models.IntegerField()),
                ('current_job', models.CharField(blank=True, max_length=1000, null=True)),
                ('linkedin', models.URLField(blank=True, null=True)),
                ('resume', models.FileField(blank=True, null=True, upload_to='')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('applicant_answer', models.TextField(blank=True, null=True)),
                ('actual_answer', models.TextField(blank=True, null=True)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='codedoor.Application')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.DecimalField(decimal_places=2, max_digits=10)),
                ('recommend', models.BooleanField()),
                ('review', models.TextField()),
                ('title', models.CharField(blank=True, max_length=200, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='codedoor.Company')),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='codedoor.Profile')),
            ],
        ),
        migrations.AddField(
            model_name='application',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='codedoor.Company'),
        ),
        migrations.AddField(
            model_name='application',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='codedoor.Profile'),
        ),
    ]