import webbrowser
import persist
import check_url
import recent

def open_browser(url, channel, user):
    webbrowser.open(url, new=2)
    recent.commit(url, user, channel)

def get_response(command, channel, user):
    """
        Executes bot command if the command is known
    """

    # This is where you start to implement more commands!
    if command.startswith('open'):
        openString = command.split(' ')[1]
        
        favUrl = persist.getSavedRecipe(openString)
        if favUrl is None:
            url = openString[1:-1]
            if check_url.check_url(url):
                open_browser(url, channel, user)
                return "Opening, {}!".format(url)
            
            return "I don't recognise {}".format(openString)
        else:
            open_browser(favUrl, channel, user)
            return "ok, opening {}".format(openString)
    if command.startswith('save'):
        parts = command.split(' ')
        print(parts)
        name = parts[1]
        url = parts[2][1:-1]
        if check_url.check_url(url):
            persist.saveRecipe(name, url)
            return "Saving {} as '{}'!".format(url, name)
        else:
            return "Cannot set invalid url"
    if command.startswith('show recent'):
        return recent.pretty_print()
    
    # Default response is help text for the user
    return "Not sure what you mean. Try *{}*.".format('hi bot')