import discord
import requests
import asyncio
import time
import os
import json
import colorama
import datetime
import json
from typing import List
from discord import Guild, Member, MessageInteraction, VoiceChannel, app_commands
from discord import Asset, Guild, MessageInteraction, app_commands
from discord.ui import Select, View
from discord.ui import Button
from discord.ext import commands

bot = commands.Bot(command_prefix='.', intents=discord.Intents.all())

with open('config.json', 'r') as c:
    config = json.load(c)
    TOKEN = config["TOKEN"]

@bot.event
async def on_ready():
    print('Bot Online.')
    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} commands")

@bot.tree.command(name="format", description="Create an exploiter report easily")
async def self(interaction: discord.Interaction, username: str, videolink: str, reason: str):
    getid = requests.get(f'https://api.roblox.com/users/get-by-username?username={username}')
    getid = getid.json()
    try:
        getid = getid['Id']
    except:
        await interaction.response.send_message(f':x: {interaction.user.mention} no user was found!', ephemeral=True)
        return
    
    getname = requests.get(f'https://api.roblox.com/users/{getid}')
    getname = getname.json()
    try:
        getname = getname['Username']
    except:
        await interaction.response.send_message(f':x: {interaction.user.mention} no user was found!', ephemeral=True)
        return
    
    class ButtonView(discord.ui.View):
        def __init__(self):
            super().__init__()
            self.value = None

        @discord.ui.button(label="Raw Format", style=discord.ButtonStyle.gray)
        async def raw(self, interaction: discord.Interaction, button: discord.ui.Button):
            message = f'```ID: {getid}\nProfile: https://www.roblox.com/users/{getid}/profile\nUser: {getname}\nReason: {reason}\nDate: {formatted_date_time}\nEvidence: {videolink}```'
            await interaction.response.send_message(message, ephemeral=True)



    view = ButtonView()
    view.add_item(discord.ui.Button(label="Profile", style=discord.ButtonStyle.link, url=f'https://www.roblox.com/users/{getid}/profile'))
    view.add_item(discord.ui.Button(label="Report", style=discord.ButtonStyle.link, url=f'https://discord.com/channels/811695607588585542/1062245388830113792'))
    now = datetime.datetime.now()
    formatted_date_time = now.strftime("%m/%d/%Y %H:%M")

    message = f'{interaction.user.mention} | {interaction.user} | {interaction.user.id}\n\n```ID: {getid}\nProfile: https://www.roblox.com/users/{getid}/profile\nUser: {getname}\nReason: {reason}\nDate: {formatted_date_time}\nEvidence: {videolink}```'
    await interaction.response.send_message(message, ephemeral=True, view=view)


@self.autocomplete('reason')
async def reason_autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> List[app_commands.Choice[str]]:
    reasons = ['Anti-lock', 'Flying', 'Auto-stomp', 'Association', 'Godmode', 'Teleporting', 'Auto-kill', 'Auto-bag', 'Lock', 'Silent Aim', 'Hit-Box Extension', 'Fake Marco', 'Auto-Farming', 'Moving Whilst Charged', 'Other (Not Listed)']
    return [
        app_commands.Choice(name=reason, value=reason)
        for reason in reasons if current.lower() in reason.lower()
    ]

bot.run(TOKEN)
