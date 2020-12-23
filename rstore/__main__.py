import requests
from prettytable import PrettyTable  # to print out pretty table
import json
import os
from os.path import expanduser


def main():
    home = expanduser("~")
    # file where json content are stored
    rstore_json = os.path.join(home, '.old_store.json')

    # check if last 75 post is stored
    try:
        f = open(rstore_json)
        old_store = json.loads(f.read())
        f.close()
    except IOError:
        old_store = None

    no_post = 75  # no of post to retrieve, can be change to any other value
    current_store = {}
    new_posts = []
    vote_changes = []

    response = requests.request(
        "GET", "https://www.reddit.com/r/popular.json", headers={
            'User-Agent': 'rstore/1.0',
        })

    if response.status_code == 200:
        # get top 75 posts
        posts = response.json()['data']['children'][:no_post]
        for post in posts:
            post_data = post['data']
            current_store[post_data['id']] = {
                "title": post_data['title'], "score": post_data['score']}

            if old_store:  # if not loading for the first time, run this to compare with
                if post_data['id'] in old_store:  # check if it's a new post

                    # check if score changes
                    if post_data['score'] != old_store[post_data['id']]['score']:
                        diff = int(post_data['score']) - \
                            int(old_store[post_data['id']]['score'])
                        vote_changes.append(
                            {"id": post_data['id'], "title": post_data['title'], "change": diff})

                else:
                    new_posts.append(
                        {"id": post_data['id'], "title": post_data['title']})

        # only run this part if it's not loading for the first time
        if old_store:

            # 1. Which posts (ID & Headline) are new from the last program execution,
            print("")
            print("#########################  New Posts ################################")
            print("")
            new_post_table = PrettyTable()
            new_post_table.field_names = ["Id.", "Title"]
            for new_post in new_posts:
                title = new_post['title'][:75] + '..'   # truncate title length
                new_post_table.add_row([new_post['id'], title])
            print(new_post_table)

            # 2. Which posts are no longer within the top 75 posts
            print("")
            print(
                "##################### Post No longer within tops posts ###################")
            print("")
            old_post_table = PrettyTable()
            old_post_table.field_names = ["Id.", "Title"]
            for id, val in old_store.items():
                if id not in current_store:
                    title1 = val['title'][:75] + \
                        '..'   # truncate title length
                    old_post_table.add_row([id, title1])
            print(old_post_table)

            # 3. Which posts have had their vote counts increase or decrease, and by how much.
            print("")
            print(
                "###################  Posts with changes in vote #########################")
            print("")
            change_vote_table = PrettyTable()
            change_vote_table.field_names = [
                "Id.", "Title", "Changed By", "Increase/Decrese"]
            for post in vote_changes:
                inc_dsc = "Increase" if post['change'] > 0 else "Decrease"
                title2 = post['title'][:75] + '..'   # truncate title length
                change_vote_table.add_row(
                    [post['id'], title2, abs(post['change']),  inc_dsc])
            print(change_vote_table)

        else:
            # Nothing to compare with for first load
            print("######################################################")
            print("################ First Time Loading ##################")
            print("###### Try again shortly after to get updates ########")
            print("######################################################")

        # store the new top 75 (no_post)
        f = open(rstore_json, "w")
        f.write(json.dumps(current_store))
        f.close()

    elif response.status_code == 429:
        print("#######################################################")
        print("######## Too Many Attemps Try again soon ##############")
        print("#######################################################")


if __name__ == '__main__':
    main()
