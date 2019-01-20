from django.db import migrations, models

def set_company_averages(apps, schema_editor):
    Review = apps.get_model('codedoor', 'Review')
    Company = apps.get_model('codedoor', 'Company')

    def compute_avg(company):
        company_reviews = Review.objects.filter(company=company)
        sum = 0.0
        for r in company_reviews:
            sum += r.rating
        if len(company_reviews):
            company.avg_rating = sum / len(company_reviews)
        else:
            company.avg_rating = 0.0
        company.save()

    for c in Company.objects.all().iterator():
        compute_avg(c)

def reverse_func(apps, schema_editor):
    pass # this is not a reversible migration.

class Migration(migrations.Migration):

    dependencies = [
        ('codedoor', '0004_auto_20190104_0147'),
    ]

    operations = [
        migrations.RunPython(set_company_averages, reverse_func),
    ]