import json
import os

try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    botdata_path = os.path.join(script_dir, '..', 'botdata.json')

    with open(botdata_path, 'r') as jsonbotdata:
        botdata = json.load(jsonbotdata)
    SERVERID = botdata['discord_server_id']
except Exception as e:
    print(f"Could not read botdata.json file: {e}")

async def doGuildCheck(ctx):
    '''Checks your server id for connecting'''
    try:
        guildcheck = int(ctx.guild.id)
        if guildcheck != SERVERID:
            print("I do not have access to this guild, please check your .env file and update your guild ID.")
        return True if guildcheck == SERVERID else False
    except Exception as e:
        print(f"Couldn't check guild ID of user: {e}")