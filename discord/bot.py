import os
import discord
from discord.ext import commands

import responses

supported_bosses = ['hluwill', 'ctene', 'bm']


with open("discord/token.txt", 'r') as f:
    token = f.readlines()[0]


def run_discord_bot():
    TOKEN = token
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    client = commands.Bot(command_prefix='$', intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running')
        synced = await client.tree.sync()
        print(f"{len(synced)} slash commands synced")


    matchmaking_desc = """
                    Request matchmaking service for a given boss.
                """
    boss_choices = [discord.app_commands.Choice(name=x.title(), value=x.lower()) for x in supported_bosses]
    @client.tree.command(name='matchmake', description=matchmaking_desc)
    @discord.app_commands.choices(boss=boss_choices)
    async def matchmake(interaction: discord.Interaction, name: str, boss: discord.app_commands.Choice[str]):
        
        name_str = name.lower()
        boss_str = boss.value.lower()
        response = responses.matchmaking(name_str, boss_str)
        content = f"Attempting matchmaking {name.lower()} for {boss.value} party. \n {response}"
        await interaction.response.send_message(content=content, ephemeral=True)

    update_desc = """
                Request update to BA
            """
    @client.tree.command(name='update', description=update_desc)
    @discord.app_commands.choices(boss=boss_choices)
    async def update(interaction: discord.Interaction, name: str, boss: discord.app_commands.Choice[str]):
        name_str = name.lower()
        boss_str = boss.value.lower()
        response = responses.update(name_str, boss_str)
        await interaction.response.send_message(content=response)

    client.run(TOKEN)
   
if __name__=="__main__":
    run_discord_bot()