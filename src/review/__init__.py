import requests
import json


# Function for extracting the reviews
def reviews_extractor(link):
    key = link.split("/")[-2]
    headers = {
        'authority': 'www.apartments.com',
        'dnt': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
        'content-type': 'application/json',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'x-requested-with': 'XMLHttpRequest',
        'origin': 'https://www.apartments.com',
        'referer': link,
        'accept-language': 'en-US,en;q=0.9'}

    data = '{"ListingKeys":["' + f"{key}" + '"]}'
    response = requests.post('https://www.apartments.com/services/reviews/profile/get', headers=headers, data=data)
    d = json.loads(response.text)
    if "Reviews" in d:
        return json.loads(response.text)['Reviews']
    else:
        return []
