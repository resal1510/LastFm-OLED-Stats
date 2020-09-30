API_KEY = 'a592dabf076121a578f5b7be548eeee2'
USER_AGENT = 'Custom user agent'

import requests
import json


### To get the live scrobble track + total of scrobbles
print("Live scrobbling track + number of total scrobbles : \n")

def lastfm_get(payload):
    # define headers and URL
    headers = {'user-agent': USER_AGENT}
    url = 'http://ws.audioscrobbler.com/2.0/'
    # Add API key and format to the payload
    payload['api_key'] = API_KEY
    payload['format'] = 'json'
    payload['user'] = 'resal1510'
    payload['limit'] = 1
    payload['nowplaying'] = 'true'
    response = requests.get(url, headers=headers, params=payload)
    return response

r = lastfm_get({
    'method': 'user.getRecentTracks'
})

def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

jsonData = r.json()
trackName = jsonData["recenttracks"]["track"][0]['name']
artistName = jsonData["recenttracks"]["track"][0]['artist']["#text"]

totalScrobbles = jsonData["recenttracks"]["@attr"]['total']
print(artistName + ' - ' + trackName)
print(totalScrobbles)

#### Top 3 artists
print("\nTop 3 artists for 7days : \n")

def lastfm_get(payload):
    # define headers and URL
    headers = {'user-agent': USER_AGENT}
    url = 'http://ws.audioscrobbler.com/2.0/'
    # Add API key and format to the payload
    payload['api_key'] = API_KEY
    payload['format'] = 'json'
    payload['user'] = 'resal1510'
    payload['limit'] = 3
    payload['period'] = '7day'
    response = requests.get(url, headers=headers, params=payload)
    return response

r2 = lastfm_get({
    'method': 'user.getTopArtists'
})

jsonData2 = r2.json()

i = 0
while i < 3:
    print(str(i+1)+'. ' + jsonData2["topartists"]["artist"][i]['playcount'] + ' Scrobbles -- ' + jsonData2["topartists"]["artist"][i]['name'])
    i += 1

#### Top 3 Tracks
print("\nTop 3 tracks for 7days : \n")

def lastfm_get(payload):
    # define headers and URL
    headers = {'user-agent': USER_AGENT}
    url = 'http://ws.audioscrobbler.com/2.0/'
    # Add API key and format to the payload
    payload['api_key'] = API_KEY
    payload['format'] = 'json'
    payload['user'] = 'resal1510'
    payload['limit'] = 3
    payload['period'] = '7day'
    response = requests.get(url, headers=headers, params=payload)
    return response

r3 = lastfm_get({
    'method': 'user.getTopTracks'
})

jsonData3 = r3.json()



i = 0
while i < 3:
    print(str(i+1)+'. ' + jsonData3["toptracks"]["track"][i]['playcount'] + ' Scrobbles -- ' + jsonData3["toptracks"]["track"][i]['artist']['name'] + ' - ' + jsonData3["toptracks"]["track"][i]['name'])
    i += 1
