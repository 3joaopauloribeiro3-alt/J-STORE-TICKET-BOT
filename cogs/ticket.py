import discord
from discord.ext import commands

from config import (
    TICKET_CATEGORY_ID,
    STAFF_ROLE_ID,
    LOG_CHANNEL_ID,
    PURPLE
)

from database.database import (
    create_ticket,
    get_ticket,
    delete_ticket
)


class CloseTicketView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Fechar Ticket",
        emoji="🔒",
        style=discord.ButtonStyle.danger,
        custom_id="jstore:close_ticket"
    )
    async def close_ticket(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        channel = interaction.channel

        ticket = get_ticket(channel.id)

        if not ticket:
            await interaction.response.send_message(
                "❌ Este canal não é um ticket.",
                ephemeral=True
            )
            return

        await interaction.response.send_message(
            "🔒 Ticket fechado. O canal será excluído.",
            ephemeral=False
        )

        log_channel = interaction.guild.get_channel(
            LOG_CHANNEL_ID
        )

        if log_channel:

            embed = discord.Embed(
                title="🔒 Ticket fechado",
                color=PURPLE
            )

            embed.add_field(
                name="👤 Usuário",
                value=f"<@{ticket['user_id']}>",
                inline=False
            )

            embed.add_field(
                name="🎫 Canal",
                value=channel.name,
                inline=False
            )

            embed.add_field(
                name="🛡️ Fechado por",
                value=interaction.user.mention,
                inline=False
            )

            await log_channel.send(
                embed=embed
            )

        delete_ticket(channel.id)

        await channel.delete(
            reason=f"Ticket fechado por {interaction.user}"
        )


class TicketView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    async def create_ticket(
        self,
        interaction: discord.Interaction,
        ticket_type: str
    ):

        guild = interaction.guild

        existing = get_ticket(
            interaction.user.id,
            by_user=True
        )

        if existing:

            channel = guild.get_channel(
                existing["channel_id"]
            )

            if channel:

                await interaction.response.send_message(
                    f"❌ Você já possui um ticket aberto: "
                    f"{channel.mention}",
                    ephemeral=True
                )

                return

        category = guild.get_channel(
            TICKET_CATEGORY_ID
        )

        if not category:

            await interaction.response.send_message(
                "❌ A categoria de tickets não foi encontrada.",
                ephemeral=True
            )

            return

        staff_role = guild.get_role(
            STAFF_ROLE_ID
        )

        overwrites = {

            guild.default_role:
                discord.PermissionOverwrite(
                    view_channel=False
                ),

            interaction.user:
                discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                    read_message_history=True,
                    attach_files=True,
                    embed_links=True
                )
        }

        if staff_role:

            overwrites[staff_role] = (
                discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                    read_message_history=True,
                    manage_messages=True
                )
            )

        channel = await guild.create_text_channel(

            name=f"ticket-{interaction.user.name}".lower()[:90],

            category=category,

            overwrites=overwrites,

            reason="Criação de ticket J STORE"
        )

        create_ticket(
            interaction.user.id,
            channel.id,
            guild.id,
            ticket_type
        )

        embed = discord.Embed(

            title="🎫 J STORE — Ticket",

            description=(
                f"Olá, {interaction.user.mention}! 👋\n\n"
                "Seu atendimento foi criado com sucesso.\n\n"
                f"**Tipo:** `{ticket_type}`\n\n"
                "Nossa equipe irá atendê-lo em breve."
            ),

            color=PURPLE
        )

        embed.add_field(

            name="📌 Informações",

            value=(
                "• Explique seu problema com detalhes.\n"
                "• Envie comprovantes quando necessário.\n"
                "• Aguarde o atendimento da equipe."
            ),

            inline=False
        )

        await channel.send(

            content=(
                f"{interaction.user.mention} "
                + (
                    staff_role.mention
                    if staff_role
                    else ""
                )
            ),

            embed=embed,

            view=CloseTicketView()
        )

        await interaction.response.send_message(

            f"✅ Ticket criado: {channel.mention}",

            ephemeral=True
        )

    @discord.ui.button(
        label="Comprar",
        emoji="🛒",
        style=discord.ButtonStyle.success,
        custom_id="jstore:buy"
    )
    async def buy(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        await self.create_ticket(
            interaction,
            "Compra"
        )

    @discord.ui.button(
        label="Suporte",
        emoji="❓",
        style=discord.ButtonStyle.primary,
        custom_id="jstore:support"
    )
    async def support(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        await self.create_ticket(
            interaction,
            "Suporte"
        )


class Ticket(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(
        name="painel-ticket",
        description="Envia o painel de tickets da J STORE."
    )
    @discord.app_commands.default_permissions(
        administrator=True
    )
    async def ticket_panel(
        self,
        interaction: discord.Interaction
    ):

        embed = discord.Embed(

            title="🛒 J STORE — ATENDIMENTO",

            description=(
                "━━━━━━━━━━━━━━━━━━━━━━\n\n"
                "✨ **Bem-vindo ao atendimento da J STORE!**\n\n"
                "Precisa de ajuda ou deseja realizar uma compra?\n"
                "Abra um ticket através dos botões abaixo.\n\n"
                "━━━━━━━━━━━━━━━━━━━━━━"
            ),

            color=PURPLE
        )

        embed.add_field(
            name="🛒 Comprar",
            value=(
                "Abra um ticket para realizar uma compra "
                "ou consultar nossos produtos."
            ),
            inline=False
        )

        embed.add_field(
            name="❓ Suporte",
            value=(
                "Precisa de ajuda? Abra um ticket "
                "e fale com nossa equipe."
            ),
            inline=False
        )

        embed.set_footer(
            text="J STORE • Atendimento oficial"
        )

        await interaction.channel.send(
            embed=embed,
            view=TicketView()
        )

        await interaction.response.send_message(
            "✅ Painel enviado!",
            ephemeral=True
        )


async def setup(bot):

    await bot.add_cog(
        Ticket(bot)
    )
