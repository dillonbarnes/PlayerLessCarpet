import discord
import discord.ext 
from discord.ext import commands 
import discord.utils
import os
import requests 
import json
import random
import datetime
import time
from discord.ext import tasks
import asyncio
import sys
from keep_alive import keep_alive
from discord.ext.commands import has_permissions
from discord.ext.commands import MissingPermissions, BadArgument

client = commands.Bot(command_prefix = "?")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please pass in all requirements :rolling_eyes:.')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You dont have all the requirements :angry:")

with open('reports.json', encoding='utf-8') as f:
  try:
    report = json.load(f)
  except ValueError:
    report = {}
    report['users'] = []

async def ch_pr():
    await client.wait_until_ready()
    
    while not client.is_closed():
        statuses = [
            "?commands",
            f"Serving {len(client.users)} users",
            "Playing 0 player Minecraft."
        ]
        status = random.choice(statuses)

        await client.change_presence(status=discord.Status.online, activity=discord.activity.Game(name = status))
        await asyncio.sleep(100)  

    if client.is_closed():
        print("Bot offline")

@client.command()
async def restart(ctx):
  if ctx.author.id == 569938612435681282:
    await ctx.send("Restarting/ending session DillonB07")
    print("Restarting...")
    os.execl(sys.executable, sys.executable, *sys.argv)
  if ctx.author.id == 723880504985911318:
    await ctx.send("Restarting/ending session MineAndDine96")
    print("Restarting...")

@client.command()
async def users(ctx):
  await ctx.channel.send(f"I am serving {len(client.users)} users")

# The below code bans player.
@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
  await member.ban(reason=reason)
  await ctx.send(f'User {member} has been banned')

# The below code kicks player
@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
  await member.kick(reason=reason)
  await ctx.send(f'User {member} has been kicked')

@client.command()
async def clear(ctx, amount=2): 
  if commands.has_permissions(manage_messages=True): 
   await ctx.channel.purge(limit=amount)                                     
   await ctx.send(f'I have deleted {amount} messages!')                         
   return
  if commands.has_permissions(manage_messages=False):
    await ctx.send('You are not allowed to run that command!')

@client.command()
@commands.has_permissions(manage_guild=True)
async def mute(ctx, member: discord.Member = None):
  guild = ctx.guild
  for role in guild.roles:
    if role.name == "Muted":
      await member.add_roles(role)
      await ctx.send("The user has been muted")

@client.command()
@commands.has_permissions(manage_guild=True)
async def unmute(ctx, member: discord.Member = None):
  guild = ctx.guild
  for role in guild.roles:
    if role.name == "Muted":
      await member.remove_roles(role)
      await ctx.send("The user has been unmuted")

@client.command()
@has_permissions(manage_roles=True, ban_members=True)
async def warn(ctx,user:discord.User,*reason:str):
  if not reason:
    await ctx.channel.send("Please provide a reason")
    return
  reason = ' '.join(reason)
  for current_user in report['users']:
    if current_user['name'] == user.name:
      current_user['reasons'].append(reason)
      break
  else:
    report['users'].append({
      'name':user.name,
      'reasons': [reason,]
    })
  with open('reports.json','w+') as f:
    json.dump(report,f)

@client.command()   #provides a link to SciCraft-Discord
async def scicraft(ctx):
  embed=discord.Embed(title="Scicraft", color=0xff0000)
  embed.set_author(name=ctx.message.author) 

  embed.add_field(name="Discord:", value="https://discord.gg/scicraft", inline=False)

  embed.add_field(name="Reddit: ", value="https://www.reddit.com/r/SciCraft/", inline=False)

  embed.add_field(name="Twitter: ", value="http://twitter.com/scicraft_", inline=False)

  await ctx.send(embed=embed) 

@client.command()   #provides a Link to Aternos.org
async def aternos(ctx):
  embed=discord.Embed(color=0xff0000)
  embed.set_author(name=ctx.message.author) 
  embed.add_field(name="Aternos:", value="Aternos free server hosting. https://aternos.org", inline=False)
  await ctx.send(embed=embed) 

@client.command()   #Provides Download links
async def download(ctx):
  embed=discord.Embed(title="Download Carpet mod without /player",color=0xff0000)
  embed.set_author(name=ctx.message.author) 

  embed.add_field(name="Curseforge: ", value="Download on Curseforge https://www.curseforge.com/minecraft/mc-mods/carpet-without-player", inline=False)

  embed.add_field(name="GitHub: ", value="Download Source Code on GitHub https://github.com/MineAndDine96/fabric-carpet-no-player/tree/main", inline=False)
  await ctx.send(embed=embed) 

@client.command()   #Sends the commands of the bot
async def commands(ctx):
  embed=discord.Embed(title="Help for the Carpet Mod without /player Help Bot", description="Welcome to the help! Please take a look at the command below and use what you need!", color=0xff0000)
  embed.set_author(name="DillonB07")
  embed.add_field(name="?scicraft", value="Sends a link to the Scicraft Discord, Reddit and.", inline=False)
  embed.add_field(name="?aternos", value="Sends a link to Aternos website.", inline=False)
  embed.add_field(name="?download", value="Provides a link to download the Carpet Mod without /player.", inline=False)
  embed.add_field(name="?carpet", value="Sends a link for the Official Carpet Mod.", inline=False)
  embed.add_field(name="?invite", value="Sends an invite link for this server.", inline=False)
  embed.add_field(name="?suggest", value="Suggest something for the mod. Not the server the mod. If it a good suggestion we will try and add it.", inline=False)
  embed.add_field(name="?bot", value="Sends the bot invite link.", inline=False)
  embed.add_field(name="?scripts", value="Sends information on setting up Scarpet scripts.", inline=False)
  await ctx.send(embed=embed)

@client.command()    #Provides information on the Official Carpet Mod
async def carpet(ctx):
  embed=discord.Embed(title="Official Carpet Mod", color=0xff0000)
  embed.set_author(name=ctx.message.author) 
  embed.add_field(name="gnembon on CurseForge:", value="https://www.curseforge.com/members/gnembon/projects", inline=False)
  embed.add_field(name="gnembon on YouTube:", value="https://www.youtube.com/c/gnembon/", inline=False)
  embed.add_field(name="Carpet Mod on CurseForge", value="https://www.curseforge.com/minecraft/mc-mods/carpet", inline=False)
  embed.add_field(name="Carpet Mod on GitHub", value="https://github.com/gnembon/carpetmod", inline=False)
  await ctx.send(embed=embed)

@client.command()   #provides an invite link to Discord Server
async def invite(ctx):
  embed=discord.Embed(title="Invite People to this Discord Server", color=0xff0000)
  embed.set_author(name=ctx.message.author)
  embed.add_field(name="Link", value="https://discord.gg/N6RQe76KDw", inline=False)
  await ctx.send(embed=embed)
  
@client.command()
async def scripts(ctx):
  embed=discord.Embed(title="Installing Scarpet Scripts", color=0xff0000)
  embed.set_author(name=ctx.message.author)
  embed.add_field(name="Setup", value="First, you need to create a scripts folder. This can go inside the world folder or inside your carpet config folder(inside your .minecraft folder). Next, you put the .sc file into your folder and run the script ingame with /script. You may need to reload the world first with /reload or relog.", inline=False)
  embed.add_field(name="Getting Scripts", value="To use a script with Carpet, you need the scarpet apps. These can be found here: https://github.com/gnembon/scarpet. Download the script you want(You may need to copy and paste it) and put it in your scripts folder.", inline=False)
  embed.add_field(name="Use it!", value="You've finished settin up your scripts. You can use them with /script. Remember to load them with /script load.", inline=False)
  await ctx.send(embed=embed)

@client.command()
async def suggest(ctx, *, suggestion):
  await ctx.send("Your suggestion has been sent to the suggestion channel!")
  embed = discord.Embed(title = "New Suggestions",color=random.randint(0, 0xFFFFFF))
  embed.add_field(name = "Author:", value = f"`{ctx.author.name}`")
  embed.add_field(name = "Server:", value = f"`{ctx.guild.name}`")
  embed.add_field(name = "Suggestion: ", value = f"`{suggestion}`")
  guild = client.get_guild(814919704274665523)

  for channel in guild.channels:
      if channel.id == 816304514301689856:
          await channel.send(embed = embed)

@client.command()
async def bot(ctx):
  await ctx.send("https://discord.com/api/oauth2/authorize?client_id=815902015589711934&permissions=272723008&scope=bot")

#Status changing 
client.loop.create_task(ch_pr())
#Keep bot on 24/7
keep_alive()
#Connect to Discord
client.run(os.getenv("TOKEN"))