import discord
import requests
from bs4 import BeautifulSoup
import json
import asyncio
import lxml
import asyncio
from discord.ext import commands
import re
from discord.ui import Button, View, Select
import urllib.parse
from time import time, sleep
import collections
from discord.ext import tasks
bot = commands.Bot(command_prefix=".")
client = discord.Client()


# forsencord user list
kill_list = ['ND', 'v1darr', 'azaelwu1', 'betr8byhumanity', 'v1darr', 'thomasrobin91', 'apr292000', 'jerooo159']

# TMDB
api = 'bb1c3b1185ad7a94b4426faf3d96f304'


@bot.slash_command(
    name="list",
    description="Search for a users list",
    guild_ids=[847169717689122816])
async def embed(ctx, user, list):

# starts the discord bot
bot.run('')
