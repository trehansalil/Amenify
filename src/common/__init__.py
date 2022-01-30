from bs4 import BeautifulSoup
import requests


def unique_list(a):
    k = []
    for j in a:
        if j not in k:
            k.append(j)
    return k


def link_extractor(link, pg='', a=[]):
    headers = {
        'authority': 'www.apartments.com',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }
    if pg:
        response = requests.get(f'{link}{pg}/', headers=headers)
        soup = BeautifulSoup(response.text)
        a.extend(unique_list([i['href'] for i in soup.select(".property-link")]))

    else:
        response = requests.get(f'{link}', headers=headers)
        soup = BeautifulSoup(response.text)
        a.extend(unique_list([i['href'] for i in soup.select(".property-link")]))
        pages = soup.select_one(".pageRange").get_text().lower().replace("page", "").replace("of", "").strip().split()
        print(f"The number of Pages that are to be crawled are: {int(pages[1])}")
        print(len(a))
        pages = [int(pg) + 1 for pg in pages]
        for j in range(pages[0], pages[1]):
            print(len(link_extractor(link=link, pg=str(j), a=a)))
    return a


# Constructor for storing the data
def apartments_data_obj():
    return ({
        "link": None,
        "name": None,
        "primary_photo": None,
        "backdrop": [],
        "description": None,
        "property_min_price": None,
        "property_max_price": None,
        "phone_number": None,
        "address": None,
        'locality': None,
        'region': None,
        'pin_code': None,
        'country': None,
        'opening_timings': [],
        'type': None,
        'latitude': None,
        'longitude': None,
        'property_type': None,
        'pets_allowed': None,
        "reviews": [],
        'amenities': [],
        'nearby_areas': [],
        'Neighborhood_description': None,
        'parking': [],
        'lease_options': None,
        "fee_details": [],
        "pets_details": [],
        "nearby_public_schools": [],
        "nearby_private_schools": [],
        "model_details": [],
        "community_outside_image": [],
        "community_inside_image": [],
        "all_images": [],
        "management_company_logo": None,
        "leasing_periods": [],
        "number_of_units": [],
        "number_of_stories": [],
        "distance_to_city_centre": None,
        "model_name": [],
        "rent_Details": [],
        "sq_ft_Details": []
    })
