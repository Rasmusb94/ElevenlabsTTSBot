import discord
import functions.sendBotMessage as sendBotMessage
import functions.getBotResponse as getBotResponse

async def playVoice(ttsvoice, botmessage, ttsuser, voice, audiofile):
    print(f"{ttsvoice} says: {botmessage} as requested by {ttsuser}.")
    await stopStart(voice, audiofile)

async def playJoinVoice(ttsvoice, botmessage, ttsuser, voice, audiofile):
    print(f"{ttsuser} is joining! {ttsvoice} says: {botmessage}")
    await stopStart(voice, audiofile)

async def playLeaveVoice(ttsvoice, botmessage, ttsuser, voice, audiofile):
    print(f"{ttsuser} just left! {ttsvoice} says: {botmessage}")
    await stopStart(voice, audiofile)

async def stopStart(voice, audiofile):
    try:
        voice.stop()
        voice.play(audiofile)
    except Exception as e:
        print(f"Couldn't play sound file: {e}")

async def stopVoice(ctx, bot):
    try:
        if ctx.author.voice:
            voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
            if voice.is_playing():
                voice.stop()
                botresponse = "stop"
            else:
                botresponse = "notspeaking"
            botmessage = await getBotResponse.getBotResponse(botresponse)
            await sendBotMessage.sendBotMessage(ctx, botmessage)
        else:
            botresponse = "usernotconnected"
            botmessage = await getBotResponse.getBotResponse(botresponse)
            await sendBotMessage.sendBotMessage(ctx, botmessage)
    except Exception as e:
        print(f"The bot is unstoppable!! {e}")