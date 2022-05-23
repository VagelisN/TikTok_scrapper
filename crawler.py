from operator import itemgetter
from TikTokApi import TikTokApi
from pymongo import MongoClient
from datetime import datetime
import logging
import requests
import re
import time

baseUrl = 'https://m.tiktok.com/api/search/general/full/?aid=1988&keyword='  
urlOffSet = '&offset='  
urlEnding ='&verifyFp=verify_l3emyvrt_PSFOvW0p_qXtp_4pLk_A5UX_ZHEqtC2aL4jK'

def getPopularChallengeHashtags(name):
    challenges = set()
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "cookie": "tt_csrf_token=9zoLWww6-kVrn_PlYefrdER4pbbYPuDkYHO8; _abck=926D56A097D64962000AF1BFFACFE5C3~-1~YAAQN9+euXp7B46AAQAAzrQ54geBZmIlF+S/nM4RTFgNz935PzuDkh/O4w54MR9sE8ZqNgKwX/4FiuvtaR/Km9GeiBaac7HA+dbiR2by5ftFWDHR+jFd5btRwKEKgk8vArq7Q+McmgTpsMkJPcKK5Q+s7xWUWktv+MVPWtvy+H3kM9nt7TfFurLyiHjkJqckbEN+PnTzsKh0ZCr3B4yLDHwq95lVGYJehV57uPXmb54oyDSFYq94oI9XGnyEAZdWhrGQU9DVKNFx1tJDSVQ8OcN8I0kjg4aS5zZNbW7Ygg0EAVX6BV18XA9QQqS03boJflQDjOUki7mufmzAyK4XbBfYf07r0JsFUfAtjpr6GfrhS4QnQpuNuEGU/tI=~-1~-1~-1; ak_bmsc=9297555ACFB84DAD8EEFD7EA38358571~000000000000000000000000000000~YAAQN9+euXt7B46AAQAAzrQ54g/ro6/+DA4rucLqo37sH1j9/D340CFFbbUvklE/BVLlQpc3XTOkZ0HV6a/i6jul1iQZTkIer8bDp+zsH+GdiRa4IJ0VQk7F2dKXE/EoXKpQ9INmm7+Axwf3AAtYJsmRLMiz0q0hxaTuzcy5/XZQDrAfRgbiU9nn0fuVwo2xE48VCKcnfBzodarwP12urIfmbxRxkhgdws34ZEtrW96DC5Tt1rqv8xu8M6xe+Bf3avzSbJKillSEGnHDx8XAJGbE2n16AjOX5qwS0Ege14RGLQwWmfrLe59faSLO4W4KByxd6oJTx7rfwY2Yb5VZJT/mSIIzYRRk7cD4oB6kefSbLNSMOiQTw7ANCmORenl9aDyK8bX3QORT2mI=; bm_sz=34E36517D9D11CE28FA25D281494F377~YAAQN9+euX17B46AAQAAz7Q54g/ZE8I1jTftGl01ehdCjR3JAKFRa4m1QIjEFK7G6AixsDi/tQtCKcogcZKoy/kn2ZGAwRZP2Sa3xRObGJIRv+xmSa5PjCWv/iuNxIjJXa1hTLVSSrMI8ytbe8KYDdQjxaXvZPomfBbzpfIk37mEihp+fM4hVQWyUl0KooaQu9UgD5jxLGRwYrcZC96FTggo8dked2nbO1OF3Cxu9sS5VL7yRbXQqgWcy00pBJnhn9+rZmDwDxdSvw+ZC8wtgjxQbgodec175STfIWSHim3f34M=~3425347~3618370; s_v_web_id=verify_l3emyvrt_PSFOvW0p_qXtp_4pLk_A5UX_ZHEqtC2aL4jK; cookie-consent={%22ga%22:true%2C%22af%22:true%2C%22fbp%22:true%2C%22lip%22:true%2C%22bing%22:true%2C%22ttads%22:true%2C%22version%22:%22v7%22}; passport_csrf_token=813bb95622884ab3d405af0f4187456d; passport_csrf_token_default=813bb95622884ab3d405af0f4187456d; cmpl_token=AgQQAPOfF-RO0rH6e10N5t0_-OYl8Saaf4QUYMf9vg; sid_guard=52a9fce246af7324cd3b55a6b1a04802%7C1653063027%7C5183999%7CTue%2C+19-Jul-2022+16%3A10%3A26+GMT; uid_tt=af1077ade12abc657628f29dcf3e7b8963793b16d966a6b0f1543c51b00ffac9; uid_tt_ss=af1077ade12abc657628f29dcf3e7b8963793b16d966a6b0f1543c51b00ffac9; sid_tt=52a9fce246af7324cd3b55a6b1a04802; sessionid=52a9fce246af7324cd3b55a6b1a04802; sessionid_ss=52a9fce246af7324cd3b55a6b1a04802; sid_ucp_v1=1.0.0-KDExNGJiZTdlN2Q0ODhmY2YwZThmNWFhYzA4ZTQ1NjM0NDRlNDE3NjMKIAiGiNCuqL-l4mEQ8_qelAYYswsgDDD7rJKOBjgBQOoHEAMaBm1hbGl2YSIgNTJhOWZjZTI0NmFmNzMyNGNkM2I1NWE2YjFhMDQ4MDI; ssid_ucp_v1=1.0.0-KDExNGJiZTdlN2Q0ODhmY2YwZThmNWFhYzA4ZTQ1NjM0NDRlNDE3NjMKIAiGiNCuqL-l4mEQ8_qelAYYswsgDDD7rJKOBjgBQOoHEAMaBm1hbGl2YSIgNTJhOWZjZTI0NmFmNzMyNGNkM2I1NWE2YjFhMDQ4MDI; store-idc=maliva; store-country-code=gr; tt-target-idc=useast1a; bm_mi=4B8E6DDA8A9A84C012B359DFA6CA2733~YAAQF9+euQ91Bo6AAQAAshc84g9sc3qeJYnFpDXx853/lxhEHS8YT+bhGC3GzTRb4ogbYvFRxGh63iRuj/M1ASwLFOFkng9xSnQGWmhWxN1uhxRuQ+s8KqAUcAvV6BnOlI3plF0P6/NweK4V7MKUcFh/Kt8+Ztbron6XG2cf3dtKZBn2hS2Fj/TnE/PoVkqZP62Xv1r8wQpQEXJ4B2gyC/LgbUKKt9ryvR1GQRaCSIQnXsew19OzbwtpAyiACWdL0SjcdqgCXhLg6gLja9sxZ2rbHbXO2gCSeF+FgX1AiHFUyUrOpPbj3DPAmWY0Q8nTzWo7YwMy0iA=~1; bm_sv=828B2EE9DB7F1D961A2276205CBD3131~YAAQF9+euRB1Bo6AAQAAshc84g/7P8Lz/1/fK83yWINPIvifG7w8iwQgsihcPdx0udT1LTQvouprM2vI+Ard0JWZaBaB4Q9ENNFwmxMvsiuYtsKU2K5e7r73yVoUbVpTPRXw013saImP8r7SZMqKcgmFJ/4rTQOClt7b+Ky4NDHTV2+X5+WBnnR3IVmrqsIMAKT/Vbguw1w2iCigfRGDjHI9QgZVUMryz35ABnl2VrwS7S4G/yGg/9aX04f+xVcm~1; ttwid=1%7C8RkzX7fworOLIfHzrxWlnxM0RToUBEzP3szXzoOotLk%7C1653063031%7C57b1a870db0dfe33c418a72735e5a31c07ea8dcafd909fd8ef3050a2c46c3c93; odin_tt=2a0a02a94465414787117d11c0be5e11fa219ec1b68696e6f481f443165f9822b2b15c02dddad46c243bd62f8eb10c6a8668596f4bc1f5e9492039175f1205bd091afc4c44c6bcd776c339959618cf18; msToken=cR635P7VlX8NJsnQJu8mxhxXh6QKPwT1WLRStws2E2oS7PUXwtQ4D-LvmjzESptqMMW-LtV7CyRXs329guaw9bli0VfYJiKcxWW5Jx6WxXqiiSqifAWtZ-e-sbwRpbbX5cEXjgQ="
    }
    offset = 0
    while offset <= 100:
        # %23 is the url encoding of '#'
        response = requests.get(baseUrl + '%23' + name + urlOffSet + str(offset) + urlEnding, headers= headers).json()
        for data in response['data']:
            if 'item' not in data.keys() or 'textExtra' not in data['item']:
                continue
            for challenge in data["item"]["textExtra"]:
                tmp = challenge["hashtagName"]
                tmp = tmp.lower()
                if tmp != 'challenge' and tmp != 'challenges' and 'challenge' in tmp:
                    challenges.add(tmp)
        offset += 12
    return challenges

def getTopVideosForHashtag(name):
    videos = []
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "cookie": "tt_csrf_token=9zoLWww6-kVrn_PlYefrdER4pbbYPuDkYHO8; _abck=926D56A097D64962000AF1BFFACFE5C3~-1~YAAQN9+euXp7B46AAQAAzrQ54geBZmIlF+S/nM4RTFgNz935PzuDkh/O4w54MR9sE8ZqNgKwX/4FiuvtaR/Km9GeiBaac7HA+dbiR2by5ftFWDHR+jFd5btRwKEKgk8vArq7Q+McmgTpsMkJPcKK5Q+s7xWUWktv+MVPWtvy+H3kM9nt7TfFurLyiHjkJqckbEN+PnTzsKh0ZCr3B4yLDHwq95lVGYJehV57uPXmb54oyDSFYq94oI9XGnyEAZdWhrGQU9DVKNFx1tJDSVQ8OcN8I0kjg4aS5zZNbW7Ygg0EAVX6BV18XA9QQqS03boJflQDjOUki7mufmzAyK4XbBfYf07r0JsFUfAtjpr6GfrhS4QnQpuNuEGU/tI=~-1~-1~-1; ak_bmsc=9297555ACFB84DAD8EEFD7EA38358571~000000000000000000000000000000~YAAQN9+euXt7B46AAQAAzrQ54g/ro6/+DA4rucLqo37sH1j9/D340CFFbbUvklE/BVLlQpc3XTOkZ0HV6a/i6jul1iQZTkIer8bDp+zsH+GdiRa4IJ0VQk7F2dKXE/EoXKpQ9INmm7+Axwf3AAtYJsmRLMiz0q0hxaTuzcy5/XZQDrAfRgbiU9nn0fuVwo2xE48VCKcnfBzodarwP12urIfmbxRxkhgdws34ZEtrW96DC5Tt1rqv8xu8M6xe+Bf3avzSbJKillSEGnHDx8XAJGbE2n16AjOX5qwS0Ege14RGLQwWmfrLe59faSLO4W4KByxd6oJTx7rfwY2Yb5VZJT/mSIIzYRRk7cD4oB6kefSbLNSMOiQTw7ANCmORenl9aDyK8bX3QORT2mI=; bm_sz=34E36517D9D11CE28FA25D281494F377~YAAQN9+euX17B46AAQAAz7Q54g/ZE8I1jTftGl01ehdCjR3JAKFRa4m1QIjEFK7G6AixsDi/tQtCKcogcZKoy/kn2ZGAwRZP2Sa3xRObGJIRv+xmSa5PjCWv/iuNxIjJXa1hTLVSSrMI8ytbe8KYDdQjxaXvZPomfBbzpfIk37mEihp+fM4hVQWyUl0KooaQu9UgD5jxLGRwYrcZC96FTggo8dked2nbO1OF3Cxu9sS5VL7yRbXQqgWcy00pBJnhn9+rZmDwDxdSvw+ZC8wtgjxQbgodec175STfIWSHim3f34M=~3425347~3618370; s_v_web_id=verify_l3emyvrt_PSFOvW0p_qXtp_4pLk_A5UX_ZHEqtC2aL4jK; cookie-consent={%22ga%22:true%2C%22af%22:true%2C%22fbp%22:true%2C%22lip%22:true%2C%22bing%22:true%2C%22ttads%22:true%2C%22version%22:%22v7%22}; passport_csrf_token=813bb95622884ab3d405af0f4187456d; passport_csrf_token_default=813bb95622884ab3d405af0f4187456d; cmpl_token=AgQQAPOfF-RO0rH6e10N5t0_-OYl8Saaf4QUYMf9vg; sid_guard=52a9fce246af7324cd3b55a6b1a04802%7C1653063027%7C5183999%7CTue%2C+19-Jul-2022+16%3A10%3A26+GMT; uid_tt=af1077ade12abc657628f29dcf3e7b8963793b16d966a6b0f1543c51b00ffac9; uid_tt_ss=af1077ade12abc657628f29dcf3e7b8963793b16d966a6b0f1543c51b00ffac9; sid_tt=52a9fce246af7324cd3b55a6b1a04802; sessionid=52a9fce246af7324cd3b55a6b1a04802; sessionid_ss=52a9fce246af7324cd3b55a6b1a04802; sid_ucp_v1=1.0.0-KDExNGJiZTdlN2Q0ODhmY2YwZThmNWFhYzA4ZTQ1NjM0NDRlNDE3NjMKIAiGiNCuqL-l4mEQ8_qelAYYswsgDDD7rJKOBjgBQOoHEAMaBm1hbGl2YSIgNTJhOWZjZTI0NmFmNzMyNGNkM2I1NWE2YjFhMDQ4MDI; ssid_ucp_v1=1.0.0-KDExNGJiZTdlN2Q0ODhmY2YwZThmNWFhYzA4ZTQ1NjM0NDRlNDE3NjMKIAiGiNCuqL-l4mEQ8_qelAYYswsgDDD7rJKOBjgBQOoHEAMaBm1hbGl2YSIgNTJhOWZjZTI0NmFmNzMyNGNkM2I1NWE2YjFhMDQ4MDI; store-idc=maliva; store-country-code=gr; tt-target-idc=useast1a; bm_mi=4B8E6DDA8A9A84C012B359DFA6CA2733~YAAQF9+euQ91Bo6AAQAAshc84g9sc3qeJYnFpDXx853/lxhEHS8YT+bhGC3GzTRb4ogbYvFRxGh63iRuj/M1ASwLFOFkng9xSnQGWmhWxN1uhxRuQ+s8KqAUcAvV6BnOlI3plF0P6/NweK4V7MKUcFh/Kt8+Ztbron6XG2cf3dtKZBn2hS2Fj/TnE/PoVkqZP62Xv1r8wQpQEXJ4B2gyC/LgbUKKt9ryvR1GQRaCSIQnXsew19OzbwtpAyiACWdL0SjcdqgCXhLg6gLja9sxZ2rbHbXO2gCSeF+FgX1AiHFUyUrOpPbj3DPAmWY0Q8nTzWo7YwMy0iA=~1; bm_sv=828B2EE9DB7F1D961A2276205CBD3131~YAAQF9+euRB1Bo6AAQAAshc84g/7P8Lz/1/fK83yWINPIvifG7w8iwQgsihcPdx0udT1LTQvouprM2vI+Ard0JWZaBaB4Q9ENNFwmxMvsiuYtsKU2K5e7r73yVoUbVpTPRXw013saImP8r7SZMqKcgmFJ/4rTQOClt7b+Ky4NDHTV2+X5+WBnnR3IVmrqsIMAKT/Vbguw1w2iCigfRGDjHI9QgZVUMryz35ABnl2VrwS7S4G/yGg/9aX04f+xVcm~1; ttwid=1%7C8RkzX7fworOLIfHzrxWlnxM0RToUBEzP3szXzoOotLk%7C1653063031%7C57b1a870db0dfe33c418a72735e5a31c07ea8dcafd909fd8ef3050a2c46c3c93; odin_tt=2a0a02a94465414787117d11c0be5e11fa219ec1b68696e6f481f443165f9822b2b15c02dddad46c243bd62f8eb10c6a8668596f4bc1f5e9492039175f1205bd091afc4c44c6bcd776c339959618cf18; msToken=cR635P7VlX8NJsnQJu8mxhxXh6QKPwT1WLRStws2E2oS7PUXwtQ4D-LvmjzESptqMMW-LtV7CyRXs329guaw9bli0VfYJiKcxWW5Jx6WxXqiiSqifAWtZ-e-sbwRpbbX5cEXjgQ="
    }
    offset = 0
    while offset <= 100:
        response = requests.get(baseUrl + name + urlOffSet + str(offset) + urlEnding, headers= headers).json()
        if 'data' not in response.keys():
            break
        for data in response['data']:
            if 'item' not in data.keys() or 'textExtra' not in data['item']:
                continue
            item = data["item"]
            if True in [True if name == x['hashtagName'] else False  for x in item['textExtra']]:
                pass
            else:
                continue

            id = item['video']['id']
            likes = item['stats']['diggCount']
            shares = item['stats']['shareCount']
            views = item['stats']['playCount']
            video_score = views + 1.6 * likes + 2.2 * shares
            videos.append({"id" : id, "score" : video_score, "likes": likes, "views": views, "shares": shares})  
        offset += 12
    return sorted(videos, key=itemgetter('score'), reverse=True)[:5]

def getVideoFromId( videoId):
    return api.video(id = videoId)

def getUsersVideos(username):
    response = requests.get('https://tiktok.com/@' + username, headers= {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.79 Safari/537.36'}).text
    compileStr = '"user-post"(?:.)*?"browserList"'
    p = re.compile(compileStr, re.DOTALL)
    trimmedResponse = p.search(response).group(0)
    p = re.compile('\d+')
    results = []
    for id in p.findall(trimmedResponse):
        results.append(id)
    return results

def getChallengeHashtagsFromVideo(video):
    results = []
    challenges = video.hashtags
    for challenge in challenges:
        name = challenge.name
        if (name != 'challenge') and (name != 'challenges') and ('challenge' in name):
            results.append(name)
    return results

'''
Returns the challenge, with the 5 most popular videos
'''
def getSumForHashtag(hashtagName):
    if isinstance(hashtagName, list):
        hashtagName = hashtagName[0]
    topVideos = getTopVideosForHashtag(hashtagName)

    totalLikes = sum(i['likes'] for i in topVideos)
    totalShares = sum(i['shares'] for i in topVideos)
    totalViews = sum(i['views'] for i in topVideos)
    totalScore = sum(i['score'] for i in topVideos)
    return {
        "name": hashtagName, 
        "date": datetime.today().replace(hour=0, minute=0, second=0, microsecond=0),
        "likes" : totalLikes, 
        "views": totalViews, 
        "shares": totalShares, 
        "score": totalScore, 
        "videos": topVideos
    }


client = MongoClient("mongodb+srv://TikTokApi:3patates@tiktokcluster.vcf8n.mongodb.net/?retryWrites=true&w=majority")
tikTokDB = client['TikTokDB']
dailyTrendsCollection = tikTokDB['DailyTrends']
hashtags = []
customVerify = "verify_l0h7ncp4_Fd2ZmLZO_WHvz_42pj_8zhK_gyZjJYxzHwf9"
deviceId = 'ac0c4016-b6c1-4f57-ab70-5714df68782c'
with TikTokApi(logging_level=logging.DEBUG, custom_verify_fp= customVerify, generate_static_device_id=True) as api:
    hashtags = getPopularChallengeHashtags('challenge')
    '''
    For each separate hashtag in list, get 100 videos, 
    and keep the top 5 based on the following formula
    VC + LC * 1.6 + SC * 2.2
    '''
    print(hashtags)
    for hashtag in hashtags:
        item = getSumForHashtag(hashtag) 
        print(item)
        dailyTrendsCollection.insert_one(item)