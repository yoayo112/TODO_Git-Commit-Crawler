#Author: Sky Vercauteren
#Date: March 31, 2024
# Crawler.py. Uses the github API to find all the 'TODO' comments in a repo and send them to discord

import requests
from urllib.request import urlopen
import json
import discord


#Everyone screaming dont put your token in a public repo!!
#Cool but then how tf am I supposed to validate? -ugh google this.

#For now I guess just paste discord server token here when you want to run the bot. oh I guess I also need to auth github.

repoPath = 'yoayo112/Change-The-Game/'
#Something like this???


#borrowed this from someone online using cli to get blob code.
def create_github_rawurl(url):
    # reformat the URL so the URL only prints the raw code
    url = url.replace("api","raw")
    url = url.replace("github","raw.githubusercontent")
    url = url.replace("blob/","")
    return url


#handles the message content and returns a response string to the async event manager
def handle_user_messages(msg) ->str:
    message = msg.lower() #Converts all inputs to lower case
    if(repoPath.lower() in message):

        #ok so it sees a commit. Now for the fun part.
        
        #get into github ourselves.
        headers = {'Authorization': 'token ' + gitToken }

        #creating a search query to give to git hubs very convenient search api
        query = "TODO+in:file+extension:cs+repo:yoayo112/Change-The-Game"
        todolist = []
        contents = requests.get('http://api.github.com/search/code?q='+query, headers=headers).json()
        hits = contents["items"]
        for hit in hits: #json file .items is the list of results.
            #  :(
            #  turns out, all Im gonna get from this is another url 
            #So I guess we have to step into it?
            githubURL = create_github_rawurl(hit["html_url"])
            print(githubURL)
            try:
                #try stepping into the diff html
                response = urlopen(githubURL)
                # read the code into a string
                code = response.read().decode('utf-8')
                #if it worked .. we should have a bigass string
                lines = code.split("\n")
                for line in lines:
                    if "TODO" in line:
                        todolist.append(line)
                
            except: 
                print("fail!!!")
                pass
			    # raise Exception, "failed to open modified GitHub URL " + githubURL

        #in theory todoList now contains all the hits of TODO
        return todolist
    

#on message event passes content to handler -> passes the reponse back to discord.
async def process_message(message, userMessage):
    try:
        response = handle_user_messages(userMessage)
        if(not response):
            return
        else:
            #-- see if you can set what channel it posts in!!
            #-- see if you can call the other todo bot???
            post = ''
            for line in response:
                post += line + "\n"

            await message.channel.send(post)
            
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
        await process_message(message, message.content) #if you see a message -> see if its a git push.

    client.run(discordToken)