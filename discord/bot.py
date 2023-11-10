import os
import discord
from discord.ext import commands
import responses

with open("discord/token.txt", 'r') as f:
    token = f.readlines()[0]

async def send_message(message, user_message: str, is_private: bool) -> str: 
    try:
        response = responses.get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)
    

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
    party_bosses = ['hluwill', 'ctene', 'bm', 'nseren', 'hseren']
    @client.tree.command(name='matchmake', description=matchmaking_desc)
    async def matchmake(interaction: discord.Interaction, name: str):
        
        print("calling matchmake function")

        content = "Matchmaking"
        await interaction.response.send_message(content=content, ephemeral=True)

    update_desc = """
                Request update to BA
            """
    @client.tree.command(name='update', description=update_desc)
    async def update(interaction: discord.Interaction):
        print("calling update function")
        content = "Updating"
        await interaction.response.send_message(content=content)

    client.run(TOKEN)
   
if __name__=="__main__":
    run_discord_bot()