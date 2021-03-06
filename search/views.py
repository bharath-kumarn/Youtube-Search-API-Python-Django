import requests

from isodate import parse_duration
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render, redirect
from . models import Favourites
from django.http import HttpResponseRedirect
from django.urls import reverse


def index(request):
    videos = []

    if request.method == 'POST':
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'

        search_params = {
            'part' : 'snippet',
            'q' : request.POST['search'],
            'key' : settings.YOUTUBE_DATA_API_KEY,
            'maxResults' : 21,
            'type' : 'video'
        }

        r = requests.get(search_url, params=search_params)

        results = r.json()['items']

        video_ids = []
        for result in results:
            video_ids.append(result['id']['videoId'])

        if request.POST['submit'] == 'fav':
            print("im in fav_list")
            context = {
            'videos' : Favourites.objects.all().order_by('-id')
            }
            return render(request, 'search/favouriteslist.html', context)


        video_params = {
            'key' : settings.YOUTUBE_DATA_API_KEY,
            'part' : 'snippet,contentDetails',
            'id' : ','.join(video_ids),
            'maxResults' : 9
        }

        r = requests.get(video_url, params=video_params)

        results = r.json()['items']

        
        for result in results:
            video_data = {
                'title' : result['snippet']['title'],
                'id' : result['id'],
                'url' : f'https://www.youtube.com/watch?v={ result["id"] }',
                'duration' : int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
                'thumbnail' : result['snippet']['thumbnails']['high']['url']
            }

            videos.append(video_data)

    context = {
        'videos' : videos
    }
    return render(request, 'search/index.html', context)


def favourites_save(request):
    youtube_link=request.GET.get('yt_link')
    youtube_title=request.GET.get('yt_value')
    title_exists=Favourites.objects.filter(title=youtube_title)
    if not title_exists:
        Favourites.objects.create(title=youtube_title,yt_link=youtube_link)
    return HttpResponse('saved')

def delete(request):
    youtube_link=request.GET.get('yt_link')
    Favourites.objects.filter(yt_link=youtube_link).delete()
    return HttpResponse('deleted')
