from bs4 import BeautifulSoup
import requests


def unique_list(a):
    k = []
    for j in a:
        if j not in k:
            k.append(j)
    return k


def link_extract(link, pg='', a=[]):
    headers = {
        'authority': 'www.apartments.com',
        #     'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
        #     'sec-ch-ua-mobile': '?0',
        #     'sec-ch-ua-platform': '"Windows"',
        #     'dnt': '1',
        #     'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        #     'sec-fetch-site': 'none',
        #     'sec-fetch-mode': 'navigate',
        #     'sec-fetch-user': '?1',
        #     'sec-fetch-dest': 'document',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        #     'cookie': 'ab=%7b%22e%22%3atrue%2c%22r%22%3a%5b%5d%7d; afe=%7b%22e%22%3afalse%7d; fso=%7b%22e%22%3afalse%7d; gip=%7b%22Display%22%3a%22Chicago%2c+IL%22%2c%22GeographyType%22%3a2%2c%22Address%22%3a%7b%22City%22%3a%22Chicago%22%2c%22State%22%3a%22IL%22%7d%2c%22Location%22%3a%7b%22Latitude%22%3a41.8337%2c%22Longitude%22%3a-87.7319%7d%7d; akaalb_www_apartments_com_main=~op=www_apartments_com:www_apartments_com_RESTON|~rv=86~m=www_apartments_com_RESTON:0|~os=0847b47fe1c72dfaedb786f1e8b4b630~id=e72e97970e96b024347364f7b209b263; _ga=GA1.2.582689135.1643484906; _gid=GA1.2.1494648109.1643484906; ak_bmsc=BA97247F433F195FECF60B8563251E26~000000000000000000000000000000~YAAQfsEzuP5Og3t+AQAA63pVpw6gZfEn7WZL0nOjrWGJ7ioGTJ9rSyaZpOjT3lGd3ZtJcRfD2evO/mKA23Hp6Wjcc2qViaQwq59GQ7OLHe0oASrXzOeC7MDSxKGTivyXNAZbSNugyVRnCL4E8Zjisb/Y1YrAxv8SgoNIGGmN2Dpn7G4x3iLPMzmUjKWeiP4a0v4K3dh3By86JcX7qh0RMvR2ycPlU6L8Y2ZAv9Ygx5xY2kaHcmBgonddJTiPl9oSeCCliX//+WSwS0XmupwguyHVAce9qn2j0UYKqumPfujmefEFv8pns6mftt7paR7jf/SbR+6+4vhJiInJK/SslSmvroE0cvfxYS6xcZnKAhY51aH6sNrnR2zGe5PpmbcHUkZc5WInNZ8XqjDXqpqMNy6g33JTP8ZmC3uUm33qHw3tiVXMKNgDkMu7I4tmcxBUI/QHU1aBEU9bj5PEt05CRQ9ADhVPmViE5RoZt4QKhw74U2CgyEXd2n4t4DT71UM=; _gcl_au=1.1.1158689827.1643484907; _scid=c53d89d9-baf8-4ad5-81a6-b617662901dd; _dpm_ses.c51a=*; _sctr=1|1643481000000; s=; _dpm_id.c51a=7ed969df-43a5-4841-997e-0da869a0bb12.1643484908.1.1643486053.1643484908.4a44b69e-7e68-4d49-a93a-7aa8b68ffde0; _uetsid=90580280813a11eca6817d62e3ce37cc; _uetvid=90584ba0813a11eca6a3ff13601ae6a2; cto_bundle=KtcjAl9sRGZOQTZIaWElMkJKOHdHd0U2SSUyQmdNUUt3Tk1qaGFzJTJGYkFaMGlLc3NaT0FHamNVbUdRQjloc3c4bkpFYkpDR1IlMkJ3VGZjVEJ3M1FUYndlcXVDZkNpWXo4NEZIenB2TEdma1daM05sJTJCNng0aHJOeWE0UUxJdkRkelRtb2JiNENYd3pCYUFzcXdyR0RNR0cwOWM4ZVpYVyUyRnclM0QlM0Q; _pin_unauth=dWlkPU5UWXlPV0ppTWpndFpHRm1NUzAwTWpSbUxUZ3dNbUV0TnpreE9UQmlaVFkxWlRBMQ; sr=%7B%22Width%22%3A982%2C%22Height%22%3A722%2C%22PixelRatio%22%3A1.25%7D; uat=%7B%22VisitorId%22%3A%221d431111-b78e-46c8-a851-f61aa65cf529%22%2C%22VisitId%22%3A%22ba30bbcf-4b1b-4786-979d-f9ebfdb11467%22%2C%22LastActivityDate%22%3A%222022-01-29T14%3A54%3A09.9053951-05%3A00%22%2C%22LastFrontDoor%22%3A%22APTS%22%2C%22LastSearchId%22%3A%22E959EE25-8D59-4D34-9CD4-46D57CCB76A0%22%7D; bm_sv=8AACEC289D003D153535069B7F956D58~QCz6fAHAWnDUeYs+1uVGgFud9PypcHfgc9hYCAPjNfy3oYuHERMiFT0kTCQNcTNL254/XWHj6HjCvMU6qAoyopjsJ8HS5DtOE9/PRO5YulUjk+NrDmWGbn7leDUMBt/K2towY35DN5YtfaJKIdrEmilkrgBQ/WuGHx0G3NSQk3Y=; lsc=%7B%22Map%22%3A%7B%22BoundingBox%22%3A%7B%22LowerRight%22%3A%7B%22Latitude%22%3A37.44513%2C%22Longitude%22%3A-121.91373%7D%2C%22UpperLeft%22%3A%7B%22Latitude%22%3A37.60687%2C%22Longitude%22%3A-122.09054%7D%7D%7D%2C%22Geography%22%3A%7B%22ID%22%3A%22dn2q6jh%22%2C%22Display%22%3A%22Fremont%2C%20CA%22%2C%22GeographyType%22%3A2%2C%22Address%22%3A%7B%22City%22%3A%22Fremont%22%2C%22State%22%3A%22CA%22%2C%22MarketName%22%3A%22East%20Bay%22%2C%22DMA%22%3A%22San%20Francisco-Oakland-San%20Jose%2C%20CA%22%7D%2C%22Location%22%3A%7B%22Latitude%22%3A37.53%2C%22Longitude%22%3A-122%7D%2C%22BoundingBox%22%3A%7B%22LowerRight%22%3A%7B%22Latitude%22%3A37.45439%2C%22Longitude%22%3A-121.86778%7D%2C%22UpperLeft%22%3A%7B%22Latitude%22%3A37.60462%2C%22Longitude%22%3A-122.13166%7D%7D%2C%22v%22%3A56617%7D%2C%22Listing%22%3A%7B%7D%2C%22Paging%22%3A%7B%22Page%22%3A2%7D%2C%22IsBoundedSearch%22%3Atrue%2C%22ResultSeed%22%3A943059%2C%22Options%22%3A0%7D; _gat=1',
    }
    if pg:
        response = requests.get(f'{link}{pg}/', headers=headers)
        soup = BeautifulSoup(response.text)
        a.extend(unique_list([i['href'] for i in soup.select(".property-link")]))

    else:

        response = requests.get(f'{link}', headers=headers)
        print("Yes")
        soup = BeautifulSoup(response.text)
        a.extend(unique_list([i['href'] for i in soup.select(".property-link")]))
        print(len(a))
        pages = soup.select_one(".pageRange").get_text().lower().replace("page", "").replace("of", "").strip().split()
        print(f"{int(pages[1])+1}")
        pages = [int(pg) + 1 for pg in pages]
        for j in range(pages[0], pages[1]):
            print(len(link_extract(link=link, pg=j, a=a)))
    return a
