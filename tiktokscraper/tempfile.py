# @receiver(request_finished)
    # def save_stats_data(self, context):
    #     headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
    #     user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0"
    #     url_user_agent = urllib.parse.quote_plus(user_agent)
    #     data = request.data
    #     url = f'https://t.tiktok.com/api/challenge/detail/?challengeName={hashtag_name}&aid=1988&app_name=tiktok_web&device_platform=web&referer=&user_agent={url_user_agent}&cookie_enabled=true&screen_width=1920&screen_height=1080&browser_language=en-US&browser_platform=Linux+x86_64&browser_name=Mozilla&browser_version=5.0+(X11)&browser_online=true&timezone_name=Asia/Kolkata&priority_region=IN&appId=1180&region=IN&appType=t&isAndroid=false&isMobile=false&isIOS=false&OS=linux&tt-web-region=IN&language=en&verifyFp=verify_l35llr00_RmnNX2Ia_2uc9_4gf0_99xk_1wwY7cWXcNwY'
    #     get_request = requests.get(url, headers=headers, params=None)
    #     response_json = get_request.json()




# def create(self, request, *args, **kwargs):
#
#     hashtag_name = request.data.get('hashtag_name')
#     if hashtag_name:
#
#         if response_json != '':
#             serializer = HashtagSerializer(data=data)
#             if serializer.is_valid():
#                 serializer.save()
#                 hashtagmodel_id = serializer.data['id']
#             else:
#                 return Response({
#                     'success': False,
#                     'error': serializer.errors
#                 }, status=status.HTTP_406_NOT_ACCEPTABLE)
#         else:
#             return Response({
#                 'success': False,
#                 'message': 'Data not found'
#             }, status=status.HTTP_404_NOT_FOUND)
#         all_data = {'hashtag_name': hashtagmodel_id,
#                     'hashtag_id': response_json['challengeInfo']['challenge']['id'],
#                     'is_commerce': response_json['challengeInfo']['challenge']['isCommerce'],
#                     'video_count': response_json['challengeInfo']['stats']['videoCount'],
#                     'view_count': response_json['challengeInfo']['stats']['viewCount']}
#
#         if all_data is not None:
#             stats_serializer = StatsDataSerializer(data=all_data)
#             if stats_serializer.is_valid():
#                 stats_serializer.save()
#                 return Response({
#                     'success': True,
#                     'message': 'Data saved'
#                 }, status=status.HTTP_201_CREATED)
#             else:
#                 Hashtag.objects.filter(id=hashtagmodel_id).delete()
#                 return Response({
#                     'success': False,
#                     'error': stats_serializer.errors
#                 }, status=status.HTTP_406_NOT_ACCEPTABLE)
#         else:
#             Hashtag.objects.filter(id=hashtagmodel_id).delete()
#             return Response({
#                 'success': False,
#                 'message': 'Data not found'
#             }, status=status.HTTP_404_NOT_FOUND)
#     else:
#         return Response({
#             'success': False,
#             'message': 'Hashtag name not found from request'
#         }, status=status.HTTP_406_NOT_ACCEPTABLE)