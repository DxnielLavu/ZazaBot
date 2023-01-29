import nextcord
from nextcord.ext import commands
from dotenv import load_dotenv
from os import getenv
import wavelink

load_dotenv()

bot = commands.Bot(command_prefix="--", intents = nextcord.Intents.all())

@bot.event
async def on_ready():
    print(f"bot logged in as {bot.user}")
    bot.loop.create_task(node_connect())

@bot.event
async def on_wavelink_node_ready(node: wavelink.Node):
    print(f"Node {node.identifier} is ready!")

async def node_connect():
    await bot.wait_until_ready()
    await wavelink.NodePool.create_node(bot=bot, host='lavalink.mariliun.ml', port=443, password='lavaliun', https=True)


@bot.command()
async def play(ctx: commands.Context, *, search: wavelink.YouTubeTrack):
    if not ctx.voice_client:
        vc = await ctx.author.voice.channel.connect(cls=wavelink.Player)
    elif not ctx.author.voice_client:
        return await ctx.send("Please join a voice channel")
    else:
        vc: wavelink.Player = ctx.voice_client

    await vc.play(search)

bot.run(getenv('DISCORD_TOKEN'))