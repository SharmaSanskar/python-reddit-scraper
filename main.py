# Downloads top .jpg and .png images from a given subreddit

import praw
import urllib.request
import os
import shutil
import config
import tkinter as tk
from tkinter import *

# Initialising PRAW Reddit
reddit = praw.Reddit(
    client_id=config.client_id,
    client_secret=config.client_secret,
    user_agent=config.user_agent,
)


def get_img(sub_txt, imgno_txt):
    img_no = int(imgno_txt.get())
    sub_name = sub_txt.get()
    progress_txt.set(f"Downloading top {img_no} images from r/{sub_name} . . .")

    # Removes directory if it exists
    if os.path.exists(sub_name):
        shutil.rmtree(sub_name)
    # Creates new directory after setting permissions
    os.makedirs(sub_name, 0o700)

    # Selects top 100 posts
    top_posts = reddit.subreddit(sub_name).top(limit=None)

    number = 1

    for post in top_posts:
        if number <= img_no:
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

    progress_txt.set("Images downloaded successfully!!")


# GUI
root = tk.Tk()
root.title("Reddit Scraper")

root.geometry("600x300")

heading_label = tk.Label(root, text="Reddit Scrapper", font=("Poppins", 14, "bold")).place(relx = 0.5, rely = 0.1, anchor = CENTER)
subheading_label = tk.Label(root, text="Download top images from any subreddit", font=("Poppins", 12)).place(relx = 0.5, rely = 0.2, anchor = CENTER)

sub_label = tk.Label(root,text = "Enter subreddit name", font=('Poppins', 10)).place(relx = 0.1, rely = 0.3) 
sub_txt = tk.StringVar()
sub_entry = tk.Entry(root, textvariable = sub_txt, font=('Poppins', 10)).place(relx = 0.5, rely = 0.3)  

imgno_label = tk.Label(root,text = "Enter number of images", font=('Poppins', 10)).place(relx = 0.1, rely = 0.45) 
imgno_txt = tk.StringVar()
imgno_entry = tk.Entry(root, textvariable = imgno_txt, font=('Poppins', 10)).place(relx = 0.5, rely = 0.45) 

submit_btn = tk.Button(root, text = "Download", command= lambda: get_img(sub_txt, imgno_txt), font=('Poppins', 12, "bold"), bg="#FF5700", fg="white", width=12).place(relx = 0.5, rely = 0.7, anchor = CENTER)

progress_txt = tk.StringVar()
progress_label = tk.Label(root, textvariable = progress_txt, font=('Poppins', 10)).place(relx = 0.5, rely = 0.88, anchor = CENTER)

root.mainloop()
