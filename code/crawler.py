import discord

def handle_user_messages(msg) ->str:
    message = msg.lower() #Converts all inputs to lower case
    if('github.com/yoayo112/change-the-game/' in message):
        return 'I see activity in change-the-game'
    else:
        return 'I dont see activity'

async def processMessage(message, user_message):
    try:
        botfeedback = handle_user_messages(user_message)
        if(not botfeedback):
            return
        else:
            await message.channel.send(botfeedback)
    except Exception as error:
        print(error)

def runBot():
    
    #Paste token here
    #discord_token

    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print({client.user}, 'is live')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        await processMessage(message, message.content)

    client.run(discord_token)