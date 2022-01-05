import discord
import requests

from discord.ext import commands

client = commands.Bot(command_prefix = "!") # Setting the command prefix for the bot, can be anything. 

def varRequest(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.9",
        # Using headers to appear as a real browser 
    }
    response = requests.get(url, headers=headers)
    respjson = response.json()
    variants = {} 
    if response.status_code == 200: # Good request 
        
        for i in respjson["product"]["variants"]: # going into the results of products, then the results of variants
            # then looking for id and option 1, which are the variant and the size respectively. 
            variants[i["id"]] = i["option1"]
        return variants
    else:
        return None

def scrapeVars(url):
    if "variant=" not in url and url[-5:] == ".json": 
        return varRequest(url)
    elif "variant=" in url and not (url[-5:] == ".json"): 
        prodURL = url[:len(url)-23]+".json"
        return varRequest(prodURL)
    elif "variant=" in url and url[-5:] == ".json":
        prodURL = url[:len(url)-28]+".json"
        return varRequest(prodURL)
    elif "variant=" not in url and url[-5:] != ".json":
        prodURL = url+".json"
        return varRequest(prodURL)
    else:
        return None

    #User can pass in different forms of the product url
    #https://kith.com/collections/mens-footwear-sneakers/products/nkdj0717-001.json - case 1, delete the .json (5 characters)
    #https://kith.com/collections/mens-footwear-sneakers/products/nkdj0717-001?variant=39249927405696 - case 2, delete the ?variant=39249927405696 (23 characters)
    #https://kith.com/collections/mens-footwear-sneakers/products/nkdj0717-001?variant=39249927405696.json - case 3, delete the ?variant=39249927405696.json (28 characters)
    #https://kith.com/collections/mens-footwear-sneakers/products/nkdj0717-001 - case 4. 

@client.event

async def on_ready(): 
    print("On") # When you see "On" after running, the bot is online 

@client.command()
async def variants(ctx, *, url): 
    await ctx.send("```" + str(scrapeVars(url)) + "```")   
      

client.run("TOKEN") # Replace "TOKEN" with your own bot token from the Discord developer portal