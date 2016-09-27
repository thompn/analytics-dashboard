import pandas as pd
import numpy as np
import matplotlib, scipy, time, MySQLdb
from collections import Counter
from datetime import datetime

import plotly
import plotly.offline as py
import plotly.graph_objs as go

db=MySQLdb.connect(read_default_group='trough')
cursor = db.cursor()
query = "SELECT * FROM messages"

df = pd.read_sql(query, db)
df.columns=[["usr","name","id","text","date","type","file","chatid","chattype"]]
messages = df[["id","name","date","text","file"]]

texts = messages[['name','date','text']]


def arg_compare(data, *args):
    outputcounts = []
    outputdicts = []
    for arg in args:
        argcount = 0
        argcdict = {}
        argdict = {}
        for row in data.itertuples():
            if type(row[4]) is str:
                if arg in row[4].lower():
                    argcount+=1
                    argdict[row[3]] = 1
        argcdict[arg] = argcount
        outputcounts.append(argcdict)
        outputdicts.append(argdict)
    output = outputcounts, outputdicts
    return output

def order_resample(data):
    lofdf = []
    terms = []
    for d in data[1]:
        df = pd.DataFrame.from_dict(d, orient='index')
        lofdf.append(df)
    frames = []
    for df, d in zip(lofdf, data[0]):
        for key, value in d.items():
            df[key] = df[0]
            terms.append(key)
            del df[0]
            frames.append(df)
    data = pd.concat(frames)
    data = data.resample('W').sum()
    return data, terms

def get_words(data, number, *args):
    words = []
    for row in data.itertuples():
        if type(row[4]) is str:
            if row[4].startswith("/"):
                pass
            else:
                try:
                    if "NULL" in row[5]:
                        words.append(row[4])
                except:
                    pass
    for arg in args:
        top = Counter(" ".join(words).split()).most_common(arg)
        top = [x[0] for x in top]
        allwords = Counter(" ".join(words).split()).most_common(number)
        allwords = [x for x in allwords if x[0] not in top]
    else:
        top = Counter(" ".join(words).split()).most_common(30)
        top = [x[0] for x in top]
        allwords = Counter(" ".join(words).split()).most_common(number)
        allwords = [x for x in allwords if x[0] not in top]
    return allwords


compare = arg_compare(messages, 'boat', 'spare', 'whitstable', 'kimera')

pop = order_resample(compare)

tots = messages[['date','id','name','text']]
names_tots = tots.groupby('name')
totals = names_tots.size().sort_values(ascending=False)

totals = totals.to_frame()

most_popular = get_words(messages, 10000,100)
most_popularlisttwo = []
for x in most_popular:
    if x[0] == "#":
        pass
    else:
        most_popularlisttwo.append(x)
most_popular = most_popularlisttwo
hashtags = ([x for x in most_popular if "#" in x[0]])
hashtags = pd.DataFrame(hashtags).head(10)
hashtags.columns = [["word","count"]]

types = df[['date','name','type']]
types.index = types.date
del types['date']
types['count'] = 1
chattypes = types.groupby('type').sum()
chattypes = chattypes.drop(chattypes.index[[0,1,2,3]])

usertypes = df[['name','date','type']]
usertypes['count'] = 1
usertypes.groupby(['name','type']).sum()
usertypes = pd.pivot_table(usertypes, index=['name'], \
            values=['count'],columns=['type'],aggfunc=np.sum)
usertypes = usertypes[usertypes.index != 'Risan']
users = []
photos = []
stickers = []
videos = []
new_titles = []
for row in usertypes.itertuples():
    users.append(row[0]) #user
    new_titles.append(row[4]) #newtitle
    photos.append(row[5]) #photos
    stickers.append(row[6]) #sticker
    videos.append(row[8]) #videos

utimes = tots[['date','name']]
utimes['count']=1
utimes = utimes[utimes.name != 'Risan']
