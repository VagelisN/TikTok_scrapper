from TikTokApi import TikTokApi
from moviepy.editor import *

import os
from os.path import isfile, join


# given a list of video ids this function downloads the videos to the specified path
# named out0.mp4, out1.mp4 ... 
def download_videos_by_id(video_ids, path_to_save):

    # create the folder
    if not os.path.exists(path_to_save):
        os.makedirs(path_to_save)

    # get the video info
    videos = [api.video(id=video_id) for video_id in video_ids]

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




# MAIN
api = TikTokApi()

with TikTokApi() as api:

    download_videos_by_id(["7076804347316735238", "7041997751718137094"], "./videos")

    concatenate_videos_in_folder("./videos", "final.mp4")


