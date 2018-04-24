import csv
import json
import requests
import boto3
from api_keys import s3_access_keys

company_logos_bucket = 'codedoor-company-logos'

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

            s3 = boto3.resource('s3', aws_access_key_id=s3_access_keys["id"],
                                aws_secret_access_key=s3_access_keys["secret"])
            s3.Bucket(company_logos_bucket).put_object(Key=str(pk), Body=img_data, ACL='public-read')

            url = "https://s3-us-west-1.amazonaws.com/" + company_logos_bucket + "/" + str(pk)
            print(url)
            logo = url

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
                          "logo": logo,
                          "structure": structure}
        company = {"model": "codedoor.company",
                   "pk": pk,
                   "fields": company_fields}
        lst.append(company)
        pk += 1

with open('codedoor/fixtures/companies.json', 'w+') as g:
    g.write(json.dumps(lst))
