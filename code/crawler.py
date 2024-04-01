#Author: Sky Vercauteren
#Date: March 31, 2024
# Crawler.py. Uses the github API to find all the 'TODO' comments in a repo and send them to discord

from github import Github # from a github API wrapper library called pyGithub. just for lazy mf's like me.
from github import Auth
import discord

#Everyone screaming dont put your token in a public repo!!
#Cool but then how tf am I supposed to validate? -ugh google this.

#For now I guess just paste discord server token here when you want to run the bot. oh I guess I also need to auth github.
#discordToken = 
#gitToken = 
repoPath = 'yoayo112/Change-The-Game/'
#Something like this???

#handles the message content and returns a response string to the async event manager
def handle_user_messages(msg) ->str:
    message = msg.lower() #Converts all inputs to lower case
    if(repoPath.lower() in message):

        #ok so it sees a commit. Now for the fun part.
        
        #get into github ourselves.
        auth = Auth.Token(gitToken)
        git = Github(auth=auth)

        #creating a search query to give to git hubs very convenient search api
        query = "TODO+in:file+language:csharp+repo:"+repoPath
        contents = git.search_code(query) # fingers crossed the other params where optional??
        todolist = []
        for hit in contents.items #json file .items is the list of results.
            todolist.append(hit.textMatches) #within each.item is info about the file\creator etc. we just want .textMatches

        #in theory todoList now contains all the hits of TODO
        return todoList



#on message event passes content to handler -> passes the reponse back to discord.
async def process_message(message, userMessage):
    try:
        response = handle_user_messages(userMessage)
        if(not response):
            return
        else:
            #-- see if you can set what channel it posts in!!
            #-- see if you can call the other todo bot???
            await message.channel.send(response) #tbh I have no idea how discord will handle an array.
    except Exception as error:
        print(error)




# called by main.py to start things off. listens for events.
def runBot():

    #not sure I fully understand intents, but they are permissions set by discord. 
    #in addition to the declaration below, I had to grant message_content intent permission in the discord developer application page.
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print({client.user}, 'is live')

    @client.event
    async def on_message(message):
        if message.author == client.user: #don't respond to yourself, and get stuck in infinity.
            return
        await processMessage(message, message.content) #if you see a message -> see if its a git push.

    client.run(discordToken)