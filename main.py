# Downloads top 100 .jpg and .png images from a given subreddit

import praw
import urllib.request
import os
import shutil
import config

# Initialising PRAW Reddit
reddit = praw.Reddit(
    client_id = config.client_id,
    client_secret = config.client_secret,
    user_agent = config.user_agent,
)


def get_img():
    sub_name = input("Enter a Subreddit name: ")

    # Removes directory if it exists
    if os.path.exists(sub_name):
        shutil.rmtree(sub_name)
    # Creates new directory after setting permissions
    os.makedirs(sub_name, 0o700)

    # Selects top 100 posts
    top_posts = reddit.subreddit(sub_name).top(limit=None)

    number = 1

    for post in top_posts:
        if number <= 100:
            try:
                if post.url.endswith(".jpg") or post.url.endswith(".png"):
                    # Gets the images from each post
                    response = urllib.request.urlopen(post.url)
                    img = response.read()

                    # Downloads all .jpg and .png images
                    if post.url.endswith(".jpg"):
                        with open(sub_name + "/" + str(number) + ".jpg", "wb") as f:
                            f.write(img)
                    if post.url.endswith(".png"):
                        with open(sub_name + "/" + str(number) + ".png", "wb") as f:
                            f.write(img)
                    
                    number += 1
            except:
                continue
        else:
            break



get_img()
