# InstaditBot: Bot that fetches top subreddit posts and posts to instagram
#  Copyright (C) 2023  Merlin Glander <merlinglander@vogelhosting.de A7CF F31A 48DF F3C6 0D19  C131 DC46 0EB0 3DBE 76C4>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import json
import os
import wget
import shutil
import time
import random
import requests as r
from instagrapi import Client
from PIL import Image
import threading

# print license details
print("InstaditBot\n"
      "This program comes with ABSOLUTELY NO WARRANTY\n"
      "This is free software, and you are welcome to redistribute it\n"
      "under certain conditions")

# delete config folder
if os.path.isdir("./config"):
    shutil.rmtree("./config")

# load config dictionary
if os.path.isfile("dictionary.txt"):
    with open("dictionary.txt", "r") as configFileR:
        config = json.load(configFileR)
else:
    with open("dictionary.txt", "w") as f:
        f.write(str("{}"))
    with open("dictionary.txt", "r") as configFileR:
        config = json.load(configFileR)

# add account to config
def add_account():
    new_username = str(input("Username: "))
    new_password = str(input("Password: "))
    new_subreddit = str(input("What Subreddit? (without /r/) "))
    config.update({new_username: {"username": new_username, "password": new_password, "subreddit": new_subreddit}})
    if input("Add another account?[y/n] ") == "y":
        add_account()
    else:
        with open("dictionary.txt", "w") as configfilew:
            json.dump(config, configfilew)

if input("Add new account?[y/n] ") == "y":
    add_account()

def create_caption(reddit_memelist, hashtag_list, memelist_index):
    hashtag_list_current = random.sample(hashtag_list, 16)
    caption = (
        reddit_memelist["data"]["children"][memelist_index]["data"]["title"]
        + "\n.\nWhy are you liking my memes but not following? \n.\n "
        + " ".join(hashtag_list_current)
    )
    return caption

# make images squares
def make_square(im, min_size=256, fill_color=(0, 0, 0, 0)):
    sizex, sizey = im.size
    size = max(min_size, sizex, sizey)
    new_im = Image.new('RGB', (size, size), fill_color)
    new_im.paste(im, (int((size - sizex) / 2), int((size - sizey) / 2)))
    return new_im

# download memelists
def get_memelist(number):
    currentsub = config[number]["subreddit"]
    downloadlink = "https://www.reddit.com/r/" + currentsub + "/hot.json?limit=99"
    memelist = r.get(downloadlink, headers={"User-Agent": "CIA-Datendiebstahl"}).content
    with open(currentsub + ".json", "w") as newjson:
        memelist = memelist.decode('utf-8')
        newjson.write(str(memelist))
    with open(currentsub + ".json", "r") as file:
        reddit_memelist = json.load(file)
    return reddit_memelist

# log in to instagram
def post(username, password, number):
    print("starting Thread " + str(number))
    bot = Client()
    bot.login(username=username, password=password)
    # call the download function
    reddit_memelist = get_memelist(number)
    j = len(reddit_memelist["data"]["children"])
    # load posted files
    postedlist_file = str(username) + "_posted.txt"
    if os.path.isfile(postedlist_file):
        with open(postedlist_file, "r") as postedlistfile:
            postedlist = postedlistfile.read().split('\n')
    else:
        open(postedlist_file, "w").close()
        postedlist = []
    # load hashtags
    hashtag_list_file = username + "_hashtags.txt"
    with open(hashtag_list_file, "r") as hashtaglistFile:
        hashtag_list = hashtaglistFile.read().split("\n")
    for memelist_index in range(j):
        downlink = reddit_memelist["data"]["children"][memelist_index]["data"]["url"]
        extension = os.path.splitext(downlink)[1]
        filename = os.path.splitext(os.path.basename(downlink))[0]
        # make sure only jpgs come through
        if extension == ".jpg":
            # check if photo has been posted before
            print(username + ": Checking if photo " + str(filename) + " has been posted before")
            if filename in postedlist:
                print(username + ": Photo has been posted before")
            else:
                print(username + ": Photo has not been posted before, continuing to download")
                # download the jpgs
                print(username + ": " + downlink)
                print(username + ": ")
                wget.download(downlink)
                # make images squares and save
                test_image = Image.open(filename + ".jpg")
                new_image = make_square(test_image, fill_color=(255, 255, 255, 0))
                new_image.save(filename + "_squared" + ".jpg")
                # get the description
                image_caption = create_caption(reddit_memelist, hashtag_list, memelist_index)
                # post to instagram
                delay = random.randint(900, 1800)
                print(" \n Waiting for " + str(delay) + " seconds")
                time.sleep(delay)
                bot.photo_upload(filename + "_squared.jpg", caption=image_caption)
                # add image to posted list
                postedlist.append(filename)
                with open(postedlist_file, "w") as postedlistfile:
                    postedlistfile.write('\n'.join(postedlist))
                # count the yeah counter
                os.remove(str(filename) + ".jpg")
                os.remove(filename + "_squared" + ".jpg")
        else:
            print(username + ": Photo is not a .jpg, skipping!")

# start threading with arguments
for i in config:
    current_username = config[i]["username"]
    current_password = config[i]["password"]
    x = threading.Thread(target=post, args=(current_username, current_password, i))
    time.sleep(2)
    x.start()
