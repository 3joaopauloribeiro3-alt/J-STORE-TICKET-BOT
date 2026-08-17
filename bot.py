import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from database.database import initialize
from cogs.ticket import Ticket, TicketView

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN não configurado.")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True


class JStoreBot(commands.Bot):

    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=intents,
            help_command=None
        )

    async def setup_hook(self):
        initialize()

        await self.add_cog(
            Ticket(self)
        )

        self.add_view(TicketView())

        await self.tree.sync()


bot = JStoreBot()


@bot.event
async def on_ready():

    print(
        f"✅ J STORE conectado como {bot.user}"
    )

    print(
        f"🌐 Servidores: {len(bot.guilds)}"
    )


@bot.tree.command(
    name="ping",
    description="Verifica se o bot está online."
)
async def ping(
    interaction: discord.Interaction
):

    await interaction.response.send_message(
        f"🏓 Pong! `{round(bot.latency * 1000)}ms`",
        ephemeral=True
    )


bot.run(TOKEN)
