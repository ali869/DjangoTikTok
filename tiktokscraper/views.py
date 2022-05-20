from django.shortcuts import render
from .models import Hashtag, StatsData
from rest_framework import viewsets
from .serializers import HashtagSerializer, StatsDataSerializer
import requests
import urllib.parse
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import requires_csrf_token


# Create your views here.

@requires_csrf_token
def home(request):
    all_scraped_data = Hashtag.objects.filter(is_saved=True).values()
    all_unscraped_data = Hashtag.objects.filter(is_saved=False).values()
    template = loader.get_template("add_hashtag.html")
    context = {
        "scraped_data": all_scraped_data,
        "unscraped_data": all_unscraped_data
    }
    return HttpResponse(template.render(context, request))


class TikTokScraperView(viewsets.ModelViewSet):
    serializer_class = HashtagSerializer

    def create(self, request, *args, **kwargs):
        hashtag = request.data.get('hashtag_name')
        if type(hashtag) is str:
            if hashtag is not None:
                check_already = Hashtag.objects.filter(hashtag_name=hashtag)
                if check_already:
                    all_scraped_data = Hashtag.objects.filter(is_saved=True).values()
                    all_unscraped_data = Hashtag.objects.filter(is_saved=False).values()
                    template = loader.get_template("add_hashtag.html")
                    context = {
                        "scraped_data": all_scraped_data,
                        "unscraped_data": all_unscraped_data,
                        "already_flag": True
                    }
                    return HttpResponse(template.render(context, request))
                else:
                    headers = {
                        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
                    user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0"
                    url_user_agent = urllib.parse.quote_plus(user_agent)
                    url = f'https://t.tiktok.com/api/challenge/detail/?challengeName={hashtag}&aid=1988&app_name=tiktok_web&device_platform=web&referer=&user_agent={url_user_agent}&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=en-US&browser_platform=Linux+x86_64&browser_name=Mozilla&browser_version=5.0+(X11)&browser_online=true&timezone_name=Asia/Kolkata&priority_region=IN&appId=1180&region=IN&appType=t&isAndroid=false&isMobile=false&isIOS=false&OS=linux&tt-web-region=IN&language=en&verifyFp=verify_l35llr00_RmnNX2Ia_2uc9_4gf0_99xk_1wwY7cWXcNwY'
                    get_request = requests.get(url, headers=headers, params=None)
                    response_json = get_request.json()
                    check_response = response_json.get('challengeInfo')
                    if check_response is not None:
                        request.data._mutable = True
                        request.data['is_valid_hashtag'] = True
                        request.data._mutable = False
                    else:
                        request.data._mutable = True
                        request.data['is_valid_hashtag'] = False
                        request.data._mutable = False
                    serilaizer_response = HashtagSerializer(data=request.data)
                    if serilaizer_response.is_valid():
                        serilaizer_response.save()
                        all_scraped_data = Hashtag.objects.filter(is_saved=True).values()
                        all_unscraped_data = Hashtag.objects.filter(is_saved=False).values()
                        template = loader.get_template("add_hashtag.html")
                        context = {
                            "scraped_data": all_scraped_data,
                            "unscraped_data": all_unscraped_data,
                            "data_saved": True
                        }
                        return HttpResponse(template.render(context, request))
                    all_scraped_data = Hashtag.objects.filter(is_saved=True).values()
                    all_unscraped_data = Hashtag.objects.filter(is_saved=False).values()
                    template = loader.get_template("add_hashtag.html")
                    context = {
                        "scraped_data": all_scraped_data,
                        "unscraped_data": all_unscraped_data,
                        "hashtag_found": False
                    }
                    return HttpResponse(template.render(context, request))
            all_scraped_data = Hashtag.objects.filter(is_saved=True).values()
            all_unscraped_data = Hashtag.objects.filter(is_saved=False).values()
            template = loader.get_template("add_hashtag.html")
            context = {
                "scraped_data": all_scraped_data,
                "unscraped_data": all_unscraped_data,
                "hashtag_found": False
            }
            return HttpResponse(template.render(context, request))
        elif type(hashtag) is list:
            hashtag_str = hashtag[0]
            hashtag_list = hashtag_str.split(',')
            already_hashtag_list = []
            saved_hashtags = []
            for i in hashtag_list:
                check_already = Hashtag.objects.filter(hashtag_name=i)
                if check_already.exists() is False:
                    serilaizer_response = HashtagSerializer(data={"hashtag_name": i})
                    if serilaizer_response.is_valid():
                        serilaizer_response.save()
                        saved_hashtags.append(i)
                else:
                    already_hashtag_list.append(i)
            all_scraped_data = Hashtag.objects.filter(is_saved=True).values()
            all_unscraped_data = Hashtag.objects.filter(is_saved=False).values()
            template = loader.get_template("add_hashtag.html")
            context = {
                "scraped_data": all_scraped_data,
                "unscraped_data": all_unscraped_data
            }
            return HttpResponse(template.render(context, request))

    def list(self, request, *args, **kwargs):
        all_data = StatsData.objects.all().values()
        context = {
            "all_objects_data": all_data
        }
        template_name = "get_data.html"
        return render(request, template_name, context)

    def save_stats_data(self, request):
        get_all_hashtags = Hashtag.objects.values()
        if get_all_hashtags.exists():
            for i in get_all_hashtags:
                hashtag = i['hashtag_name']
                hashtagmodel_id = i['id']
                headers = {
                    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
                user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0"
                url_user_agent = urllib.parse.quote_plus(user_agent)
                url = f'https://t.tiktok.com/api/challenge/detail/?challengeName={hashtag}&aid=1988&app_name=tiktok_web&device_platform=web&referer=&user_agent={url_user_agent}&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=en-US&browser_platform=Linux+x86_64&browser_name=Mozilla&browser_version=5.0+(X11)&browser_online=true&timezone_name=Asia/Kolkata&priority_region=IN&appId=1180&region=IN&appType=t&isAndroid=false&isMobile=false&isIOS=false&OS=linux&tt-web-region=IN&language=en&verifyFp=verify_l35llr00_RmnNX2Ia_2uc9_4gf0_99xk_1wwY7cWXcNwY'
                get_request = requests.get(url, headers=headers, params=None)
                response_json = get_request.json()
                check_response = response_json.get('challengeInfo')
                if check_response is None:
                    continue
                all_data = {'hashtag_name': hashtagmodel_id,
                            'hashtag_id': response_json['challengeInfo']['challenge']['id'],
                            'is_commerce': response_json['challengeInfo']['challenge']['isCommerce'],
                            'video_count': response_json['challengeInfo']['stats']['videoCount'],
                            'view_count': response_json['challengeInfo']['stats']['viewCount']}
                if all_data is not None:
                    check_already_hashtag_stats_data = StatsData.objects.filter(hashtag_name=hashtagmodel_id).first()
                    if check_already_hashtag_stats_data is not None:
                        check_already_hashtag_stats_data.hashtag_id = all_data['hashtag_id']
                        check_already_hashtag_stats_data.is_commerce = all_data['is_commerce']
                        check_already_hashtag_stats_data.video_count = all_data['video_count']
                        check_already_hashtag_stats_data.view_count = all_data['view_count']
                        check_already_hashtag_stats_data.save()
                    else:
                        is_saved_data = Hashtag.objects.filter(id=hashtagmodel_id).first()
                        is_saved_data.is_saved = True
                        is_saved_data.save()
                        stats_serializer = StatsDataSerializer(data=all_data)
                        if stats_serializer.is_valid():
                            stats_serializer.save()
            all_scraped_data = Hashtag.objects.filter(is_saved=True).values()
            all_unscraped_data = Hashtag.objects.filter(is_saved=False).values()
            template = loader.get_template("add_hashtag.html")
            context = {
                "scraped_data": all_scraped_data,
                "unscraped_data": all_unscraped_data,
                "scraped_flag": True
            }
            return HttpResponse(template.render(context, request))
        else:
            all_scraped_data = Hashtag.objects.filter(is_saved=True).values()
            all_unscraped_data = Hashtag.objects.filter(is_saved=False).values()
            template = loader.get_template("add_hashtag.html")
            context = {
                "scraped_data": all_scraped_data,
                "unscraped_data": all_unscraped_data,
                "scraped_flag": False
            }
            return HttpResponse(template.render(context, request))

    def get_stats_data(self, request):
        object_id = request.GET['req_id']
        get_data = StatsData.objects.filter(hashtag_name=object_id)
        context = {
            'data': get_data
        }
        template = loader.get_template("show_stats_data.html")
        return HttpResponse(template.render(context, request))
