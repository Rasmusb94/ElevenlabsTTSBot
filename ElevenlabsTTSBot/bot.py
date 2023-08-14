import asyncio
import os
import random
import json
import discord
import requests

from discord import FFmpegPCMAudio
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from elevenlabs import voices

with open('botdata.json', 'r') as jsonbotdata:
    botdata = json.load(jsonbotdata)
TOKEN = botdata['discord_token']
PREFIX = botdata['command_prefix']
EXTENSION = ".mp3"
SERVERID = botdata['discord_server_id']
APIKEY = botdata['elevenlabs_api_key']
ROLEID = botdata['role_id']
SOUNDFILEDIR = 'soundfiles/'
EASTEREGGSDIR = 'eastereggs/'
EASTEREGGSJOINDIR = 'join/'
EASTEREGGSLEAVEDIR = 'leave/'
eastereggcheck = botdata['enable_easter_eggs']
ENABLEEASTEREGGS = True if eastereggcheck == 'True' else False
CHUNK_SIZE = 1024
leavejoincheck = botdata['leave_join_sounds']
LEAVEJOINTTS = True if leavejoincheck == 'True' else False
LEAVEJOINSTABILITY = botdata['leave_join_stability']
if LEAVEJOINSTABILITY == "random":
    LEAVEJOINSTABILITY = round(random.uniform(0.01, 0.2),2)
rudebotcheck = botdata['rude_bot']
RUDE_BOT = True if rudebotcheck == 'True' else False
intents = discord.Intents.all()
intents.members = True
help_command = commands.DefaultHelpCommand(no_category = 'Commands')
HELPDESCRIPTION = "These are the currently available commands!"
TTSMODEL = 'eleven_monolingual_v1'

joinMessagesprefix = botdata['joinmessagesprefix']
joinMessageprefixslen = len(joinMessagesprefix)
joinMessagessuffix = botdata['joinmessagessuffix']
joinMessagessuffixlen = len(joinMessagessuffix)

leaveMessagesprefix = botdata['leavemessagesprefix']
leaveMessagesprefixlen = len(leaveMessagesprefix)
leaveMessagessuffix = botdata['leavemessagessuffix']
leaveMessagessuffixlen = len(leaveMessagessuffix)

namefollowups = botdata['namefollowups']
namefollowupslen = len(namefollowups)
sentenceendings = botdata['sentenceendings']
sentenceendingslen = len(sentenceendings)

headers = {
  "Accept": "audio/mpeg",
  "Content-Type": "application/json",
  "xi-api-key": APIKEY
}

bot = commands.Bot(command_prefix=PREFIX,
                   intents=intents,
                   case_insensitive=True,
                   help_command=help_command,
                   description=HELPDESCRIPTION)

@bot.event
async def on_ready():
    '''Connects the bot to Discord'''
    print(f"{bot.user.name} has connected to Discord!")
    statusmessage = "Type " + PREFIX + "help"
    activity = discord.Game(statusmessage)
    await bot.change_presence(status=discord.Status.online, activity=activity)

@bot.command(pass_context=True, name="join", help="Joins the voice channel")
async def _join(ctx):
    await getvoice(ctx)

@bot.command(pass_context=True, name="leave", help="Leaves the voice channel")
async def _leave(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
        botresponse = "leaving"
        errormessage = await getbotresponse(botresponse)
        botmessage = await ctx.send(errormessage)
        await asyncio.sleep(5)
        await botmessage.delete()
        print("Leaving the channel")
    else:
        botresponse = "notconnected"
        errormessage = await getbotresponse(botresponse)
        botmessage = await ctx.send(errormessage)
        await asyncio.sleep(5)
        await botmessage.delete()

@bot.command(pass_context=True, name="random", help="Takes a random voice and stability, just type " + PREFIX + "'random Hello World'")
async def _random(ctx, *args):
    voice = await getvoice(ctx)
    try:
        botmessage = " ".join(args[:])
        voicedata = voices()
        counter = 0
        randommax = len(voicedata)
        voicenum = random.randrange(0, randommax)
        voiceid = voicedata[voicenum].voice_id
        ttsvoice = voicedata[voicenum].name.capitalize()
        stability = round(random.uniform(0.01, 1.00),2)
        print(stability)
        url = "https://api.elevenlabs.io/v1/text-to-speech/" + voiceid
        data = {
            "text": botmessage,
            "model_id": TTSMODEL,
            "voice_settings": {
                "stability": stability,
                "similarity_boost": stability
            }
        }
        response = requests.post(url, json=data, headers=headers, timeout=10)
        ttsuser = ctx.message.author.name
        counter = 2
        filename = ttsuser + EXTENSION
        filepath = SOUNDFILEDIR + filename
        while os.path.exists(filepath):
            filepath = SOUNDFILEDIR + ttsuser + str(counter) + EXTENSION
            counter += 1
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                if chunk:
                    f.write(chunk)
        audiofile = FFmpegPCMAudio(filepath)
        print(ttsvoice, "Says:", botmessage, "as requested by", ttsuser)
        voice.stop()
        voice.play(audiofile)
        stabstr = str(stability)
        infomessage = "Random voice: " + ttsvoice + ". Stability: " + stabstr
        message = await ctx.send(infomessage)
        await asyncio.sleep(10)
        await message.delete()
    except (ValueError, UnboundLocalError) as valerror:
        botresponse = "valerror"
        errormessage = await getbotresponse(botresponse)
        botmessage = await ctx.send(errormessage)
        print(valerror)
        await asyncio.sleep(5)
        await botmessage.delete()

@bot.command(pass_context=True, name="tts", help="Use tts Voice message, example: " + PREFIX + "'tts Adam 50 Hello World' param: <Voice or random> <Stability 1-100> <Message>")
async def _tts(ctx, name, stability, *args):
    voice = await getvoice(ctx)
    try:
        botmessage = " ".join(args[:])
        ttsvoice = name.capitalize()
        voicedata = voices()
        counter = 0
        stablecheck = int(stability)
        randomvoice = False
        if stablecheck > 100:
            stability = '50'
        else:
            stablecheck = float(stablecheck / 100)
            stability = str(stablecheck)
        if ttsvoice == "Random":
            randomvoice = True
            randommax = len(voicedata)
            voicenum = random.randrange(0, randommax)
            voiceid = voicedata[voicenum].voice_id
            ttsvoice = voicedata[voicenum].name
        else:
            for i in voicedata:
                if ttsvoice == voicedata[counter].name:
                    voiceid = voicedata[counter].voice_id
                counter += 1
        url = "https://api.elevenlabs.io/v1/text-to-speech/" + voiceid
        data = {
            "text": botmessage,
            "model_id": TTSMODEL,
            "voice_settings": {
                "stability": stability,
                "similarity_boost": stability
            }
        }
        response = requests.post(url, json=data, headers=headers, timeout=10)
        ttsuser = ctx.message.author.name
        counter = 2
        filename = ttsuser + EXTENSION
        filepath = SOUNDFILEDIR + filename
        while os.path.exists(filepath):
            filepath = SOUNDFILEDIR + ttsuser + str(counter) + EXTENSION
            counter += 1
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                if chunk:
                    f.write(chunk)
        audiofile = FFmpegPCMAudio(filepath)
        print(ttsvoice, "Says:", botmessage, "as requested by", ttsuser)
        voice.stop()
        voice.play(audiofile)
        if randomvoice is True:
            infomessage = "Random voice: " + ttsvoice
            message = await ctx.send(infomessage)
            await asyncio.sleep(10)
            await message.delete()
    except (ValueError, UnboundLocalError) as valerror:
        botresponse = "valerror"
        errormessage = await getbotresponse(botresponse)
        botmessage = await ctx.send(errormessage)
        print(valerror)
        await asyncio.sleep(5)
        await botmessage.delete()

@bot.command(pass_context=True, name="unstable", help="TTS with 0 stability, for making crazy stuff! '!tts Adam Hello World' param: <Voice or random> <Message>")
async def _unstable(ctx, name, *args):
    voice = await getvoice(ctx)
    try:
        botmessage = " ".join(args[:])
        ttsvoice = name.capitalize()
        voicedata = voices()
        counter = 0
        randomvoice = False
        stability = "0.00"
        if ttsvoice == "Random":
            randomvoice = True
            randommax = len(voicedata)
            voicenum = random.randrange(0, randommax)
            voiceid = voicedata[voicenum].voice_id
            ttsvoice = voicedata[voicenum].name
        else:
            for i in voicedata:
                if ttsvoice == voicedata[counter].name:
                    voiceid = voicedata[counter].voice_id
                counter += 1
        url = "https://api.elevenlabs.io/v1/text-to-speech/" + voiceid
        data = {
            "text": botmessage,
            "model_id": TTSMODEL,
            "voice_settings": {
                "stability": stability,
                "similarity_boost": stability
            }
        }
        response = requests.post(url, json=data, headers=headers, timeout=10)
        ttsuser = ctx.message.author.name
        counter = 2
        filename = ttsuser + EXTENSION
        filepath = SOUNDFILEDIR + filename
        while os.path.exists(filepath):
            filepath = SOUNDFILEDIR + ttsuser + str(counter) + EXTENSION
            counter += 1
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                if chunk:
                    f.write(chunk)
        audiofile = FFmpegPCMAudio(filepath)
        print(ttsvoice, "Says:", botmessage, "as requested by", ttsuser)
        voice.stop()
        voice.play(audiofile)
        if randomvoice is True:
            infomessage = "Random voice: " + ttsvoice
            message = await ctx.send(infomessage)
            await asyncio.sleep(10)
            await message.delete()
    except (ValueError, UnboundLocalError) as valerror:
        botresponse = "valerror"
        errormessage = await getbotresponse(botresponse)
        botmessage = await ctx.send(errormessage)
        print(valerror)
        await asyncio.sleep(5)
        await botmessage.delete()
@bot.event
async def on_voice_state_update(member, before, after):
    '''For sending TTS messages when users join and leave the voice channel'''
    if ROLEID in [y.id for y in member.roles] and LEAVEJOINTTS is True :
        try:
            voice = discord.utils.get(
                bot.voice_clients, guild=member.guild
            )
            if after.channel is not None:
                channel = member.voice.channel
                if voice is None:
                    voice = await channel.connect()
            #leaving sounds
            if after.channel is None and before.channel == voice.channel:
                eastereggroll = random.randint(1, 50)
                if eastereggroll == 50 and ENABLEEASTEREGGS is True:
                    eastereggdirpath = EASTEREGGSDIR + EASTEREGGSLEAVEDIR
                    eastereggfile = random.choice([x for x in os.listdir(eastereggdirpath) if os.path.isfile(os.path.join(eastereggdirpath, x))])
                    eastereggpath = eastereggdirpath + eastereggfile
                    audiofile = FFmpegPCMAudio(eastereggpath)
                else:
                    randend = random.randint(0, sentenceendingslen - 1)
                    diceroll = random.randint(0, 2)
                    username = member.nick
                    if username is None:
                        username = member.name
                    if diceroll == 0:
                        randpref = random.randint(0, leaveMessagesprefixlen - 1)
                        botmessage = leaveMessagesprefix[randpref] + username + sentenceendings[randend]
                    else:
                        randsuff = random.randint(0, leaveMessagessuffixlen - 1)
                        randname = random.randint(0, namefollowupslen - 1)
                        botmessage = username + namefollowups[randname] + leaveMessagessuffix[randsuff] + sentenceendings[randend]
                    voicedata = voices()
                    stability = LEAVEJOINSTABILITY
                    randommax = len(voicedata)
                    voicenum = random.randrange(0, randommax)
                    voiceid = voicedata[voicenum].voice_id
                    ttsvoice = voicedata[voicenum].name
                    url = "https://api.elevenlabs.io/v1/text-to-speech/" + voiceid
                    data = {
                        "text": botmessage,
                        "model_id": TTSMODEL,
                        "voice_settings": {
                            "stability": stability,
                            "similarity_boost": stability
                        }
                    }
                    response = requests.post(url, json=data, headers=headers, timeout=10)
                    ttsuser = member.name
                    counter = 2
                    filename = ttsuser + "_leave" + EXTENSION
                    filepath = SOUNDFILEDIR + filename
                    while os.path.exists(filepath):
                        filepath = SOUNDFILEDIR + ttsuser + "_leave" + str(counter) + EXTENSION
                        counter += 1
                    with open(filepath, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                            if chunk:
                                f.write(chunk)
                    f.close()
                    audiofile = FFmpegPCMAudio(filepath)
                    print("Playing " + botmessage + " using " + ttsvoice)
                voice.stop()
                voice.play(audiofile)
            #joining sounds
            elif before.channel is None and after.channel is voice.channel or before.channel is not voice.channel and after.channel is voice.channel:
                eastereggroll = random.randint(1, 50)
                if eastereggroll == 50 and ENABLEEASTEREGGS is True:
                    eastereggdirpath = EASTEREGGSDIR + EASTEREGGSJOINDIR
                    eastereggfile = random.choice([x for x in os.listdir(eastereggdirpath) if os.path.isfile(os.path.join(eastereggdirpath, x))])
                    eastereggpath = eastereggdirpath + eastereggfile
                    audiofile = FFmpegPCMAudio(eastereggpath)
                else:
                    randpref = random.randint(0, joinMessageprefixslen - 1)
                    randname = random.randint(0, namefollowupslen - 1)
                    randsuff = random.randint(0, joinMessagessuffixlen - 1)
                    randend = random.randint(0, sentenceendingslen - 1)
                    username = member.nick
                    if username is None:
                        username = member.name
                    botmessage = joinMessagesprefix[randpref] + username + namefollowups[randname] + joinMessagessuffix[randsuff] + sentenceendings[randend]
                    voicedata = voices()
                    stability = "0.00"
                    randommax = len(voicedata)
                    voicenum = random.randrange(0, randommax)
                    voiceid = voicedata[voicenum].voice_id
                    ttsvoice = voicedata[voicenum].name
                    url = "https://api.elevenlabs.io/v1/text-to-speech/" + voiceid
                    data = {
                        "text": botmessage,
                        "model_id": TTSMODEL,
                        "voice_settings": {
                            "stability": stability,
                            "similarity_boost": stability
                        }
                    }
                    response = requests.post(url, json=data, headers=headers, timeout=10)
                    ttsuser = member.name
                    counter = 2
                    filename = ttsuser + "_join" + EXTENSION
                    filepath = SOUNDFILEDIR + filename
                    while os.path.exists(filepath):
                        filepath = SOUNDFILEDIR + ttsuser + "_join" + str(counter) + EXTENSION
                        counter += 1
                    with open(filepath, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                            if chunk:
                                f.write(chunk)
                    f.close()
                    audiofile = FFmpegPCMAudio(filepath)
                    print("Playing " + botmessage + " using " + ttsvoice)
                voice.stop()
                voice.play(audiofile)
        except (ValueError, UnboundLocalError, AttributeError, TypeError) as errormsg:
            print(errormsg)

@bot.event
async def on_message(message):
    '''For removing messages sent to the bot'''
    await bot.process_commands(message)
    if message.content.startswith(PREFIX):
        await asyncio.sleep(20)
        await message.delete()

@bot.command(pass_context=True, name="voices", help="Displays the available voices for use")
async def _voices(ctx):
    data = voices()
    namelist = []
    counter = 0
    for i in data:
        voicename = str(data[counter].name)
        namelist.append(voicename)
        counter += 1
    namelist.sort()
    message = ''
    last_item = namelist[-1]
    for i in namelist:
        message += i
        if i != last_item:
            message += ', '
    botmessage = await ctx.send("These are the available TTS voices: \n" + message)
    await asyncio.sleep(45)
    await botmessage.delete()

@bot.command(pass_context=True, name="quota", help="Displays the remaining quota for use")
async def _quota(ctx):
    url = "https://api.elevenlabs.io/v1/user"
    apiheaders = {
    "Accept": "application/json",
    "xi-api-key": APIKEY
    }
    response = requests.get(url, headers=apiheaders, timeout=10)
    listtest = json.loads(response.text)
    remainingquota = int(listtest["subscription"]["character_limit"]) - int(listtest["subscription"]["character_count"])
    botmessage = await ctx.send("Your remaining quota for this month is: " + str(remainingquota) + " characters.")
    await asyncio.sleep(10)
    await botmessage.delete()

async def getvoice(ctx):
    '''For connecting the bot to voice chat'''
    if await doguildcheck(ctx) is True:
        if ctx.voice_client is None:
            if ctx.author.voice:
                channel = ctx.message.author.voice.channel
                voice = await channel.connect()
                print("joining voice channel of", ctx.author.name)
                return voice
            joinmessage(ctx)
        else:
            if ctx.author.voice:
                if ctx.voice_client.channel != ctx.message.author.voice.channel:
                    await ctx.guild.voice_client.disconnect()
                    channel = ctx.message.author.voice.channel
                    voice = await channel.connect()
                    print("moving to channel of", ctx.author.name)
                    return voice
                voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
                channel = ctx.message.author.voice.channel
                return voice
            joinmessage(ctx)
            
async def doguildcheck(ctx):
    '''Checks your server id for connecting'''
    guildcheck = int(ctx.guild.id)
    if guildcheck != SERVERID:
        print("I do not have access to this guild, please check your .env file and update your guild ID.")
    return True if guildcheck == SERVERID else False

@bot.command(pass_context=True, name="stop", help="Stops the current sound clip or loop")
async def _stop(ctx):
    if ctx.author.voice:
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        voice.stop()
        botresponse = "stop"
        errormessage = await getbotresponse(botresponse)
        botmessage = await ctx.send(errormessage)
        await asyncio.sleep(5)
        await botmessage.delete()
    else:
        botresponse = "usernotconnected"
        errormessage = await getbotresponse(botresponse)
        botmessage = await ctx.send(errormessage)
        await asyncio.sleep(5)
        await botmessage.delete()

async def getbotresponse(botresponse):
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
                case _:
                    return("It doesn't work I guess, beats me.")

async def joinmessage(ctx):
    '''Error on attempting to join channel'''
    botresponse = "usernotconnected"
    errormessage = await getbotresponse(botresponse)
    botmessage = await ctx.send(errormessage)
    print("user is not in a channel or bot does not have access")
    await asyncio.sleep(5)
    await botmessage.delete()
@bot.event
async def on_command_error(ctx, error):
    '''Default error catch'''
    if isinstance(error, CommandNotFound):
        return
    raise error

bot.run(TOKEN)
