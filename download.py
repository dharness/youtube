import os
from pprint import pprint

import youtube_dl
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
# Disable OAuthlib's HTTPS verification when running locally.
# *DO NOT* leave this option enabled in production.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


def get_youtube_client():
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"
    API_KEY = "AIzaSyAAfhZDfDRHqHGu7fHsQ-J9hd6ChR2gnjc"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=API_KEY)
    return youtube


def get_playlist_page(youtube, playlist_id, page_token=None):
    args = {
        "part": "contentDetails",
        "playlistId": playlist_id,
    }
    if page_token != None:
        args.update({'pageToken': page_token})
    request = youtube.playlistItems().list(**args)
    response = request.execute()
    return response


def get_all_items_for_playlist(playlist_id):
    youtube = get_youtube_client()
    done = False
    next_page_token = None
    all_items = []
    i = 1
    while done == False:
        print('Fetching page: {i}'.format(i=i))
        i += 1
        playlist_page = get_playlist_page(youtube, playlist_id, page_token=next_page_token)

        next_page_token = playlist_page.get('nextPageToken')
        all_items += playlist_page.get('items', [])
        if next_page_token == None:
            done = True

    return all_items


def extract_video_ids_from_playlist_items(playlist_items):
    video_ids = []
    for playlist_item in playlist_items:
        video_id = playlist_item.get('contentDetails', {}).get('videoId')
        if video_id is not None:
            video_ids.append(video_id)
    return video_ids


def download_video_by_id(video_id):
    with youtube_dl.YoutubeDL({}) as ydl:
        ydl.download([
            'https://www.youtube.com/watch?v={video_id}'.format(video_id=video_id)
        ])


def main():
    with youtube_dl.YoutubeDL({
        'nooverwrites': True,
        'outtmpl': 'downloads/%(title)s.%(ext)s'
    }) as ydl:
        ydl.download([
            'https://www.youtube.com/playlist?list=PLyhDkJDrXPDPSe6_bs3ipZJwsLvVWlOrB'
        ])
    return

    playlist_id = "PLyhDkJDrXPDOonDGtbbtoeN3vFzOj0FiM"
    playlist_items = get_all_items_for_playlist(playlist_id)
    video_ids = extract_video_ids_from_playlist_items(playlist_items)

    for video_id in video_ids:
        download_video_by_id(video_id)


if __name__ == "__main__":
    main()
