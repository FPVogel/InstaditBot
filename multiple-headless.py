import json
import os
import wget
import shutil
import time
import random
import requests as r
from instabot import Bot
from PIL import Image
import threading

# delete config folder
if os.path.isdir("./config"):
    shutil.rmtree("./config")

# load config dictionary

if os.path.isfile("dictionary.txt"):
    configFileR = open("dictionary.txt", "r")
    config = json.load(configFileR)
    configFileR.close()
else:
    f = open("dictionary.txt", "w")
    f.write(str("{}"))
    f.close()
    configFileR = open("dictionary.txt", "r")
    config = json.load(configFileR)
    configFileR.close()


# make images squares
def make_square(im, min_size=256, fill_color=(0, 0, 0, 0)):
    sizex, sizey = im.size
    size = max(min_size, sizex, sizey)
    new_im = Image.new('RGB', (size, size), fill_color)
    new_im.paste(im, (int((size - sizex) / 2), int((size - sizey) / 2)))
    return new_im


# log in to instagram
def post(username, password, reddditmemelist, number):
    print("starting Thread " + str(number))
    bot = Bot()
    bot.login(username=username, password=password, is_threaded=True)
    j = len(reddditmemelist["data"]["children"])
    with open(str(username) + "_posted.txt", "r") as postedlistFile:
        postedlist = postedlistFile.read().split('\n')
    with open(username + "_hashtags.txt", "r") as hashtaglistFile:
        hashtaglist = hashtaglistFile.read().split("\n")
    for memelisti in range(j):
        downlink = reddditmemelist["data"]["children"][memelisti]["data"]["url"]
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
                hashtaglistcurrent = []
                for _ in range(16):
                    randomhashtag = random.randint(0, len(hashtaglist) - 1)
                    hashtaglistcurrent.append(hashtaglist[randomhashtag])
                imagecaption = reddditmemelist["data"]["children"][memelisti]["data"]["title"] \
                    + "\n.\nWhy are you liking my memes but not following? \n.\n " + hashtaglistcurrent[1] \
                    + hashtaglistcurrent[2] + hashtaglistcurrent[3] + hashtaglistcurrent[4] + \
                    hashtaglistcurrent[5] \
                    + hashtaglistcurrent[6] + hashtaglistcurrent[7] + hashtaglistcurrent[8] + \
                    hashtaglistcurrent[9] \
                    + hashtaglistcurrent[10] + hashtaglistcurrent[11] + hashtaglistcurrent[12] + \
                    hashtaglistcurrent[13] \
                    + hashtaglistcurrent[14] + hashtaglistcurrent[15]
                # post to instagram
                delay = random.randint(900, 1800)
                print(" \n Waiting for " + str(delay) + " seconds")
                time.sleep(delay)
                bot.upload_photo(filename + "_squared.jpg", caption=imagecaption)
                # add image to posted list
                postedlist.append(filename)
                with open(str(username) + "_posted.txt", "w") as postedlistFile:
                    for element in postedlist:
                        postedlistFile.write(element)
                        postedlistFile.write('\n')
                # count the yeah counter
                os.remove(str(filename) + ".jpg")
                os.remove(filename + "_squared" + ".jpg.REMOVE_ME")
        else:
            print(username + ": Photo is not a .jpg, skipping!")


for i in config:
    currentsub = config[i]["subreddit"]
    currentusername = config[i]["username"]
    currentpassword = config[i]["password"]
    downloadlink = "https://www.reddit.com/r/" + currentsub + "/hot.json?limit=99"
    memeList = r.get(downloadlink, headers={"User-Agent": "CIA-Datendiebstahl"}).content
    newjson = open(currentsub + ".json", "w")
    memeList = memeList.decode('utf-8')
    newjson.write(str(memeList))
    newjson.close()
    file = open(currentsub + ".json", "r")
    y = json.load(file)
    file.close()
    x = threading.Thread(target=post, args=(str(currentusername), str(currentpassword), y, i))
    time.sleep(2)
    x.start()
