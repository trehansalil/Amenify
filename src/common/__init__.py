import json

import requests
from bs4 import BeautifulSoup


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


# Image Extractor
def awc_token_generator(link):
    headers = {
        'authority': 'www.apartments.com',
        'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'upgrade-insecure-requests': '1',
        'dnt': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.apartments.com/',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': 'afe=%7b%22e%22%3afalse%7d; fso=%7b%22e%22%3afalse%7d; ga=GA1.2.1410274332.1633444711; gcl_au=1.1.592405348.1633444712; pin_unauth=dWlkPVpqZzFNalkyWldVdE9ETTNaUzAwTmpSaExXSTRPR1l0WlRGbE16VTRPV1JqTmpsag; fbp=fb.1.1633473668366.1278204302; akaalb_www_apartments_com_main=~op=www_apartments_com:www_apartments_com_LAX|~rv=18~m=www_apartments_com_LAX:0|~os=0847b47fe1c72dfaedb786f1e8b4b630~id=f53fba71b8b612cf71e481a3ee24e6f9; ab=%7b%22e%22%3atrue%2c%22r%22%3a%5b%5d%7d; gip=%7b%22Display%22%3a%22Chicago%2c+IL%22%2c%22GeographyType%22%3a2%2c%22Address%22%3a%7b%22City%22%3a%22Chicago%22%2c%22State%22%3a%22IL%22%7d%2c%22Location%22%3a%7b%22Latitude%22%3a41.8337%2c%22Longitude%22%3a-87.7319%7d%7d; gid=GA1.2.311639498.1636495244; ak_bmsc=B5F4353811AB4EDB1F7FA7471C818A2D~000000000000000000000000000000~YAAQjGPUF6qNceh8AQAAQb23Bg2I4Wj92sAwx8DobtfKYNrbmQ9IxTlMMzGauSv4nGBvkQq2+g97KC3o7CoQXgHsZEHso/JeePMnV71ftsSeB4J+G8UQWeHS9+1sydHLrdjBL5TtK2iYSsJwSkpIWurnNycdJAgSXxq5X3ta+5gd5iI4PJBarDN7RLYIu+ukI0Wllpqnm4Swv2LohqgzHBC62s84/ybogPIZMz9jwMnc7MfkaZdwN6Urd9nXNI2phVC3/H1b1QHJ4UY1I+bO62wXwbPPtnuffotUzgtQhLnCC1Z8gLNBlwZmuZTnfcJHnkT2f+kqJ9nL10CtaYRNfsUxPUpk3ra8CEI/hQq4Ef2VIMbsp9msil12sVJrtck0anZA7sf03mXlGd6wqOe3I8vxvD9xXa1FuPGhuOvIBktAhCqFTCHyJI8P3JFYpzILoYvnq1sEWPsbxR1VcuR6yf/kNo+Nn0jEoctK9w5974wHEy2kdtX+73G4YXKbhRU=; scid=b71a59e7-ac9c-4792-86af-4f23378ecde4; dpm_ses.c51a=*; sctr=1|1636482600000; derived_epik=dj0yJnU9QXplOV9ON0F0dVNQdlpzWnFvQnN4UHM1eVZvTHRjMkcmbj1yTVNvYWRUTmxVSzVCUXZSN3U2a1pRJm09MSZ0PUFBQUFBR0dLNzZRJnJtPTEmcnQ9QUFBQUFHR0s3NlE; bm_sv=EFF0DA877482D6E7EFFE3CF9147D770B~raBfwkSvlIS8jKRdkU2x8frbiHL+gH/2ABlUaHOznu8NcO2b28gwua0zBLvjg/ncWOLqL8naXNj3VtRQ2YcA8CViFLj/e0Gr3c3EXLv4XWX4Z2T4mH721xxFHRYOdpp4wPAR4sqnD1ZmVkcbPEKTrFjteRXtGmK7TW5MjkVVgiw=; sr=%7B%22Width%22%3A1440%2C%22Height%22%3A176%2C%22PixelRatio%22%3A2%7D; gat=1; dpm_id.c51a=3ddcfa02-3746-4142-b0ad-decba11c21a9.1633444713.11.1636495421.1635255902.02124780-e941-4e11-89c5-9cb078ac2624; uetsid=7d102a0041a811ec98d0e91524ab7fc7; _uetvid=ea1ed44025e911ecb6938b7072c3fe1c; uat=%7b%22VisitorId%22%3a%22839cf823-a426-4c15-9397-4c629ae87b95%22%2c%22VisitId%22%3a%2229ad052d-5411-4ff1-a1a1-6cb6da52ce5a%22%2c%22LastActivityDate%22%3a%222021-11-09T14%3a03%3a41.6589531-08%3a00%22%2c%22LastFrontDoor%22%3a%22APTS%22%7d',
    }

    response = requests.get(link, headers=headers)
    soup = BeautifulSoup(response.text, features="html.parser")
    d = [i for i in soup.find_all("script") if "src" in i.attrs]
    script_call = [i for i in d if i.attrs['src'].count("/scripts/scripts.en-us.bundle.js?")]
    script_call_idx = soup.find_all("script").index(script_call[0])
    action = soup.find_all("script")[script_call_idx + 1].contents[0]
    awc_token = \
        action.split("configuration.configure(")[-1].replace(");", "").strip()[:-1].split("antiWebCrawlerToken:")[
            -1].split(
            ",")[0].replace("'", "").strip()
    return awc_token


def image_extractor(link):
    key = link.split("/")[-2]

    headers = {
        'authority': 'www.apartments.com',
        'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
        'x_csrf_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE2MzY0OTUyNjUsImV4cCI6MTYzNjU4MTY2NSwiaWF0IjoxNjM2NDk1MjY1LCJpc3MiOiJodHRwczovL3d3dy5hcGFydG1lbnRzLmNvbSIsImF1ZCI6Imh0dHBzOi8vd3d3LmFwYXJ0bWVudHMuY29tIn0._6j6QVWNYs_qavpvsU8-vX05oBlwOyAqAtZa_tPEzTs',
        'dnt': '1',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
        'content-type': 'application/json',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'x-requested-with': 'XMLHttpRequest',
        'x_awc_token': awc_token_generator(link)
        ,
        'sec-ch-ua-platform': '"macOS"',
        'origin': 'https://www.apartments.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': link,
        'accept-language': 'en-US,en;q=0.9',
        'cookie': 'afe=%7b%22e%22%3afalse%7d; fso=%7b%22e%22%3afalse%7d; ga=GA1.2.1410274332.1633444711; gcl_au=1.1.592405348.1633444712; pin_unauth=dWlkPVpqZzFNalkyWldVdE9ETTNaUzAwTmpSaExXSTRPR1l0WlRGbE16VTRPV1JqTmpsag; fbp=fb.1.1633473668366.1278204302; akaalb_www_apartments_com_main=~op=www_apartments_com:www_apartments_com_LAX|~rv=18~m=www_apartments_com_LAX:0|~os=0847b47fe1c72dfaedb786f1e8b4b630~id=f53fba71b8b612cf71e481a3ee24e6f9; ab=%7b%22e%22%3atrue%2c%22r%22%3a%5b%5d%7d; gip=%7b%22Display%22%3a%22Chicago%2c+IL%22%2c%22GeographyType%22%3a2%2c%22Address%22%3a%7b%22City%22%3a%22Chicago%22%2c%22State%22%3a%22IL%22%7d%2c%22Location%22%3a%7b%22Latitude%22%3a41.8337%2c%22Longitude%22%3a-87.7319%7d%7d; gid=GA1.2.311639498.1636495244; ak_bmsc=B5F4353811AB4EDB1F7FA7471C818A2D~000000000000000000000000000000~YAAQjGPUF6qNceh8AQAAQb23Bg2I4Wj92sAwx8DobtfKYNrbmQ9IxTlMMzGauSv4nGBvkQq2+g97KC3o7CoQXgHsZEHso/JeePMnV71ftsSeB4J+G8UQWeHS9+1sydHLrdjBL5TtK2iYSsJwSkpIWurnNycdJAgSXxq5X3ta+5gd5iI4PJBarDN7RLYIu+ukI0Wllpqnm4Swv2LohqgzHBC62s84/ybogPIZMz9jwMnc7MfkaZdwN6Urd9nXNI2phVC3/H1b1QHJ4UY1I+bO62wXwbPPtnuffotUzgtQhLnCC1Z8gLNBlwZmuZTnfcJHnkT2f+kqJ9nL10CtaYRNfsUxPUpk3ra8CEI/hQq4Ef2VIMbsp9msil12sVJrtck0anZA7sf03mXlGd6wqOe3I8vxvD9xXa1FuPGhuOvIBktAhCqFTCHyJI8P3JFYpzILoYvnq1sEWPsbxR1VcuR6yf/kNo+Nn0jEoctK9w5974wHEy2kdtX+73G4YXKbhRU=; gat=1; scid=b71a59e7-ac9c-4792-86af-4f23378ecde4; dpm_ses.c51a=*; sctr=1|1636482600000; bm_sv=EFF0DA877482D6E7EFFE3CF9147D770B~raBfwkSvlIS8jKRdkU2x8frbiHL+gH/2ABlUaHOznu8NcO2b28gwua0zBLvjg/ncWOLqL8naXNj3VtRQ2YcA8CViFLj/e0Gr3c3EXLv4XWUN10hNu5aNUEvfZ3IZZ1XENvy2XiNeD4uERTT7JSxpA7btN3q2ZUXKuctPuXYqDps=; sr=%7B%22Width%22%3A1440%2C%22Height%22%3A150%2C%22PixelRatio%22%3A2%7D; uat=%7b%22VisitorId%22%3a%22839cf823-a426-4c15-9397-4c629ae87b95%22%2c%22VisitId%22%3a%2229ad052d-5411-4ff1-a1a1-6cb6da52ce5a%22%2c%22LastActivityDate%22%3a%222021-11-09T14%3a01%3a07.0572776-08%3a00%22%2c%22LastFrontDoor%22%3a%22APTS%22%7d; dpm_id.c51a=3ddcfa02-3746-4142-b0ad-decba11c21a9.1633444713.11.1636495267.1635255902.02124780-e941-4e11-89c5-9cb078ac2624; uetsid=7d102a0041a811ec98d0e91524ab7fc7; uetvid=ea1ed44025e911ecb6938b7072c3fe1c; _derived_epik=dj0yJnU9QXplOV9ON0F0dVNQdlpzWnFvQnN4UHM1eVZvTHRjMkcmbj1yTVNvYWRUTmxVSzVCUXZSN3U2a1pRJm09MSZ0PUFBQUFBR0dLNzZRJnJtPTEmcnQ9QUFBQUFHR0s3NlE',
    }

    data = '{"ListingKey":"' + key + '"}'

    response = requests.post('https://www.apartments.com/services/property/profilemedia/', headers=headers, data=data)

    output = json.loads(response.text)
    all_images = [i['Uri'] for i in output['Carousel']]

    # community_outside = all_images[0]
    # community_inside = [i for i in all_images[::-1] if i.count("building-photo") != 0][0]
    return all_images


# Education Data Extractor
def super_education(soup, typ="Public", dev="title"):
    data_fetch = []
    [data_fetch.extend(i.select(f".{dev}")) for i in
     soup.select("#educationContainer")[0].select(f".schools{typ}Container.cell-xs-12.tabContent")]
    return [i.get_text().strip() for i in data_fetch if i.get_text().strip()]


def education_data_fetcher(soup, typ="Public"):
    keys = super_education(soup=soup, typ=typ, dev="title")
    type_list = super_education(soup=soup, typ=typ, dev="subtitle")
    grade_list = [i for i in super_education(soup=soup, typ=typ, dev="bodyTextLine") if i.count("Grade")]
    if len(super_education(soup=soup, typ=typ, dev="schoolScore")) != 0:
        score_list = [int(i) for i in super_education(soup=soup, typ=typ, dev="schoolScore")]
    else:
        score_list = []
    delta = {i: [] for i in keys}
    #     print(keys)
    for enum, i in enumerate(keys):
        if len(type_list) != 0:
            delta[i].append(type_list[enum])
        if len(grade_list) != 0:
            delta[i].append(grade_list[enum])
        if len(score_list) != 0:
            #             print(score_list)
            try:
                delta[i].append(score_list[enum])
            except:
                delta[i].append(None)
    return {f"{typ} Schools": delta}
