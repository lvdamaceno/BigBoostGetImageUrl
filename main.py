import requests
import variables as v
from datetime import datetime


def get_json(ean):
    url = "https://plataforma.bigdatacorp.com.br/produtos"
    payload = {
        "q": f"ean{{{ean}}}",
        "Datasets": "images_data"
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "AccessToken": v.AccessToken,
        "TokenId": v.TokenId
    }

    response = requests.post(url, json=payload, headers=headers)
    response_json = response.json()
    return response_json


def get_sources(json):
    images_per_source = json['Result'][0]['ImagesData']['ImagesPerSource']
    sources = []
    for source in images_per_source:
        sources.append(source)
    return sources


def max_date(json, source):
    dates = json['Result'][0]['ImagesData']['ImagesPerSource'][source]["ImagesDetailsHistory"]
    dates_list = []
    for date in dates:
        dates_list.append(date.split()[0])
    max_date = max(dates_list, key=lambda d: datetime.strptime(d, '%m/%d/%Y'))
    for d in dates:
        if d.split()[0] == max_date:
            return d


def get_url_list(json, source, date):
    image_data = json['Result'][0]['ImagesData']['ImagesPerSource'][source]['ImagesDetailsHistory'][date]
    image_list = []
    for image in image_data:
        image_list.append(image['ImageUrl'])
    return image_list


def most_recent(json):
    sources = get_sources(json)
    source_list = []
    for source in sources:
        source_list.append([source, max_date(json, source)])
    dates_list = []
    for data in source_list:
        dates_list.append(data[1].split()[0])
        max_date_source = max(dates_list, key=lambda d: datetime.strptime(d, '%m/%d/%Y'))
        for s in source_list:
            if s[1].split()[0] == max_date_source:
                return s


if __name__ == '__main__':
    eans = [
        7890724094675,7891129180567,7891129195448,7894121084567,7894855221139,7894855221436,7894855231794,7894855232098,
        7895500757225,7895500761130,7896525011095,7896525098461,7897016837552,7897016837569,7897016838603,7897016838627,
        7897180505134,7897180505387,7897180505394,7897747481451,7898148439584,7898187040147,7898187040611,7898187047368,
        7898457175722,7898543573548,7898554875884,7898574580003,7898574582236,7898574582854,7898574582892,7898574586661,
        7898574588061,7898574588283,7898574588320,7898574589402,7898574589983,7898574589990,7898580990018,7898580990025,
        7898604856313,7898604857112,7898604857129,7898604857358,7898604857839,7898604858065,7898604858928,7898658868560,
        7899081732268,7899081743271,7899180444864,7899370094589,7899376425219,7899376425509,7899639700831,7899665057602,
        7899676622653,7899676630283,7899766207388,7899766207456,7899766207470,7899766207500,7899766207524,7899766209504,
        7899766209559,7899913407500,7899913408620,7899913408866,7899913411385,7899959601399,7908042217383,7908184602467,
        7908460003339,7908547700014,7909192118285,7909192330724,7909192368604,7909373111647,7909373111685,7909373111845,
        7909875022229,7909875030590,8710103900405
        ]
    for ean in eans:
        json = get_json(ean)

        if json['Result'] != []:
            recent = most_recent(json)
            print(ean, get_url_list(json, recent[0], recent[1]))
        else:
            print(ean, 'Sem imagens')



