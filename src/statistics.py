import json
import requests
import urllib.parse
import isodate
import functools
import src.utils as utils
import operator
from os import path

parts = "snippet,contentDetails,statistics,topicDetails"
fields = "items(snippet/categoryId,contentDetails/duration,topicDetails,statistics,recordingDetails/location(latitude,longitude))"
apiKey = "AIzaSyAa8yy0GdcGPHdtD083HiGGx_S0vMPScDM"

def getVideosMetadata():

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

        url = f"https://content-youtube.googleapis.com/youtube/v3/videos"
        url += f"?part={urllib.parse.quote(parts)}"
        url += f"&fields={urllib.parse.quote(fields)}"
        url += f"&id={urllib.parse.quote(','.join(ids[i:i+39]))}"
        url += f"&key={apiKey}"

        r = requests.get(
            url,
            headers={"x-origin": "https://explorer.apis.google.com"}
        )

        items += r.json()["items"]

        utils.printProgressBar(i, len(ids))

    f = open("in/videos_metadata.json", "w")
    f.write(json.dumps(items))
    f.close()


def processMetadata(s):
    if not path.exists("in/videos_metadata.json"):
        getVideosMetadata()

    f = open("in/videos_metadata.json", "r", encoding='utf8')
    videosMetadata = json.loads(f.read())
    f.close()

    # Process durations

    durationsTD = utils.safe_map(lambda j : isodate.parse_duration(j["contentDetails"]["duration"]), videosMetadata)
    durationsMin = list(map(lambda d : round(d.total_seconds() / 60), durationsTD))    
    durationsMin = list(filter(lambda d : d < 60, durationsMin))
    durationsMin = sorted(durationsMin, reverse=True)

    utils.hist_plot(data=durationsMin, bins=10, filename="durations_histogram")

    daysSpent = round(functools.reduce(lambda x,y : x+y, durationsMin) / (24*60))
    s.write(f"Days spent on Youtube: {daysSpent}\n")

    # Process views and likes

    views = utils.safe_map(lambda j : int(j["statistics"]["viewCount"]), videosMetadata)
    utils.hist_plot(data=views, bins=10, filename="views_histogram", xscale="log")

    likeRatio = utils.safe_map(lambda j : 
        round(100 * int(j["statistics"]["likeCount"]) 
            / (int(j["statistics"]["likeCount"]) + int(j["statistics"]["dislikeCount"]))),
        videosMetadata
    )
    utils.hist_plot(data=likeRatio, bins=10, filename="like_ratio_histogram")

    # Process YouTube categories

    catIds = utils.safe_map(lambda j : int(j["snippet"]["categoryId"]), videosMetadata)
    viewsByCatId = {i : catIds.count(i) for i in catIds}
    viewsByCatId = dict(sorted(viewsByCatId.items(), key=operator.itemgetter(1), reverse=True))
    
    url = f"https://content-youtube.googleapis.com/youtube/v3/videoCategories"
    url += f"?id={urllib.parse.quote(','.join(str(k) for k in viewsByCatId.keys()))}"
    url += f"&part=snippet&key={apiKey}"
    items = requests.get(
        url,
        headers={"x-origin": "https://explorer.apis.google.com"}
    ).json()["items"]

    namesByCatId = {j["id"] : j["snippet"]["title"] for j in items}
    viewByCatName = {namesByCatId[str(i[0])] : i[1] for i in viewsByCatId.items()}
    utils.dump_dict(dict=viewByCatName, filename="top_categories")

    # Process Wikipedia categories

    wkCatIds = utils.safe_map(lambda j : j["topicDetails"]["topicCategories"][0].split('wiki/')[1], videosMetadata)
    viewsByWkCatId = {i : wkCatIds.count(i) for i in wkCatIds}
    viewsByWkCatId = dict(sorted(viewsByWkCatId.items(), key=operator.itemgetter(1), reverse=True))
    utils.dump_dict(dict=viewsByWkCatId, filename="top_wk_categories")    


def processHistory(s):
    f = open("in/history.json", "r", encoding='utf8')
    history = json.loads(f.read())
    f.close()

    s.write(f"Watched videos: {len(history)}\n")

    datetimes = list(map(lambda j : isodate.parse_datetime(j["time"]), history))
    utils.hist_plot(data=datetimes, bins=round((max(datetimes)-min(datetimes)).days / 30), filename="datetimes_histogram")


print("Generating statistics")
s = open("out/statistics.txt", "w") 

processHistory(s)
processMetadata(s)

s.close()
print("Done!")