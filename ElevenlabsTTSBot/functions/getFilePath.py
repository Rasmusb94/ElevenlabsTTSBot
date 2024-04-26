import os
import json
CHUNK_SIZE = 1024
from discord import FFmpegPCMAudio

try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    botdata_path = os.path.join(script_dir, '..', 'botdata.json')

    with open(botdata_path, 'r') as jsonbotdata:
        botdata = json.load(jsonbotdata)
        EXTENSION = ".mp3"
        SOUNDFILEDIR = 'soundfiles/'
except Exception as e:
    print(f"Could not read botdata.json file: {e}")

async def getFilePath(ttsuser, response):
    filename = ttsuser + EXTENSION
    filepath = SOUNDFILEDIR + filename
    filepath = await checkFilePath(ttsuser, filepath)
    try:
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                if chunk:
                    f.write(chunk)
        audiofile = FFmpegPCMAudio(filepath)
    except Exception as e:
        print(f"Something went wrong when getting the file path: {e}")
    return audiofile

async def checkFilePath(ttsuser, filepath):
    counter = 2
    try:
        while os.path.exists(filepath):
            filepath = SOUNDFILEDIR + ttsuser + str(counter) + EXTENSION
            counter += 1
    except Exception as e:
        print(f"Couldn't check the system for matching files: {e}")
    return filepath