import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import View, Button
from utils.fetch_data import search_symbol
import os

class TickerSearchCommand:
    def __init__(self, bot: app_commands.CommandTree, client: discord.Client, guild_id: int):
        self.bot = bot
        self.client = client
        self.guild_id = guild_id

    async def register(self):
        @self.bot.command(name="symbol_search", description="Search for a stock symbol", guild=discord.Object(id=self.guild_id))
        async def symbol_search(ctx: discord.Interaction, keywords: str):
            api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
            if not api_key:
                await ctx.response.send_message("API key not found.")
                return

            data = search_symbol(api_key, keywords)
            if 'bestMatches' in data:
                matches = data['bestMatches']
                if not matches:
                    await ctx.response.send_message("No matches found.")
                    return

                # Create a view with buttons for pagination
                view = SymbolSearchView(matches)
                await ctx.response.send_message(embed=view.create_embed(0), view=view)
            else:
                await ctx.response.send_message("No matches found.")

class SymbolSearchView(View):
    def __init__(self, matches):
        super().__init__(timeout=None)
        self.matches = matches
        self.index = 0

    def create_embed(self, index):
        match = self.matches[index]
        embed = discord.Embed(title="Stock Symbol Search Result", color=discord.Color.blue())
        embed.add_field(name="Symbol", value=match['1. symbol'], inline=False)
        embed.add_field(name="Name", value=match['2. name'], inline=False)
        embed.add_field(name="Type", value=match['3. type'], inline=False)
        embed.add_field(name="Region", value=match['4. region'], inline=False)
        embed.add_field(name="Market Open", value=match['5. marketOpen'], inline=False)
        embed.add_field(name="Market Close", value=match['6. marketClose'], inline=False)
        embed.add_field(name="Timezone", value=match['7. timezone'], inline=False)
        embed.add_field(name="Currency", value=match['8. currency'], inline=False)
        embed.add_field(name="Match Score", value=match['9. matchScore'], inline=False)
        return embed

    @discord.ui.button(label="Previous", style=discord.ButtonStyle.primary)
    async def previous(self, interaction: discord.Interaction, button: Button):
        if self.index > 0:
            self.index -= 1
            await interaction.response.edit_message(embed=self.create_embed(self.index), view=self)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.primary)
    async def next(self, interaction: discord.Interaction, button: Button):
        if self.index < len(self.matches) - 1:
            self.index += 1
            await interaction.response.edit_message(embed=self.create_embed(self.index), view=self)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        # Update button visibility based on the current index
        self.children[0].disabled = self.index == 0  # Disable "Previous" button if at the start
        self.children[1].disabled = self.index == len(self.matches) - 1  # Disable "Next" button if at the end
        return True