import discord
import time
from discord.ext import commands
import os
from discord.utils import get
import youtube_dl
from youtube import YoutubeService
from time import sleep
from creds import TOKEN

class DiscordBot():


    def __init__(self, token: str):
        youtubeservice = YoutubeService()
        client = commands.Bot(command_prefix = '/')


        @client.event
        async def on_ready():
            print("cleaning out old audio files")
            for i in os.listdir("./songs/"):
                if i.endswith(".mp3"):
                    os.remove(f"./songs/{i}")
                print("files removed")
            print("ready")


        @client.command(pass_context=True)
        async def join(ctx):
            global voice
            channel = ctx.message.author.voice.channel
            voice = get(client.voice_clients, guild=ctx.guild)
            
            if voice and voice.is_connected():
                await voice.move_to(channel)
            else:
                voice = await channel.connect()
            print(f"the bot has joined {channel}")
            await ctx.send(f"joined {channel}")


        @client.command(pass_context=True)
        async def play(ctx):
            global voice
            global audio_source
            
            if voice.is_playing():
                self.StopAudio(audio_source, voice)

            if voice.is_paused():
                voice.play(audio_source, voice)
                await ctx.send(f"Resuming...")
            else:
                audio_source = youtubeservice.CreateAudioSteam(ctx.message.content[6:])
                voice.play(audio_source)
                await ctx.send(f"Now playing: {ctx.message.content[6:]} for {ctx.ctx.message.author.mention}")
   

        @client.command(pass_context=True)
        async def leave(ctx):
            channel = ctx.message.author.voice.channel
            voice = get(client.voice_clients, guild=ctx.guild)

            if voice and voice.is_connected():
                await voice.disconnect()
                print(f"the bot has left {channel}")
                await ctx.send(f"Left {channel}")
            return

      

        @client.command(pass_context=True)
        async def pause(ctx):
            channel = ctx.message.author.voice.channel
            global voice
            voice.pause()
            await ctx.send(f"Paused Audio: {channel}")

        @client.command(pass_context=True)
        async def stop(ctx):
            global voice
            global audio_source
            self.StopAudio(audio_source, voice)







        client.run(token)

    def StopAudio(self, audiostream, voice):
        # keep the file name for clean up
        file = audiostream._process.args[2]
        voice.stop()
        audiostream.cleanup()
        sleep(0.01)
        os.remove(file)





    
DiscordBot(TOKEN)