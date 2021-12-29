import requests
import cv2
import numpy as np
import urllib

# Heavily based off the Twitter API Example from https://github.com/twitterdev/Twitter-API-v2-sample-code

#REPLACE WITH BEARER TOKEN FROM USER CREATED TWITTER APP
bearer_token = "BEARER TOKEN HERE"

search_url = "https://api.twitter.com/2/tweets/search/recent"


EnDict = {'english': ['moricalliope', 'takanashikiara', 'watsonameliaEN', 'gawrgura', 'ninomaeinanis', 'irys_en',
                      'ceresfauna', 'tsukumosana', 'ourokronii', 'nanashimumei_en', 'hakosbaelz']}

NijEnDict = {'english': ['PomuRainpuff', 'EliraPendora', 'FinanaRyugu', 'Rosemi_Lovelock', 'Petra_Gurin', 'Selen_Tatsuki', 'ReimuEndou', 'MillieParfait', 'NinaKosaka', 'EnnaAlouette', 'luca_kaneshiro', 'ike_eveland', 'Vox_Akuma'
, 'shu_yamino', 'Mysta_Rias']}

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def url_to_image(url):
    resp = urllib.request.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image


def importer(nij):
    for liver in EnDict['english']:

        query_params = {'query': '(from:' + liver + '(schedule OR calendar OR ᴘɪɴ) has:media -is:retweet)',
                        'expansions': 'attachments.media_keys', 'media.fields': 'url'}

        json_response = connect_to_endpoint(search_url, query_params)
        print(json_response)

        if json_response.__contains__('includes'):
            url = json_response['includes']['media'][0]['url']

            img = url_to_image(url)

            cv2.imwrite(liver + '.jpg', img)
        else:
            print('Could not find schedule for ' + liver)

    if nij is True:
        for liver in NijEnDict['english']:
            query_params = {'query': '(from:' + liver + '(schedule OR calendar OR R-🔞 OR live tag OR fan name) has:media -is:retweet)',
                            'expansions': 'attachments.media_keys', 'media.fields': 'url'}

            json_response = connect_to_endpoint(search_url, query_params)
            print(json_response)
            if json_response.__contains__('includes'):
                url = json_response['includes']['media'][0]['url']

                img = url_to_image(url)

                cv2.imwrite(liver + '.jpg', img)
            else:
                print('Could not find schedule for ' + liver)

def main():
    importer(True)

