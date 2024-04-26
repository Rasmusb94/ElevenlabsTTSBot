import functions.doGuildCheck as doGuildCheck
import functions.sendBotMessage as sendBotMessage
import functions.getBotResponse as getBotResponse
import discord

async def connectToVoice(ctx, bot, *join):
    '''For connecting the bot to voice chat'''
    try:
        if await doGuildCheck.doGuildCheck(ctx) is True:
            if ctx.voice_client is None:
                if ctx.author.voice:
                    channel = ctx.message.author.voice.channel
                    voice = await channel.connect()
                    print("joining voice channel of", ctx.author.name)
                    return voice
                else:
                    botresponse = "usernotconnected"
                    errormessage = await getBotResponse.getBotResponse(botresponse)
                    await sendBotMessage.sendBotMessage(ctx, errormessage)
            else:
                if ctx.author.voice:
                    if ctx.voice_client.channel != ctx.message.author.voice.channel:
                        await ctx.guild.voice_client.disconnect()
                        channel = ctx.message.author.voice.channel
                        voice = await channel.connect()
                        print("moving to channel of", ctx.author.name)
                    if join and join[0] is not None:
                        if join[0] == "joincommand" and ctx.voice_client.channel == ctx.message.author.voice.channel:
                            botresponse = "alreadyjoined"
                            errormessage = await getBotResponse.getBotResponse(botresponse)
                            await sendBotMessage.sendBotMessage(ctx, errormessage)
                    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
                    return voice
                else:
                    botresponse = "usernotconnected"
                    errormessage = await getBotResponse.getBotResponse(botresponse)
                    await sendBotMessage.sendBotMessage(ctx, errormessage)
    except Exception as e:
        print(f"Could not get the user voice channel: {e}")

async def leaveVoice(ctx):
    try:
        if ctx.author.voice == None:
            botresponse = "usernotconnected"
            errormessage = await getBotResponse.getBotResponse(botresponse)
            await sendBotMessage.sendBotMessage(ctx, errormessage)
        else:
            if ctx.voice_client != None:
                await ctx.guild.voice_client.disconnect()
                botresponse = "leaving"
                response = await getBotResponse.getBotResponse(botresponse)
                await sendBotMessage.sendBotMessage(ctx, response)
            else:
                botresponse = "notconnected"
                errormessage = await getBotResponse.getBotResponse(botresponse)
                await sendBotMessage.sendBotMessage(ctx, errormessage)
    except Exception as e:
        print(f"Something went wrong when trying to leave the channel: {e}")