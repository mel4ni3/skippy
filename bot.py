import discord
import random
from discord.ext import commands

client = commands.Bot(command_prefix = '$')
client.remove_command("help")

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    print(client.user.id)
    await client.change_presence(activity = discord.Game('$help'), status = discord.Status.idle)

@client.event
async def on_member_join(member):
    print(f'{member} has joined a server.')

@client.event
async def on_member_remove(member):
    print(f'{member} has left a server.')

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@client.command(aliases=['8ball'])
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
    embed = discord.Embed(title = messages[random.randint(0, len(messages) - 1)], colour = discord.Colour.random())
    await ctx.send(embed = embed)

@client.command()
async def embed(ctx):
    embed=discord.Embed(title="Sample Embed", 
        url="https://realdrewdata.medium.com/", 
        description="This is an embed that will show how to build an embed and the different components", 
        color=0xFF5733)

    embed.set_author(name=ctx.author.display_name,
        icon_url=ctx.author.avatar_url)

    embed.set_thumbnail(url="https://i.imgur.com/axLm3p6.jpeg")

    embed.add_field(name="Field 2 Title", value="It is inline with Field 3", inline=True)
    embed.add_field(name="Field 3 Title", value="It is inline with Field 2", inline=True)

    embed.set_footer(text="Information requested by: {}".format(ctx.author.display_name))


    await ctx.send(embed=embed)

@client.command()
async def map(ctx):
    embed=discord.Embed(title="UCF Campus Map", 
        url="https://map.ucf.edu/",
        color=0xebd534)

    embed.set_image(url="https://parking.ucf.edu/files/2018/08/shuttlemaps18.png")
    
    await ctx.send(embed=embed)

@client.command(aliases=["whois"])
async def userinfo(ctx, member: discord.Member = None):
    if not member:  # if member is no mentioned
        member = ctx.message.author  # set member as the author
    roles = [role for role in member.roles[1:]] # splice list to exclude @everyone
    embed = discord.Embed(colour=discord.Colour.purple(), timestamp=ctx.message.created_at,
                        title=f"User Info - {member}")
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"Requested by {ctx.author}")

    embed.add_field(name="ID:", value=member.id)
    embed.add_field(name="Display Name:", value=member.display_name)

    embed.add_field(name="Created Account On:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
    embed.add_field(name="Joined Server On:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))

    embed.add_field(name="Roles:", value="".join([role.mention for role in roles]))
    embed.add_field(name="Highest Role:", value=member.top_role.mention)
    print(member.top_role.mention)
    await ctx.send(embed=embed)

@client.command(aliases=["avatar", "pfp"])
async def av(ctx, member: discord.Member = None):
    if not member:
        member = ctx.message.author
    embed=discord.Embed(title=member.display_name)
    embed.set_image(url=member.avatar_url)
    embed.set_footer(text=f"Requested by {ctx.author}")
    await ctx.send(embed=embed)


@client.command(aliases=["help"])
async def info(ctx):
    embed=discord.Embed(title=client.user.display_name, colour=discord.Colour.greyple(), description="prefix: $")
    embed.set_thumbnail(url=client.user.avatar_url)
    embed.add_field(name="ping", value="Returns pong with latency")
    embed.add_field(name="map", value="Returns a map of UCF")
    embed.add_field(name="8ball", value="Must provide a question to get an answer")
    embed.add_field(name="userinfo/whois", value="Get info on a user, if no user is added, will display sender's info.")
    embed.add_field(name="avatar/av/pfp", value="Get's a user's avatar, if no user is added, will display sender's avatar.")
    embed.add_field(name="info/help", value="List of bot commands.")

    embed.set_footer(text=f"Requested by {ctx.author}")
    await ctx.send(embed=embed)

@client.command()
async def bruh(ctx):

    await ctx.send("https://www.youtube.com/watch?v=2ZIpFytCSVc")




client.run('ODY1MzA5NTcxOTM3ODYxNjcz.YPCIVg.sqoJTl9ysP3GLXNHBhxU_gy7k9U')