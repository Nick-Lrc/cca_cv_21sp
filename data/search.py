from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import argparse

'''
This script is based on the YouTube Data API's official search example available
at "https://github.com/youtube/api-samples/blob/master/python/search.py".
An YouTube API key is required. Set the DEVELOPER_KEY below to your own API key.
'''
DEVELOPER_KEY = 'AIzaSyD3OZlvsxw78viWDt4JvykOHV8HdMSPgaA'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def youtube_search(options):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    # Call the search.list method to retrieve results matching the specified query term.
    search_response = youtube.search().list(
        q=options.q,
        part='id,snippet',
        maxResults=options.max_results,
        type=options.type,
        videoDuration=options.video_duration,
        relevanceLanguage=options.relevance_language,
    ).execute()

    # Add each result to the appropriate list, and then display the lists of matching videos
    video_ids = []
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            video_ids.append(search_result['id']['videoId'])
            print(f"{video_ids[-1]}: {search_result['snippet']['title']}")
    return video_ids

def parse_options():
    parser = argparse.ArgumentParser(description='Search YouTube videos about a given topic.')
    parser.add_argument('--q', help='Search term', default='alphago')
    parser.add_argument('--max-results', help='Max results', default=100)
    parser.add_argument('--type', help='Search type', default='video')
    parser.add_argument('--video-duration', help='Video duration', default='short')
    parser.add_argument('--relevance-language', help='Relevance language', default='en')
    return parser.parse_args()

if __name__ == '__main__':
    options = parse_options()
    try:
        print(f'Searching {options.q} videos...')
        print()
        video_ids = youtube_search(options)
        output_file = f'{options.q.lower()}.txt'
        with open(output_file, 'w') as f:
            f.write('\n'.join(video_ids) + '\n')
        print()
        print(f'Saved {len(video_ids)} search results to {output_file}.')
        print('Done.')
    except HttpError as e:
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))
