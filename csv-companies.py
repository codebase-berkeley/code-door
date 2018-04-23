import csv
import json
import requests

lst = []

with open('companies.csv', newline='', encoding='utf-8') as f:
    next(f)
    reader = csv.reader(f)
    pk = 1
    for row in reader:
        websites = row[2].split(';')
        website = websites[0]
        if website[0:5] == 'https':
            url = website[8:-1]
        else:
            url = website[7:-1]

        img = requests.get('https://logo.clearbit.com/' + url)
        if img.status_code == 200:
            img_data = img.content

            # NEEDS TO UPLOAD TO S3
            # with open('static/images/logos/' + name + '.png', 'wb') as handler:
            #     handler.write(img_data)
        else:
            continue

        name = row[1][:100]
        industry = row[3][:100]
        fund = 0
        structure = 'Startup'
        try:
            fund = int(row[4])
        except ValueError:
            pass
        if fund > 2000000:
            structure = 'Large'
        elif fund > 1000000:
            structure = 'Medium'
        elif fund > 500000:
            structure = 'Small'
        elif fund > 250000:
            structure = 'Boutique'
        else:
            structure = 'Startup'

        company_fields = {"name": name,
                          "industry": industry,
                          "website": website,
                          "logo": None,
                          "structure": structure}
        company = {"model": "codedoor.company",
                   "pk": pk,
                   "fields": company_fields}
        lst.append(company)
        pk += 1

with open('codedoor/fixtures/companies.json', 'w+') as g:
    g.write(json.dumps(lst))


