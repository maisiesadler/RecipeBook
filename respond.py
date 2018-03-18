import webbrowser
import persist
import check_url

def get_response(command):
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
                webbrowser.open(url, new=2)
                return "Opening, {}!".format(url)
            
            return "I don't recognise {}".format(openString)
        else:
            webbrowser.open(favUrl, new=2)
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
    
    # Default response is help text for the user
    return "Not sure what you mean. Try *{}*.".format('hi bot')