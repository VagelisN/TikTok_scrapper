from TikTokApi import TikTokApi

from datetime import datetime
from collections import Counter

from moviepy.editor import *

import os
from os.path import isfile, join


# given a list of video ids this function downloads the videos to the specified path
# named out0.mp4, out1.mp4 ... 
def download_videos_by_id(videos, path_to_save):

    print(videos)
    # create the folder
    if not os.path.exists(path_to_save):
        os.makedirs(path_to_save)

    # get the video data in a byte array
    video_data = [video.bytes() for video in videos]

    # save the video in a file
    for index,video in enumerate(video_data):
        with open(path_to_save + "/out" + str(index) + ".mp4", "wb") as out_file:
            out_file.write(video)



# function that takes all the videos in @input_dir and concatenates them into a single video
def concatenate_videos_in_folder(input_dir, output_file_path):

    clip_files = [join(input_dir, f) for f in os.listdir(input_dir) if isfile(join(input_dir, f))]
    clips = [VideoFileClip(c) for c in clip_files]

    #resize videos
    #height = 30
    #width = 30
    #clips = [c.resize(newsize=(width, height)) for c in clips]

    final = concatenate_videoclips(clips, method="compose")
    final.write_videofile(output_file_path)


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
    my_count = 0
    for video in api.search.videos(search_term=search_term, count=300, cursor=unix_timestamp):
        my_count = my_count + 1
        if my_count % 100 == 0:
            print("perasa ta", my_count)
        for hashtag in video.hashtags:
            if "challenge" in hashtag.name:
                hashtag_dict[hashtag.name] = hashtag_dict.get(hashtag.name, 0) + 1

    return Counter(hashtag_dict).most_common(hashtag_count)

def searchHashtags(name, numOfResults):
    return list(api.hashtag(name = name).videos(count= numOfResults))


with TikTokApi(custom_verify_fp=verifyFP) as api:

    top_hashtags = get_popular_related_hashtags("challenge", 75, "01/01/20 00:00:00")
    print(top_hashtags)

    random_challenge_videos = searchHashtags(top_hashtags[5][0], 100)
    sorted_list = sorted(random_challenge_videos, reverse=True, key=lambda x: x.as_dict["stats"]["playCount"])

    download_videos_by_id(sorted_list[0:5], "./videos")
    concatenate_videos_in_folder("./videos", "final.mp4")
    


    

    






