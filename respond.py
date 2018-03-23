import webbrowser
import persist
import check_url
import recent
import custom

def open_browser(url, channel, userid, username, savedName):
    webbrowser.open(url, new=2)
    recent.commit(url, channel, userid, username, savedName)

def get_response(command, channel, userid, username):
    """
        Executes bot command if the command is known
    """

    # This is where you start to implement more commands!
    if command.startswith('home'):
        webbrowser.open('http://127.0.0.1:5000/', new=2)
    if command.startswith('open'):
        openString = command.split(' ')[1]
        
        favUrl = persist.getSavedRecipe(openString)
        if favUrl is None:
            url = openString[1:-1]
            if check_url.check_url(url):
                open_browser(url, channel, userid, username, None)
                return "Opening, {}!".format(url)
            
            return "I don't recognise {}".format(openString)
        else:
            open_browser(favUrl, channel, userid, username, openString)
            return "ok, opening {}".format(openString)
    if command.startswith('save'):
        parts = command.split(' ')
        print(parts)
        name = parts[1]
        url = parts[2][1:-1]
        if check_url.check_url(url):
            saved = persist.saveRecipe(name, url)
            if saved:
                return "Saving {} as `{}`!".format(url, name)
            else:
                return "I cannot save this since you already have a saved recipe named `{}`".format(name)
        else:
            return "Cannot set invalid url"
    if command.startswith('get recent'):
        return recent.pretty_print()
    if command.startswith('get saved'):
        return persist.pretty_print()
    if command.startswith('clear recent'):
        recent.clear();
        return 'Done!';
    if command.startswith('add custom'):
        name = command[11:]
        canadd = custom.begin(name)
        if canadd:
            return 'ok...'
        else:
            return 'already exists'
    if command.startswith('add item '):
        item_to_add = command[9:]
        custom.add(item_to_add)
        return ''
    if command.startswith('custom done'):
        custom.done()
        return 'done'
    
    # Default response is help text for the user
    return "Not sure what you mean. Try *{}*.".format('hi bot')