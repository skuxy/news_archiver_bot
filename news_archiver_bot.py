#!/usr/bin/python3

import praw
import requests

NEWS_WEBSITES = [
    "index.hr",
    "novosti.com",
    "jutarnji.hr",
    "vecernji.hr",
    "dnevnik.hr",
    "rtl.hr",
    "dnevno.hr",
    "slobodnadalmacija.hr",
    "novilist.hr",
    "telegraf.rs",
    "telegram.hr"
]

reddit = praw.Reddit('news_bot')

hreddit_object = reddit.subreddit('croatia')

for submission in hreddit_object.new(limit=20):

    mentions_archive = False
    for comment in submission.comments:
        if "web.archive.org" in comment.body:
            mentions_archive = True
    if mentions_archive:
        continue

    original_url = submission.url

    if len([news_site for news_site in NEWS_WEBSITES
            if news_site in original_url]) > 0:

        save_post_to_archive_url = \
            "https://web.archive.org/save/{}".format(original_url)

        retry_count = 0

        while retry_count < 3:
            save_post_response = requests.get(save_post_to_archive_url)
            if save_post_response == 200:
                break

            retry_count += 1

        if save_post_response.status_code == 200:
            archived_post_json = \
                "http://archive.org/wayback/available?url={}".format(
                    original_url
                )

            archived_post_response = requests.get(archived_post_json)
            archived_post_json = archived_post_response.json()

            if archived_post_json['archived_snapshots']:
                archived_post_url = \
                    archived_post_json['archived_snapshots']['closest']['url']

                print(archived_post_url)
                submission.reply(
                    '''[Archive.org link, ako ne zelite davati klikove ovom portalu]({})
                    \n\n
                    ^(Ja sam bot, ako imate prigovora slobodno PMate u/skuxy)'''
                    .format(archived_post_url))
