import pickle
import os

directory = '/home/pi/recipe_book/recipes'
savedLoc = '/home/pi/recipe_book/recipes/saved.pkl';

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
    if name in saved:
        return False
    saved[name] = url
    afile = open(savedLoc, 'wb')
    pickle.dump(saved, afile)
    afile.close()
    return True

def getSavedRecipe(name):
    saved = getSaved()
    if name in saved:
        return saved[name]
    else:
        return None
    
def pretty_print_one(name, value):
    return '{}- {}'.format(name, value)
    
def pretty_print():
    saved = getSaved()
    return '\n'.join((pretty_print_one(name, saved[name]) for name in saved.keys()))
    
#saveRecipe('cheese', 'testing')
#print(getSaved())