import csv
from codedoor.models import Company

with open('companies.csv', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        print('Company name:' + row[1])
        name = row[1]
        print('Industry: ' + row[3])
        industry = row[3]
        print('Website:' + row[2])
        website = row[2]
        fund = 0;
        structure = 'Startup'
        try:
        	fund = int(row[4])
        except ValueError:
        	pass
        if fund > 2000000:
        	print('Structure: Large')
        	structure = 'Large'
        elif fund > 1000000:
        	print('Structure: Medium')
        	structure = 'Medium'
        elif fund > 500000:
        	print('Structure: Small')
        	structure = 'Small'
        elif fund > 250000:
        	print('Structure: Boutique')
        	structure = 'Boutique'
        else:
        	print('Structure: Startup')
        	structure = 'Startup'
        company = Company(name=name, industry=industry, website=website, structure=structure)
        company.save()
