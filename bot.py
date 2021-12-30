import discord
import os
import random
from random import randint
from discord.abc import GuildChannel
from discord.ext import commands
from dotenv import load_dotenv
import json
import urllib.parse
import urllib.error
import aiohttp


load_dotenv()  # take environment variables from .env.
TOKEN = os.getenv('DISCORD_TOKEN')
TENOR = os.getenv('TENOR_KEY')


bot = commands.Bot(command_prefix='$')

# bot.remove_command("help")


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    print('User ID:', bot.user.id)
    await bot.change_presence(activity=discord.Game('$help'), status=discord.Status.idle)


@bot.event
async def on_member_join(member):
    print(f'{member} has joined a server.')


@bot.event
async def on_member_remove(member):
    print(f'{member} has left a server.')


@bot.command(name='ping', help='Returns pong with latency.')
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')


@bot.command(aliases=['8ball'], help='Ask a yes or no question. Must provide a question to get an answer.')
async def _8ball(ctx, *, question):
    messages = ['It is certain',
                'It is decidedly so',
                'Yes definitely',
                'Reply hazy try again',
                'Ask again later',
                'Concentrate and ask again',
                'My reply is no',
                'Outlook not so good',
                'Very doubtful',
                'Cannot predict now',
                "Don't count on it.",
                'Without a doubt',
                'Better not tell you now.',
                'Outlook good.',
                'As I see it, yes',
                'My sources say no']
    embed = discord.Embed(title=messages[random.randint(
        0, len(messages) - 1)], colour=discord.Colour.random())
    await ctx.send(embed=embed)


@bot.command(help="Displays a map of the UCF campus.")
async def map(ctx):
    embed = discord.Embed(title="UCF Campus Map",
                          url="https://map.ucf.edu/",
                          color=0xebd534)

    embed.set_image(
        url="https://parking.ucf.edu/files/2018/08/shuttlemaps18.png")

    await ctx.send(embed=embed)


@bot.command(aliases=["whois"], help="Get information on a specified user.")
async def userinfo(ctx, member: discord.Member = None):
    if not member:  # if member is no mentioned
        member = ctx.message.author  # set member as the author
    # splice list to exclude @everyone
    roles = [role for role in member.roles[1:]]
    embed = discord.Embed(colour=discord.Colour.purple(), timestamp=ctx.message.created_at,
                          title=f"User Info - {member}")
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"Requested by {ctx.author}")

    embed.add_field(name="ID:", value=member.id)
    embed.add_field(name="Display Name:", value=member.display_name)

    embed.add_field(name="Created Account On:", value=member.created_at.strftime(
        "%a, %#d %B %Y, %I:%M %p UTC"))
    embed.add_field(name="Joined Server On:", value=member.joined_at.strftime(
        "%a, %#d %B %Y, %I:%M %p UTC"))

    embed.add_field(name="Roles:", value="".join(
        [role.mention for role in roles]))
    embed.add_field(name="Highest Role:", value=member.top_role.mention)
    print(member.top_role.mention)
    await ctx.send(embed=embed)


@bot.command(aliases=["avatar", "pfp"], help="Returns the specified user's avatar.")
async def av(ctx, member: discord.Member = None):
    if not member:
        member = ctx.message.author
    embed = discord.Embed(title=member.display_name)
    embed.set_image(url=member.avatar_url)
    embed.set_footer(text=f"Requested by {ctx.author}")
    await ctx.send(embed=embed)


@bot.command(help="Info on bot and shows commands that have aliases.")
async def info(ctx):
    embed = discord.Embed(title=bot.user.display_name,
                          colour=discord.Colour.greyple(), description="prefix: $, created on: " + str(bot.user.created_at))
    embed.set_thumbnail(url=bot.user.avatar_url)
    embed.add_field(name="Source Code",
                    value="https://github.com/mel4ni3/skippy/")
    embed.add_field(name="Owner", value="oreoz#1432")
    embed.add_field(
        name="8ball", value="Must provide a question to get an answer")
    embed.add_field(name="userinfo/whois",
                    value="Get info on a user, if no user is added, will display sender's info.")
    embed.add_field(name="avatar/av/pfp",
                    value="Get's a user's avatar, if no user is added, will display sender's avatar.")
    embed.add_field(name="help/info", value="List of bot commands.")

    embed.set_footer(text=f"Requested by {ctx.author}")
    await ctx.send(embed=embed)


@bot.command(help='Returns the bruh sound effect.')
async def bruh(ctx):

    await ctx.send("https://www.youtube.com/watch?v=2ZIpFytCSVc")


@bot.command(name='dice', help='Simulates rolling dice. Enter number of dice & number of sides.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    embed = discord.Embed(title='Roll ' + str(number_of_dice) + ' dice with ' +
                          str(number_of_sides) + ' sides', description=', '.join(dice))
    # await ctx.send(', '.join(dice))
    await ctx.send(embed=embed)


@bot.command(name='coinflip', help='Flip a coin for either heads or tails.')
async def coinflip(ctx):
    coin = ['heads.', 'tails.']
    embed = discord.Embed(
        title="It\'s " + coin[random.randint(0, len(coin) - 1)], colour=discord.Colour.red())
    await ctx.send(embed=embed)


@bot.command(help='Returns a gif from tenor using the search term.')
async def gif(ctx, arg):
    key = str(arg)
    lmt = 30

    async with aiohttp.ClientSession() as session:
        embed = discord.Embed(
            title='Result for ' + key,
            colour=discord.Colour.random())
        response = await session.get('https://api.tenor.com/v1/search?q=%s&key=%s&limit=%s' % (key, TENOR, lmt))
        data = json.loads(await response.text())
        gif_choice = random.randint(0, 30)
        embed.set_image(url=data['results'][gif_choice]
                        ['media'][0]['gif']['url'])
    await session.close()
    await ctx.send(embed=embed)


@bot.command(name='server', help='Get info on the server you are in.')
async def server(ctx):
    name = str(ctx.guild.name)
    embed = discord.Embed(title=str(ctx.guild.name) +
                          " Server Information", color=discord.Colour.dark_green())
    embed.set_thumbnail(url=str(ctx.guild.icon_url))
    embed.add_field(name="Owner ID", value=str(ctx.guild.owner_id))
    embed.add_field(name="Server ID", value=str(ctx.guild.id))
    embed.add_field(name="Created on", value=str(ctx.guild.created_at))
    embed.add_field(name="Member Count", value=str(ctx.guild.member_count))

    await ctx.send(embed=embed)


bot.run(TOKEN)
