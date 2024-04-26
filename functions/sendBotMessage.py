import asyncio

async def sendBotMessage(ctx, botmessage):
    try:
        botmessage = await ctx.send(botmessage)
        await asyncio.sleep(10)
        await botmessage.delete()
    except Exception as e:
        print(f"Couldn't send message: {e}")

async def sendPlayingMessage(ctx, ttsvoice, stabstr, botmessage):
    try:
        stability = float(stabstr)
        infomessage = f"Voice: {ttsvoice.capitalize()}\nStability: {int(stability * 100)}%\nMessage: {botmessage}"
        botmessage = await ctx.send(infomessage)
        await asyncio.sleep(15)
        await botmessage.delete()
    except Exception as e:
        print(f"Couldn't send message: {e}")

async def sendVoiceNotFoundMessage(voicename, ctx):
    try:
        infomessage = f"Couldn't find a voice named {voicename}"
        botmessage = await ctx.send(infomessage)
        await asyncio.sleep(15)
        await botmessage.delete()
    except Exception as e:
        print(f"Couldn't send message: {e}")