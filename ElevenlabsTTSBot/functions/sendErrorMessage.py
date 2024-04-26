import asyncio
import functions.getBotResponse as getBotResponse
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



async def sendErrorMessage(errormessage, ctx, error):
    try:
        botmessage = await ctx.send(errormessage)
        print(f"Error: {error}")
        await asyncio.sleep(5)
        await botmessage.delete()
    except Exception as e:
        print(f"Couldn't send message: {e}")

async def sendValueErrorMessage(errormessage, ctx, error):
    try:
        botmessage = await ctx.send(errormessage)
        print(f"Value Error: {error}")
        await asyncio.sleep(5)
        await botmessage.delete()
    except Exception as e:
        print(f"Couldn't send message: {e}")

async def sendJoinErrorMessage(ctx):
    try:
        botresponse = "usernotconnected"
        errormessage = await getBotResponse.getBotResponse(botresponse, RUDE_BOT, PREFIX)
        botmessage = await ctx.send(errormessage)
        print("user is not in a channel or bot does not have access")
        await asyncio.sleep(5)
        await botmessage.delete()
    except Exception as e:
        print(f"Couldn't send message: {e}")