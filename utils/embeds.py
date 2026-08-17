import discord

from config import PURPLE


def simple_embed(title, description):
    return discord.Embed(
        title=title,
        description=description,
        color=PURPLE
    )
