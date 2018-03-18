import os
import time
import re
import respond
from slackclient import SlackClient

slack_client = SlackClient(os.environ.get('SLACK_TOKEN'))

def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            print('got event')
            print(event)
            user_id, message = parse_direct_mention(event["text"])
           # if user_id == starterbot_id:
            return message, event["channel"]
    return None, None

def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search('bot', message_text)
    print(matches)
    return ('', message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def handle_command(command, channel):
    response = respond.get_response(command)
    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )
    
    
if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        while True:
            msg = slack_client.rtm_read()
            command, channel = parse_bot_commands(msg)
            if command:
                handle_command(command, channel)
            time.sleep(1)