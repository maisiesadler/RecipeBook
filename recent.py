import pickle
import os

directory = 'recipes'
savedLoc = 'recipes/recent.pkl';

def getRecent():
    if not os.path.exists(directory):
        os.makedirs(directory)
    if not os.path.isfile(savedLoc):
        cfile = open(savedLoc, 'wb')
        a = []
        pickle.dump(a, cfile)
        cfile.close()
    file2 = open(savedLoc, 'rb')
    new_d = pickle.load(file2)
    file2.close()
    return new_d

def commit(recipeUrl, user, channel):
    recent = getRecent()
    latest = {'url': recipeUrl, 'user': user, 'channel': channel}
    print(latest)
    recent.append(latest)
    afile = open(savedLoc, 'wb')
    pickle.dump(recent, afile)
    afile.close()
    
def pretty_print_one(historyEntry):
    return '<@' + historyEntry['user'] + '> - ' + historyEntry['url']
    
def pretty_print():
    return '\n'.join((pretty_print_one(s) for s in getRecent()))
