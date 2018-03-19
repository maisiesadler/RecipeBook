import pickle
import os

directory = 'recipes'
savedLoc = 'recipes/saved.pkl';

def getSaved():
    if not os.path.exists(directory):
        os.makedirs(directory)
    if not os.path.isfile(savedLoc):
        cfile = open(savedLoc, 'wb')
        a = {}
        pickle.dump(a, cfile)
        cfile.close()
    file2 = open(savedLoc, 'rb')
    new_d = pickle.load(file2)
    file2.close()
    return new_d

def saveRecipe(name, url):
    saved = getSaved()
    saved[name] = url
    afile = open(savedLoc, 'wb')
    pickle.dump(saved, afile)
    afile.close()

def getSavedRecipe(name):
    saved = getSaved()
    if name in saved:
        return saved[name]
    else:
        return None
    
#saveRecipe('cheese', 'testing')
#print(getSaved())