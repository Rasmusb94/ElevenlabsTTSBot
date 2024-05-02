import asyncio
import random
import json
import os
import discord
import requests
import functions.getBotResponse as getBotResponse
import functions.sendErrorMessage as sendErrorMessage
import functions.getFilePath as getFilePath
import functions.sendBotMessage as sendBotMessage
import functions.connectToVoice as connectToVoice
import functions.getBotVoice as getBotVoice
import functions.sendRequest as sendRequest
import functions.joinLeaveSounds as joinLeaveSounds
import functions.playVoice as playVoice

from discord.ext import commands
from discord.ext.commands import CommandNotFound

try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    botdata_path = os.path.join(script_dir, 'botdata.json')
    with open(botdata_path, 'r') as jsonbotdata:
        botdata = json.load(jsonbotdata)
    TOKEN = botdata['discord_token']
    PREFIX = botdata['command_prefix']
    SERVERID = botdata['discord_server_id']
    ROLEID = botdata['role_id']
    LEAVEJOINTTS = botdata.get('leave_join_sounds', False) == 'True'
    LEAVEJOINSTABILITY = round(random.uniform(0.01, 0.2), 2) if botdata['leave_join_stability'] == "random" else botdata['leave_join_stability']
    intents = discord.Intents.all()
    intents.members = True
    HELPDESCRIPTION = "These are the currently available commands!"
    TTSMODEL = 'eleven_multilingual_v2'
except Exception as e:
    print(f"There was an issue whilst reading the botdata file: {e}")

try:
    voicedata = json.loads(requests.get("https://api.elevenlabs.io/v1/voices").content)['voices']
except Exception as e:
    print(f"Something went wrong when getting available voices from elevenlabs: {e}")

try:
    bot = commands.Bot(command_prefix=PREFIX,
                    intents=intents,
                    case_insensitive=True,
                    help_command=commands.DefaultHelpCommand(no_category = 'Commands'),
                    description=HELPDESCRIPTION)
except Exception as e:
    print(f"Could not create the bot: {e}")

@bot.event
async def on_ready():
    '''Connects the bot to Discord'''
    print(f"{bot.user.name} has connected to Discord!")
    statusmessage = "Type " + PREFIX + "help"
    activity = discord.Game(statusmessage)
    await bot.change_presence(status=discord.Status.online, activity=activity)

@bot.command(pass_context=True, name="random", help="Takes a random voice and stability, just type " + PREFIX + "'random Hello World'")
async def _random(ctx, *message):
    if (voice := await connectToVoice.connectToVoice(ctx, bot)) is not None:
        try:
            botmessage = " ".join(message[:])

            ttsvoice, voiceid = await getBotVoice.getRandomVoice(voicedata)
            stability = await getBotVoice.getRandomStability()
            response = await sendRequest.getSoundclip(voiceid, botmessage, TTSMODEL, stability)
            audiofile = await getFilePath.getFilePath(ctx.message.author.name, response)

            await playVoice.playVoice(ttsvoice, botmessage, ctx.message.author.name, voice, audiofile)
            await sendBotMessage.sendPlayingMessage(ctx, ttsvoice, str(stability), botmessage)
        except (ValueError, UnboundLocalError) as error:
            botresponse = "valerror"
            errormessage = await getBotResponse.getBotResponse(botresponse)
            await sendErrorMessage.sendValueErrorMessage(errormessage, ctx, error)
        except Exception as error:
            botresponse = ""
            errormessage = await getBotResponse.getBotResponse(botresponse)
            await sendErrorMessage.sendValueErrorMessage(errormessage, ctx, error)

@bot.command(pass_context=True, name="tts", help=f"Use tts Voice message, example: '{PREFIX}tts Adam 50 Hello World' param: <Voice or random> <Stability 1-100> <Message>")
async def _tts(ctx, 
               name: str = commands.parameter(description="The name of the voice you want to use"), 
               stability: str = commands.parameter(description="The stability of the voice, a number between 0-100"), 
               *message):
    if (voice := await connectToVoice.connectToVoice(ctx, bot)) is not None:

        try:
            botmessage = " ".join(message[:])

            ttsvoice, voiceid = await getBotVoice.checkRandomVoice(name.capitalize(), voicedata, ctx)
            stability = await getBotVoice.setStability(stability)
            response = await sendRequest.getSoundclip(voiceid, botmessage, TTSMODEL, stability)
            audiofile = await getFilePath.getFilePath(ctx.message.author.name, response)

            await playVoice.playVoice(ttsvoice, botmessage, ctx.message.author.name, voice, audiofile)
            await sendBotMessage.sendPlayingMessage(ctx, ttsvoice, str(stability), botmessage)

        except (ValueError, UnboundLocalError) as error:
            botresponse = "valerror"
            errormessage = await getBotResponse.getBotResponse(botresponse)
            await sendErrorMessage.sendValueErrorMessage(errormessage, ctx, error)
        except Exception as error:
            botresponse = ""
            errormessage = await getBotResponse.getBotResponse(botresponse)
            await sendErrorMessage.sendValueErrorMessage(errormessage, ctx, error)

@bot.command(pass_context=True, name="custom", help=f"Custom voice tts, example: '{PREFIX}custom Adam 50 Hello World' param: <Voice or random> <Stability 1-100> <Message>")
async def _custom(ctx, 
               name: str = commands.parameter(description="The name of the voice you want to use"), 
               stability: str = commands.parameter(description="The stability of the voice, a number between 0-100"), 
               *message):
    if (voice := await connectToVoice.connectToVoice(ctx, bot)) is not None:

        try:
            botmessage = " ".join(message[:])
            ttsvoice, voiceid = await getBotVoice.getCustomVoice(name)
            if ttsvoice == "" or voiceid == "":
                raise ValueError("Couldn't find a custom voice with the requested name. Please make sure the voice has been added to the customvoices.json file and the VoiceLabs library on your Elevenlabs profile.")
            stability = await getBotVoice.setStability(stability)
            response = await sendRequest.getSoundclip(voiceid, botmessage, TTSMODEL, stability)
            audiofile = await getFilePath.getFilePath(ctx.message.author.name, response)

            await playVoice.playVoice(ttsvoice, botmessage, ctx.message.author.name, voice, audiofile)
            await sendBotMessage.sendPlayingMessage(ctx, ttsvoice, str(stability), botmessage)

        except (ValueError, UnboundLocalError) as error:
            botresponse = "valerror"
            errormessage = await getBotResponse.getBotResponse(botresponse)
            await sendErrorMessage.sendValueErrorMessage(errormessage, ctx, error)
        except Exception as error:
            botresponse = ""
            errormessage = await getBotResponse.getBotResponse(botresponse)
            await sendErrorMessage.sendValueErrorMessage(errormessage, ctx, error)

@bot.command(pass_context=True, name="unstable", help="TTS with 0 stability, for making crazy stuff! '!tts Adam Hello World' param: <Voice or random> <Message>")
async def _unstable(ctx, 
                    name: str = commands.parameter(description="The name of the voice you want to use. Or put Random."), 
                    *message):
    if (voice := await connectToVoice.connectToVoice(ctx, bot)) is not None:
        try:
            botmessage = " ".join(message[:])

            ttsvoice, voiceid = await getBotVoice.checkRandomVoice(name.capitalize(), voicedata, ctx)
            response = await sendRequest.getSoundclip(voiceid, botmessage, TTSMODEL, "0.00")
            audiofile = await getFilePath.getFilePath(ctx.message.author.name, response)

            await playVoice.playVoice(ttsvoice, botmessage, ctx.message.author.name, voice, audiofile)
            await sendBotMessage.sendPlayingMessage(ctx, ttsvoice, round(random.uniform(0.01, 0.20),2), botmessage)
        except (ValueError, UnboundLocalError) as error:
            botresponse = "valerror"
            errormessage = await getBotResponse.getBotResponse(botresponse)
            await sendErrorMessage.sendValueErrorMessage(errormessage, ctx, error)
        except Exception as error:
            botresponse = ""
            errormessage = await getBotResponse.getBotResponse(botresponse)
            await sendErrorMessage.sendValueErrorMessage(errormessage, ctx, error)

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
                audiofile = await joinLeaveSounds.checkEasterEgg("leave")
                if audiofile == "":
                    username = await joinLeaveSounds.getUsername(member)
                    botmessage = await joinLeaveSounds.getLeaveMessage(username)
                    ttsvoice, voiceid = await getBotVoice.getRandomVoice(voicedata)
                    response = await sendRequest.getSoundclip(voiceid, botmessage, TTSMODEL, LEAVEJOINSTABILITY)
                    audiofile = await getFilePath.getFilePath(member.name + "_leave", response)
                
                await playVoice.playLeaveVoice(ttsvoice, botmessage, member.name, voice, audiofile)
            #joining sounds
            elif before.channel is None and after.channel is voice.channel or before.channel is not voice.channel and after.channel is voice.channel:
                
                audiofile = await joinLeaveSounds.checkEasterEgg("join")
                if audiofile == "":
                    username = await joinLeaveSounds.getUsername(member)
                    botmessage = await joinLeaveSounds.getJoinMessage(username)
                    ttsvoice, voiceid = await getBotVoice.getRandomVoice(voicedata)
                    response = await sendRequest.getSoundclip(voiceid, botmessage, TTSMODEL, LEAVEJOINSTABILITY)
                    audiofile = await getFilePath.getFilePath(member.name + "_join", response)

                await playVoice.playJoinVoice(ttsvoice, botmessage, member.name, voice, audiofile)
        except (ValueError, UnboundLocalError, AttributeError, TypeError, Exception) as e:
            print(f"There was an error with leave/join sounds: {e}")

@bot.event
async def on_message(message):
    '''For removing messages sent to the bot'''
    await bot.process_commands(message)
    if message.content.startswith(PREFIX):
        await asyncio.sleep(15)
        await message.delete()

@bot.command(pass_context=True, name="voices", help="Displays the available voices for use")
async def _voices(ctx):
    await sendRequest.getAvailableVoices(ctx, voicedata)

@bot.command(pass_context=True, name="quota", help="Displays the remaining quota for use")
async def _quota(ctx):
    await sendRequest.getQuota(ctx)

@bot.command(pass_context=True, name="stop", help="Stops the current sound clip or loop")
async def _stop(ctx):
    await playVoice.stopVoice(ctx, bot)
    
        
@bot.command(pass_context=True, name="join", help="Joins the voice channel")
async def _join(ctx):
    await connectToVoice.connectToVoice(ctx, bot, "joincommand")

@bot.command(pass_context=True, name="leave", help="Leaves the voice channel")
async def _leave(ctx):
    await connectToVoice.leaveVoice(ctx)
    
@bot.event
async def on_command_error(error):
    '''Default error catch'''
    if isinstance(error, CommandNotFound):
        return
    raise error
    
try:
    bot.run(TOKEN)
except Exception as e:
    print("Bot couldn't run: {e}")