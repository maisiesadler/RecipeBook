import pickle
import os

directory = '/home/pi/recipe_book/recipes'
savedLoc = '/home/pi/recipe_book/recipes/custom.pkl';

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

def save(name, vals):
    saved = getSaved()
    if name in saved:
        return False
    saved[name] = vals
    print(saved)
    afile = open(savedLoc, 'wb')
    pickle.dump(saved, afile)
    afile.close()
    return True

context = {}

def begin(name):
    if name in getSaved():
        return False
    
    context['name'] = name
    context['val'] = []
    return True
def add(item):
    context['val'].append(item)
    
def done():
    save(context['name'], context['val'])
    return 'ok'