from __future__ import unicode_literals
import youtube_dl
import discord
import os
import secrets

class YoutubeService():

   


    def CreateAudioSteam(self, url: str):
        randomname = f'./songs/{secrets.token_hex(16)}.mp3'
        

        ydl_opts = {
        'format': 'bestaudio/best',
         'outtmpl' : randomname,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
           
        }],}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        

        audiosteam = discord.FFmpegOpusAudio(randomname)
        return audiosteam
        
        