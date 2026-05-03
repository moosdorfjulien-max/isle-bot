import nextcord
from nextcord.ext import commands
from gamercon_async import EvrimaRCON
from util.config import RCON_HOST, RCON_PORT, RCON_PASS
import logging

class EvrimaRcon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.rcon_host = RCON_HOST
        self.rcon_password = RCON_PASS
        self.rcon_port = RCON_PORT

    @nextcord.slash_command(
        description="Evrima RCON Commands",
        default_member_permissions=nextcord.Permissions(administrator=True)
    )
    async def rcon(self, interaction: nextcord.Interaction):
        await interaction.response.send_message("Nutze Subcommands wie /rcon announce", ephemeral=True)

    async def run_rcon(self, command):
        try:
            print("🔌 Verbinde zu RCON...")
            rcon = EvrimaRCON(self.rcon_host, self.rcon_port, self.rcon_password)
            await rcon.connect()

            print("📡 Sende Command...")
            response = await rcon.send_command(command)

            print("✅ Antwort:", response)
            return response

        except Exception as e:
            print("❌ RCON ERROR:", e)
            return f"ERROR: {e}"

    @rcon.subcommand(description="Make an announcement on the server.")
    async def announce(self, interaction: nextcord.Interaction, message: str):
        await interaction.response.defer(ephemeral=True)

        command = b'\x02' + b'\x10' + message.encode() + b'\x00'
        response = await self.run_rcon(command)

        await interaction.followup.send(f"RCON response:\n{response}", ephemeral=True)

    @rcon.subcommand(description="Save the current state of the server.")
    async def saveserver(self, interaction: nextcord.Interaction):
        await interaction.response.defer(ephemeral=True)

        command = b'\x02' + b'\x50' + b'\x00'
        response = await self.run_rcon(command)

        await interaction.followup.send(f"RCON response:\n{response}", ephemeral=True)

    @rcon.subcommand(description="Kick a player from the server.")
    async def kickplayer(self, interaction: nextcord.Interaction, user_id: str, reason: str):
        await interaction.response.defer(ephemeral=True)

        formatted_command = f"{user_id},{reason}"
        command = b'\x02' + b'\x30' + formatted_command.encode() + b'\x00'
        response = await self.run_rcon(command)

        await interaction.followup.send(f"RCON response:\n{response}", ephemeral=True)

    @rcon.subcommand(description="Ban a player from the server.")
    async def banplayer(self, interaction: nextcord.Interaction, user_id: str, reason: str, ban_length: int):
        await interaction.response.defer(ephemeral=True)

        formatted_command = f"{user_id},{reason},{ban_length}"
        command = b'\x02' + b'\x20' + formatted_command.encode() + b'\x00'
        response = await self.run_rcon(command)

        await interaction.followup.send(f"RCON response:\n{response}", ephemeral=True)

    @rcon.subcommand(description="Display a list of players on the server.")
    async def playerlist(self, interaction: nextcord.Interaction):
        await interaction.response.defer(ephemeral=True)

        command = b'\x02' + b'\x40' + b'\x00'
        response = await self.run_rcon(command)

        await interaction.followup.send(f"RCON response:\n{response}", ephemeral=True)

    @rcon.subcommand(description="Get details about the server.")
    async def serverinfo(self, interaction: nextcord.Interaction):
        await interaction.response.defer(ephemeral=True)

        command = b'\x02' + b'\x12' + b'\x00'
        response = await self.run_rcon(command)

        await interaction.followup.send(f"RCON response:\n{response}", ephemeral=True)

    @rcon.subcommand(description="Direct message a player.")
    async def pm(self, interaction: nextcord.Interaction, user_id: str, message: str):
        await interaction.response.defer(ephemeral=True)

        formatted_command = f"{user_id},{message}"
        command = b'\x02' + b'\x11' + formatted_command.encode() + b'\x00'
        response = await self.run_rcon(command)

        await interaction.followup.send(f"RCON response:\n{response}", ephemeral=True)

    @rcon.subcommand(description="Wipe all corpses from the server.")
    async def wipecorpses(self, interaction: nextcord.Interaction):
        await interaction.response.defer(ephemeral=True)

        command = b'\x02' + b'\x13' + b'\x00'
        response = await self.run_rcon(command)

        await interaction.followup.send(f"RCON response:\n{response}", ephemeral=True)


def setup(bot):
    cog = EvrimaRcon(bot)
    bot.add_cog(cog)