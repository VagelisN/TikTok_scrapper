from TikTokApi import TikTokApi

from datetime import datetime
from collections import Counter


verifyFP = 'verify_l1s2fq4x_yAdRDjgs_YaKZ_4hSE_8eNO_U0DaIqqnY8gp'


'''
searches for videos using @search_term  that were published after @since 
and extracts the most used @hashtag_count hashtags. 
'''
def get_popular_related_hashtags(search_term, hashtag_count, since):

    date_time_obj = datetime.strptime(since, "%d/%m/%y %H:%M:%S")
    unix_timestamp = datetime.timestamp(date_time_obj)

    print ("Finding most used hashtags for the term:", search_term , "since:", since)

    hashtag_dict = dict()
    for video in api.search.videos(search_term=search_term, count=1000000, cursor=unix_timestamp):
        for hashtag in video.hashtags:
            hashtag_dict[hashtag.name] = hashtag_dict.get(hashtag.name, 0) + 1

    return Counter(hashtag_dict).most_common(hashtag_count)


with TikTokApi(custom_verify_fp=verifyFP) as api:
    top_hashtags = get_popular_related_hashtags("new trend", 35, "01/04/22 00:00:00")
    print(top_hashtags)

    






