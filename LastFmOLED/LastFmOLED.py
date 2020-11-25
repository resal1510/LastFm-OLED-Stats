#!/usr/bin/env python
from __future__ import unicode_literals
import os
import requests
import json
import time
from datetime import datetime
from demo_opts import get_device
from luma.core.render import canvas
from PIL import ImageFont

############################################################
#
#Change this to adapt the script for YOUR account :
#
#Put your API KEY here
#You can generate an API KEY by following this link : https://www.last.fm/api/account/create
API_KEY = 'a592dabf076121a578f5b7be548eeee2'
#Just put your Last.fm username here (Or the username of a friend, yours isn't mandatory)
USERNAME = 'resal1510'
#You can also change the UserAgent used to do the request. It's optional, it works like this
USER_AGENT = 'Custom user agent'
#You can change the time interval between itterations of "displays" (In seconds)
INTERVAL = 3
#
############################################################

#Set i var for later use
i = 0
now = datetime.now()
current_time = now.strftime("%H:%M:%S")

def stats(device):
    #Set custom fonts
    font_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'fonts', 'RobotoCondensed-Bold.ttf'))
    #Multiple font size, for different texts on screen
    font1 = ImageFont.truetype(font_path, 14)
    font2 = ImageFont.truetype(font_path, 17)
    font3 = ImageFont.truetype(font_path, 21)

    #Create the payload that will ask the API
    def lastfm_get(payload):
        #Define headers and user agent
        headers = {'user-agent': USER_AGENT}
        url = 'http://ws.audioscrobbler.com/2.0/'
        payload['api_key'] = API_KEY
        payload['format'] = 'json'
        payload['user'] = USERNAME
        payload['limit'] = 1
        payload['nowplaying'] = 'true'
        response = requests.get(url, headers=headers, params=payload)
        return response

    #Try/Except for getting API response. Using the Last.fm parameter "user.getRecentTracks"
    try:
        r = lastfm_get({
            'method': 'user.getRecentTracks'
        })
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print("API CALL FAILED")
        print(e)
        raise SystemExit(e)

    #Creating a formatted string of the Last.fm JSON answer
    def jprint(obj):
        text = json.dumps(obj, sort_keys=True, indent=4)
        print(text)

    jsonData = r.json()
    checkError =  "error" in jsonData

    #Check if the answer from Last.fm is an error or not (To prevent crashing the whole script)
    if checkError:
        print("Error with the API, skipping the current step")
    else:
        #Construct needed variables with json data
        trackName = jsonData["recenttracks"]["track"][0]['name']
        artistName = jsonData["recenttracks"]["track"][0]['artist']["#text"]
        finalStr = (str(artistName) + ' - ' + str(trackName))
        onlyTrack = str(trackName)
        onlyArtist = str(artistName)

        #Check if the user is currently listening to something or not
        #The first "display" will change later on the script
        try:
            isLiveJ = jsonData["recenttracks"]["track"][0]['@attr']
            print(isLiveJ)
            isLive = "true"
        except KeyError:
            print("Oops! Not scrobbling right now")
            totalScrobble = jsonData["recenttracks"]["@attr"]['total']
            isLive = "false"

        #New canvas to be able to draw on the OLED screen
        with canvas(device) as draw:
            global i
            #To have 4 itterations (4 x ** seconds) with this "display"
            if i < 4:
                if isLive == 'true':
                    #If it's live -> Draw hour, "Live !" message, and the current song title
                    draw.text((24, 0), current_time, font=font3, fill="white")
                    draw.text((44, 18), "LIVE !", font=font2, fill="white")
                    draw.text((0, 45), onlyArtist[:12], font=font3, fill="white")
                    draw.text((0, 63), onlyArtist[12:], font=font3, fill="white")
                    draw.text((0, 89), onlyTrack[:12], font=font3, fill="white")
                    draw.text((0, 107), onlyTrack[12:], font=font3, fill="white")
                else:
                    #If it's not live -> "Offline" message and the total number of scrobbles of the user
                    draw.text((37, 20), "Offline...", font=font2, fill="white")
                    draw.text((37, 70), totalScrobble, font=font3, fill="white")
            #To have 2 itterations (4 x ** seconds) with this "display" (See var "INTERVAL" at the start of script)
            elif i < 6:
                #Change the payload (modify an header) to get Top artists 7 days
                def lastfm_get(payload):
                    #Define headers and user agent
                    headers = {'user-agent': USER_AGENT}
                    url = 'http://ws.audioscrobbler.com/2.0/'
                    payload['api_key'] = API_KEY
                    payload['format'] = 'json'
                    payload['user'] = USERNAME
                    payload['limit'] = 3
                    payload['period'] = '7day'
                    response = requests.get(url, headers=headers, params=payload)
                    return response

                #Try/Except for getting API response. Using the Last.fm parameter "user.getTopArtists"
                try:
                    r2 = lastfm_get({
                        'method': 'user.getTopArtists'
                    })
                except requests.exceptions.RequestException as e:  # This is the correct syntax
                    print("API CALL FAILED")
                    raise SystemExit(e)

                jsonData2 = r2.json()
                checkError =  "error" in jsonData2

                #Check if the answer from Last.fm is an error or not (To prevent crashing the whole script)
                if checkError:
                    print("Error with the API, skipping the current step")
                else:
                    ##List top 3 of "Top Artists 7days"
                    draw.text((10, 0), "Top Artists 7days", font=font1, fill="white")
                    n = 0
                    nPx = 25
                    nPx2 = 42
                    #List only 3 tracks (because the screen is little, we can add more itterations)
                    while n < 3:
                        topArtFinal = str(n+1)+'. ' + jsonData2["topartists"]["artist"][n]['playcount'] + ' Scrobbles'
                        topArtFinal2 = jsonData2["topartists"]["artist"][n]['name']
                        draw.text((0, nPx), topArtFinal, font=font2, fill="white")
                        draw.text((0, nPx2), topArtFinal2, font=font1, fill="white")
                        n += 1
                        nPx += 35
                        nPx2 += 35

            elif i < 8:
                #Change the payload (modify an header) to get Top tracks 7 days
                def lastfm_get(payload):
                    #Define headers and user agent
                    headers = {'user-agent': USER_AGENT}
                    url = 'http://ws.audioscrobbler.com/2.0/'
                    payload['api_key'] = API_KEY
                    payload['format'] = 'json'
                    payload['user'] = USERNAME
                    payload['limit'] = 3
                    payload['period'] = '7day'
                    response = requests.get(url, headers=headers, params=payload)
                    return response

                #Try/Except for getting API response. Using the Last.fm parameter "user.getTopTracks"
                try:
                    r3 = lastfm_get({
                        'method': 'user.getTopTracks'
                    })
                except requests.exceptions.RequestException as e:  # This is the correct syntax
                    print("API CALL FAILED")
                    raise SystemExit(e)

                jsonData3 = r3.json()
                checkError =  "error" in jsonData3
                
                #Check if the answer from Last.fm is an error or not (To prevent crashing the whole script)
                if checkError:
                    print("Error with the API, skipping the current step")
                else:
                    #List top 3 of "Top Track 7days"
                    draw.text((10, 0), "Top Track 7days", font=font1, fill="white")
                    n = 0
                    nPx = 25
                    nPx2 = 42
                    #List only 3 tracks (because the screen is little, we can add more itterations)
                    while n < 3:
                        topTrackFinal = str(n+1)+'. ' + jsonData3["toptracks"]["track"][n]['playcount'] + ' Scrobbles'
                        topTrackFinal2 = jsonData3["toptracks"]["track"][n]['artist']['name'] + ' - ' + jsonData3["toptracks"]["track"][n]['name']
                        draw.text((0, nPx), topTrackFinal, font=font2, fill="white")
                        draw.text((0, nPx2), topTrackFinal2, font=font1, fill="white")
                        n += 1
                        nPx += 35
                        nPx2 += 35
                    #If i == 7 (if the "loop" of "display" has finished, come back to the beggining)
                    if i == 7:
                        i = 0

#I don't really know what the fuck this is but it doesn't work without
def main():
    global i
    while True:
        stats(device)
        print(i)
        i +=1
        #Set the time between two "itterations" of displays
        time.sleep(INTERVAL)

if __name__ == "__main__":
    try:
        device = get_device()
        main()
    except KeyboardInterrupt:
        pass
