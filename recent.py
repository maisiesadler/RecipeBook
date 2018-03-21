import pickle
import os
import datetime

directory = '/home/pi/recipe_book/recipes'
savedLoc = '/home/pi/recipe_book/recipes/recent.pkl';
    
def init():
    cfile = open(savedLoc, 'wb')
    a = []
    pickle.dump(a, cfile)
    cfile.close()

def getRecent():
    if not os.path.exists(directory):
        os.makedirs(directory)
    if not os.path.isfile(savedLoc):
        init()
    file2 = open(savedLoc, 'rb')
    new_d = pickle.load(file2)
    file2.close()
    return new_d

def commit(recipeUrl, channel, userid, username, savedName = None):
    recent = getRecent()
    now = datetime.datetime.now()
    latest = {'url': recipeUrl, 'userid': userid,
              'username': username,
              'channel': channel, 'time': now,
              'savedName': savedName }
    print(latest)
    recent.append(latest)
    afile = open(savedLoc, 'wb')
    pickle.dump(recent, afile)
    afile.close()
    
def clear():
    init()
    
def pretty_print_one(historyEntry, idx):
    userid = historyEntry['userid']
    url = historyEntry['url']
    time = historyEntry['time'].strftime('%Y-%m-%d %H:%M:%S')
    one = "*{}:* <@{}> at {} - {}".format(idx, userid, time, url)
    if 'savedName' in historyEntry:
        one = one + ' (saved as `{}`)'.format(historyEntry['savedName'])
    return one;
    
def pretty_print():
    recentEnumerable = enumerate(reversed(getRecent()))
    return '\n'.join((pretty_print_one(s, idx) for idx, s in recentEnumerable))
