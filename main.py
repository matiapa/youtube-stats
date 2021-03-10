import json
import requests
import urllib.parse
import isodate
import functools
import matplotlib.pyplot as plt
import utils
from os import path, system

apiKey = "AIzaSyAa8yy0GdcGPHdtD083HiGGx_S0vMPScDM"

def getVideosInfo():

    f = open("in/history.json", "r", encoding='utf8')
    history = json.loads(f.read())
    f.close()

    ids = []
    for video in history:
        if 'titleUrl' in video:
            id = video['titleUrl'].split('=')[1]
            ids.append(id)

    # 25 length of id && 1024 max qs length => 40 ids per query

    items = []
    print("Getting videos metadata")
    for i in range(0, len(ids), 40):

        idValues = urllib.parse.quote(",".join(ids[i:i+39]))
        query = f"part=contentDetails&fields=items%2FcontentDetails%2Fduration&id={idValues}&key={apiKey}"

        r = requests.get(
            f"https://content-youtube.googleapis.com/youtube/v3/videos?{query}",
            headers={"x-origin": "https://explorer.apis.google.com"}
        )

        items += r.json()["items"]

        utils.printProgressBar(i, len(ids))

        # print(f"{i}/{len(ids)}")

    f = open("in/videos_info.json", "a")
    f.write(json.dumps(items))
    f.close()


def processHistory():

    s = open("out/statistics.txt", "w")

    # Process info from history

    f = open("in/history.json", "r", encoding='utf8')
    history = json.loads(f.read())
    f.close()

    datetimes = list(map(lambda j : isodate.parse_datetime(j["time"]), history))
    plt.hist(datetimes, bins=round((max(datetimes)-min(datetimes)).days / 30), histtype='step')
    plt.grid()
    plt.savefig("out/datetimes_histogram.png")

    # Process info from videos info

    if not path.exists("in/videos_info.json"):
        getVideosInfo()

    f = open("in/videos_info.json", "r", encoding='utf8')
    videosInfo = json.loads(f.read())
    f.close()

    durationsTD = list(map(lambda j : isodate.parse_duration(j["contentDetails"]["duration"]), videosInfo))
    durationsMin = list(map(lambda d : round(d.total_seconds() / 60), durationsTD))    
    durationsMin = list(filter(lambda d : d < 60, durationsMin))
    durationsMin = sorted(durationsMin, reverse=True)

    plt.hist(durationsMin, bins=10, histtype='step')
    plt.grid()
    plt.savefig("out/durations_histogram.png")

    daysSpent = round(functools.reduce(lambda x,y : x+y, durationsMin) / (24*60))
    s.write(f"Days spent on Youtube: {daysSpent}")

    s.close()

processHistory()
print("Done!")