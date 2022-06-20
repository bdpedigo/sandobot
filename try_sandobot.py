#%%
import json

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import tweepy
from scipy.stats import rankdata

#%%
with open("./creds.json", "r") as f:
    creds = json.load(f)

client = tweepy.Client(creds["bearer_token"])

user = client.get_user(username="SandwichSeattle")
id = user.data.id

#%%
datas = []
for response in tweepy.Paginator(
    client.get_users_tweets, id, max_results=100, limit=1000
):
    data = response.data
    datas.append(data)

#%%
rows = []
for data in datas:
    for tweet in data:
        text = tweet.text

        if (text.find(" - ") != -1) and (text.find("):") != -1):
            index = text.find("/10")
            if index != -1:
                substring = text[index - 4 : index + 3]
                full_rating = substring.split(" ")[-1]
                rating = full_rating.split("/")[0]
                rating = rating.replace(":", ".")
                rating = float(rating)

                colon_index = text.find(":")
                dash_index = text.find(" - ")
                openparen_index = text.find("(")
                closeparen_index = text.find(")")
                sandwich_name = text[0:dash_index].strip(" ")

                seller = text[dash_index:openparen_index].strip(" - ").strip(" ")

                location = text[openparen_index + 1 : closeparen_index]

                rows.append(
                    {
                        "rating": rating,
                        "text": text,
                        "sandwich_name": sandwich_name,
                        "seller": seller,
                        "location": location,
                    }
                )
#%%


results = pd.DataFrame(rows)
results.sort_values("rating", inplace=True, ascending=False)
results = results.reset_index(drop=True)
results["rank"] = rankdata(-results["rating"], method="min")
results

#%%

fig, ax = plt.subplots(1, 1, figsize=(8, 6))

sns.set_context("talk", font_scale=2)

sns.histplot(data=results, x="rating", ax=ax, bins=15)

ax.set(xticks=[5, 6, 7, 8, 9, 10], xlabel="Rating (out of 10)")

#%%

results.head(10)

# %%
