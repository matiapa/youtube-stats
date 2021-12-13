from pyyoutube import Api
from math import ceil

CLIENT_ID="635528969546-mtdssianohgaigf9ei8ql0mv37paejaf.apps.googleusercontent.com"
CLIENT_SECRET="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"
REFRESH_TOKEN = '1//0hvdui-Oomm4kCgYIARAAGBESNwF-L9IrLs-MVTDdq2psgOQog0KyPgjxmZkL34f9LY8C2XEKH-nhtezur7ylMgjDYjRyiKjYIz0'

def get_refresh_token():
    CLIENT_ID="635528969546-mtdssianohgaigf9ei8ql0mv37paejaf.apps.googleusercontent.com",
    CLIENT_SECRET="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"

    api = Api(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    print(api.get_authorization_url())

    token = api.refresh_token(REFRESH_TOKEN)
    token.access_token

    # Acá va la URL a la que te redirije el flow de autenticación
    redirect_url= "https://localhost/?state=PyYouTube&code=4/0AX4XfWjhQ80nAkp2wc3Cb8DfqX20u3_Go3ISs8l4f2z2lg_p6BUtudtwKyCqePe2dJBqSA&scope=profile%20https://www.googleapis.com/auth/userinfo.profile%20https://www.googleapis.com/auth/youtube"
    
    token = api.generate_access_token(authorization_response=redirect_url)
    print(token.refresh_token)
    print(token.access_token)

def get_access_token():
    api = Api(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    return api.refresh_token(REFRESH_TOKEN).access_token

ACCESS_TOKEN = get_access_token()


def get_subscriptions():
    api = Api(access_token=ACCESS_TOKEN)
    return api.get_subscription_by_me(mine=True, parts="snippet", count=None)

def get_channels(subs):
    api = Api(access_token=ACCESS_TOKEN)
    channels = []

    ids = list(map(lambda s : s.snippet.resourceId.channelId, subs.items))

    full_channels = []
    for i in range(0, ceil(len(ids)/50)):
        full_channels += api.get_channel_info(channel_id=ids[i*50:(i+1)*50], parts="snippet,topicDetails,brandingSettings").items

    for full_channel in full_channels:
        channel = {}  
        channel['id'] = full_channel.id
        channel['title'] = full_channel.snippet.title
        channel['description'] = full_channel.snippet.description
        channel['keywords'] = full_channel.brandingSettings.channel.keywords

        if full_channel.topicDetails != None:
            topics = full_channel.topicDetails.get_full_topics()
            channel['topics'] = ', '.join(list(map(lambda t : t.description or "", topics)))
        else:
            channel['topics'] = None

        channels.append(channel)

    return channels

def search(keyword):
    subs = get_subscriptions()
    channels = get_channels(subs)

    predicate = lambda c : keyword in c['title'] or keyword in c['description'] \
        or (c['keywords']!=None and keyword in c['keywords']) \
        or (c['topics']!=None and keyword in c['topics'])
    return list(filter(predicate, channels))

search('DIY')