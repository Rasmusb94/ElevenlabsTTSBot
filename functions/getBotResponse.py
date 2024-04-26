import json
import os

try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    botdata_path = os.path.join(script_dir, '..', 'botdata.json')

    with open(botdata_path, 'r') as jsonbotdata:
        botdata = json.load(jsonbotdata)
    PREFIX = botdata['command_prefix']
    RUDE_BOT = botdata.get('rude_bot', False) == 'True'
except Exception as e:
    print(f"Could not read botdata.json file: {e}")

async def getBotResponse(botresponse):
    '''Exception return messages'''
    match RUDE_BOT:
        case True:
            match botresponse:
                case 'valerror':
                    return("Wrong input dickhead")
                case 'leaving':
                    return("Peace out losers")
                case 'alreadyjoined':
                    return("Hey, I'm right here bitch")
                case 'notconnected':
                    return("I can't leave if I'm not connected.. Jeez Louise..")
                case 'usernotconnected':
                    return("How 'bout you join first, and then I'll consider it.")
                case 'stop':
                    return("Alright, alright, jeez...")
                case 'notspeaking':
                    return("I'm not even talking bruh!")
                case _:
                    return("It doesn't work I guess, beats me.")
        case False:
            match botresponse:
                case 'valerror':
                    returnmessage = "Wrong input, check "+ PREFIX +"help for command guides"
                    return(returnmessage)
                case 'leaving':
                    return("Leaving the voice channel")
                case 'alreadyjoined':
                    return("I'm already in your voice channel")
                case 'notconnected':
                    return("I'm already not here mate")
                case 'usernotconnected':
                    return("You need to join the channel before using a bot command")
                case 'stop':
                    return("Stopping the madness")
                case 'notspeaking':
                    return("Can't stop if I'm not goin!")
                case _:
                    return("It doesn't work I guess, beats me.")