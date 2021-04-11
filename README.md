[![forthebadge](https://forthebadge.com/images/badges/0-percent-optimized.svg)](https://forthebadge.com) [![forthebadge](https://forthebadge.com/images/badges/gluten-free.svg)](https://forthebadge.com) [![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com) [![forthebadge](https://forthebadge.com/images/badges/powered-by-coffee.svg)](https://forthebadge.com)

[![GitHub license](https://img.shields.io/github/license/FPVogel/InstaditBot?style=for-the-badge&logo=appveyor)](https://github.com/FPVogel/InstaditBot/blob/main/LICENSE)
# InstaditBot
 Bot that fetches top subreddit posts and posts to instagram
# Usage
To use the bot install the required libraries as in requirements.txt, after that start the script multiple.py to set up your account(s). The bot fetches the top 100 posts in given subreddit and downloads the .jpg files, converts these to a 1:1 ratio, fetches the description of the original post along with hashtags that are being pulled from hashtags.txt and randomly ordered. The script then waits a random amount of time between 15 and 30 minutes and after that posts the image with description. You can also run multiple-headless.py to not be prompted at startup and be able to automate the script.
