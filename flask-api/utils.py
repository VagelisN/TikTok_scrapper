from TikTokApi import TikTokApi

from datetime import datetime
from collections import Counter

from moviepy.editor import *

import os
from os.path import isfile, join
import shutil

import matplotlib.pyplot as plt
import matplotlib

def makeCompilation(video_ids):
    downloadVideosById(video_ids, "./videos")
    concatenateVideosInFolder("./videos", "./videos/compilation.mp4")
    video_file = open("./videos/compilation.mp4", "rb") # opening for [r]eading as [b]inary
    data = video_file.read() # if you only wanted to read 512 bytes, do .read(512)
    video_file.close()
    #shutil.rmtree("./videos")
    return data


# given a list of video ids this function downloads the videos to the specified path
# named out0.mp4, out1.mp4 ... 
def downloadVideosById(video_ids, path_to_save):

    api = TikTokApi()
    id_list = [api.video(id=id) for id in video_ids]

    # create the folder
    if not os.path.exists(path_to_save):
        os.makedirs(path_to_save)

    # get the video data in a byte array
    video_data = [video.bytes() for video in id_list]

    # save the video in a file
    for index,video in enumerate(video_data):
        with open(path_to_save + "/out" + str(index) + ".mp4", "wb") as out_file:
            out_file.write(video)



# function that takes all the videos in @input_dir and concatenates them into a single video
def concatenateVideosInFolder(input_dir, output_file_path):

    clip_files = [join(input_dir, f) for f in os.listdir(input_dir) if isfile(join(input_dir, f))]
    clips = [VideoFileClip(c) for c in clip_files]

    #resize videos
    #height = 30
    #width = 30
    #clips = [c.resize(newsize=(width, height)) for c in clips]

    final = concatenate_videoclips(clips, method="compose")
    final.write_videofile(output_file_path)

def makePlotAndGetBinary(cursor, hashtag, metric):

    # get axis from pymongo cursor
    x_axis = []
    y_axis = []
    for item in list(cursor):
        x_axis.append(item["date"])
        y_axis.append(item["views"])


    # create plot
    plt.rcParams["figure.figsize"] = (10, 8)
    fig, ax = plt.subplots()

    ax.plot(x_axis, y_axis)
    
    ax.get_yaxis().set_major_formatter(
    matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))



    plt.xticks(x_axis)
    plt.yticks(y_axis)

    plt.xlabel("Date")
    plt.ylabel(metric.capitalize())

    plt.title(f"Evolution of the hashtag {hashtag} based on {metric}")

    # save plot and get binary 
    plt.savefig('plot.png')

    image_file = open("plot.png", "rb") # opening for [r]eading as [b]inary
    data = image_file.read() # if you only wanted to read 512 bytes, do .read(512)
    image_file.close()

    os.remove("plot.png")

    return data