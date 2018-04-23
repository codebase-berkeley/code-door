import requests # 200 or 404


img = requests.get('https://logo.clearbit.com/google.com')
if img.status_code == 200:
	img_data = img.content

	with open('google.png', 'wb') as handler:
		handler.write(img_data)