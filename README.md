<h1>ElevenlabsTTSBot</h1>
A local TTS bot using AI for voice generation with <a href="https://elevenlabs.io/speech-synthesis">ElevenLabs Speech Synthesis</a>!<br>
<h2>Video guide coming soon!</h2>
<!---<a href="http://www.youtube.com/watch?feature=player_embedded&v=LBQEurX-MUc" target="_blank">
 <img src="http://img.youtube.com/vi/LBQEurX-MUc/mqdefault.jpg" alt="Video Installation Guide" width="240" height="160" border="10" />
</a>--->
<h2>First Things First</h2>
Download the <a href="https://github.com/Rasmusb94/ElevenlabsTTSBot/releases">latest release of the ElevenlabsTTSBot</a> and extract the folder to your preferred location.
<h2>Creating Your Bot</h2>
Go to <a href="https://discord.com/developers/applications">the Discord Developer Portal</a>.
<ul>
  <li>Click New Application</li>
  <li>Set a name for your bot and accept the T&C</li>
  <li>Set an avatar for your bot if you like</li>
  <li>Go to the "Bot" tab</li>
  <li>Scroll down to "Privileged Gateway Intents" and enable all three options</li>
  <li>Scroll back up and select "Reset Token" to show your bot token, you will need this for the bot data file</li>
  <li>Invite your bot by going to - discordapp.com/oauth2/authorize?client_id={CLIENT_ID}&scope=bot&permissions=35184408799232
Replace the {CLIENT_ID} including the brackets with the "Application ID" found under the "General Information" tab in your Application settings.</li>
  <li>Select which server you want to add the bot to.</li>
</ul>
<h2>Creating an ElevenLabs Account</h2>
You are required to make an ElevenLabs account to run this bot. Go to <a href="https://elevenlabs.io/speech-synthesis">ElevenLabs website</a> and create your free account. Free users get a 10,000 character quota per month, which may last anywhere from the entire month to 10 minutes depending on your friend group...
<h2>Bot Data Information</h2>
Open the botdata.json file using your text editor of choice. Any notepad should work just fine.
Note: Make sure NOT TO add OR remove any " or , characters in the file.
<ul>
  <li>Update the discord_token field using the token you just got from the developer Portal</li>
  <li>Enabling developer mode to get the server ID.
If you cannot find the ID of your server, you must go to user settings, scroll to "Advanced" under "App Settings" and enable Developer mode.
After doing this, simply right click your server and select "Copy Server ID"</li>
  <li>Update the discord_server_id field with the ID of your server</li>
  <li>Update the elevenlabs_api_key field using the API Key found on your <a href="https://elevenlabs.io/speech-synthesis">Elevenlabs.io</a> profile.
  <li>(Optional) Feel free to edit the other fields but make sure to keep the format as is</li>
</ul>
<h2>Dependencies</h2>
<h3>FFMpeg</h3>
<ul>
  <li>Go to www.github.com/BtbN/FFmpeg-Builds/releases and download the latest gpl build for your system</li>
  <li>Open the Zipped folder and extract the "bin" folder to your preferred location, for example in the DiscordMadnessboard directory</li>
  <li>Open Windows System Properties and click the "Advanced" tab, and go to "Environment Variables"</li>
  <li>Click the "Path" System variable, "Edit", and "New". Here you will need to add the path to your /bin folder, which can quickly be found by right clicking the folder and going to properties</li>
  <li>Click OK and exit System Properties, FFMpeg is now ready to be used</li>
</ul>
<h3>Python</h3>
Should work with Python 3.10 + but only tested with 3.11
<ul>
  <li>Go to <a href="https://python.org/downloads/">the Python website</a> and download the latest version of Python 3.11</li>
  <li>When installing, make sure to tick the "Add python.exe to PATH" box, or otherwise do the same as you did for FFMpeg by manually adding Python to path</li>
</ul>
<h3>Python Libraries</h3>
<ul>
  <li>Open Windows PowerShell as an Administrator</li>
  <li>Type "pip install discord"</li>
  <li>Type "pip install mutagen"</li>
  <li>Type "pip install PyNaCl"</li>
  <li>Type "pip install elevenlabs"</li>
</ul>
This should install the required libraries to Python, if it does not work please check your Python installation completed correctly, or use another method such as choco to install the libraries.

<h2>Running the Bot</h2>
That's it!<br>
You can now run the TTS Bot by opening the bot.py file with Python. For troubleshooting you can run the file in debug mode using your developing environment of choice, such as VS Code.
<h3>Commands</h3>
The currently available commands are as follows:
<ul>
  <li>quota - Displays your available character count </li>
  <li>voices - Displays the available AI voices</li>
  <li>unstable - tts with 0 stability for simplicity - !unstable (voice) (ttsmessage) | (voicename or random) (string)</li>
  <li>tts - tts with selected voice and stability - !tts (voice) (stability) (ttsmessage) | (voicename or random) (num 1-100) (string)</li>
  <li>random - uses a random voice with random stability - !random (ttsmessage) | (string)</li>
  <li>help</li>
  <li>stop</li>
  <li>join</li>
  <li>leave</li>
</ul>

<h2>Activating Leave & Join sounds</h2>
The bot is also able to welcome and say goodbye to people joining and leaving voice chat! To enable, follow these steps:
<ul>
  <li>Create a new role (or use an old one) in your Discord guild under "Server Settings" - "Roles"</li>
  <li>Add users who will be welcomed to the role by clicking them, selecting "Roles" and applying the role to them</li>
  <li>Copy the Role ID from the Roles section in your server settings</li>
  <li>Update the "role_id" line in the botdata.json file with your role ID number</li>
  <li>Set the "leave_join_sounds" line to "True"</li>
  <li>(Optional) Change the stability to anything between 0.00 and 1.00 depending on preference! You can also add or remove bits that the bot may say using the "joinmessagesprefix" list etc.</li>
</ul>
