import random
import os
import json

from discord import FFmpegPCMAudio

try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    botdata_path = os.path.join(script_dir, '..', 'botdata.json')

    with open(botdata_path, 'r') as jsonbotdata:
        botdata = json.load(jsonbotdata)
        JOINMESSAGESPREFIX = botdata['joinmessagesprefix']
        JOINMESSAGESSUFFIX = botdata['joinmessagessuffix']
        LEAVEMESSAGESPREFIX = botdata['leavemessagesprefix']
        LEAVEMESSAGESSUFFIX = botdata['leavemessagessuffix']

        NAMEFOLLOWUPS = botdata['namefollowups']
        SENTENCEENDINGS = botdata['sentenceendings']

        ENABLEEASTEREGGS = botdata.get('enable_easter_eggs', False) == 'True'
except Exception as e:
    print(f"Could not read botdata.json file: {e}")

async def checkEasterEgg(situation):
    try:
        eastereggroll = random.randint(1, 50)
        audiofile = ""
        if eastereggroll == 50 and ENABLEEASTEREGGS is True:
            eastereggdirpath = f"eastereggs/{situation}/"
            eastereggfile = random.choice([x for x in os.listdir(eastereggdirpath) if os.path.isfile(os.path.join(eastereggdirpath, x))])
            eastereggpath = eastereggdirpath + eastereggfile
            audiofile = FFmpegPCMAudio(eastereggpath)
        return audiofile
    except Exception as e:
        print(f"Something went wrong when checking for easter eggs: {e}")

async def getUsername(member):
    username = member.nick
    if username is None:
        username = member.name
    return username

async def getLeaveMessage(username):
    try:
        randend = random.randint(0, len(SENTENCEENDINGS) - 1)
        diceroll = random.randint(0, 2)
        if diceroll == 0:
            randpref = random.randint(0, len(LEAVEMESSAGESPREFIX) - 1)
            botmessage = LEAVEMESSAGESPREFIX[randpref] + username + SENTENCEENDINGS[randend]
        else:
            randsuff = random.randint(0, len(LEAVEMESSAGESSUFFIX) - 1)
            randname = random.randint(0, len(NAMEFOLLOWUPS) - 1)
            botmessage = username + NAMEFOLLOWUPS[randname] + LEAVEMESSAGESSUFFIX[randsuff] + SENTENCEENDINGS[randend]
    except Exception as e:
        print(f"Something went wrong when getting the leave message: {e}")
    return botmessage

async def getJoinMessage(username):
    try:
        randpref = random.randint(0, len(JOINMESSAGESPREFIX) - 1)
        randname = random.randint(0, len(NAMEFOLLOWUPS) - 1)
        randsuff = random.randint(0, len(JOINMESSAGESSUFFIX) - 1)
        randend = random.randint(0, len(SENTENCEENDINGS) - 1)
        botmessage = JOINMESSAGESPREFIX[randpref] + username + NAMEFOLLOWUPS[randname] + JOINMESSAGESSUFFIX[randsuff] + SENTENCEENDINGS[randend]
        return botmessage
    except Exception as e:
        print(f"Something went wrong when getting the join message: {e}")