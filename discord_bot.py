from discord import Intents, Interaction, Object, app_commands
from discord.ext import commands

from discord_settings import DiscordSettings
from src.small_size_league_expert.crew import SmallSizeLeagueExpert

settings = DiscordSettings()

intents = Intents.default()
# intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


class Ask(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ask", description="Ask any question")
    @app_commands.describe(
        question="Your question related to RoboCUP Small Size League category"
    )
    async def ask(self, interaction: Interaction, question: str):
        await interaction.response.defer(thinking=True)

        inputs = {"question": question}

        crew_instance = SmallSizeLeagueExpert()

        print("Kicking off SSL promoter crew...")
        # Ensure your crew is configured to handle potential blocking IO asynchronously
        # or run it in an executor if it's significantly blocking.
        result = await crew_instance.crew().kickoff_async(inputs=inputs)
        print(f"Crew execution finished. Result type: {type(result.pydantic)}")

        final_answer = (
            f'{interaction.user.mention}: "{question}"\n\n{result.pydantic.answer}'
        )

        cropped_message = "... (truncated per Discord message size limit)"
        message_size_limit = 2000 - len(cropped_message)

        cropped_answer = final_answer[:message_size_limit]

        if len(final_answer) > message_size_limit:
            cropped_answer = cropped_answer + cropped_message

        await interaction.followup.send(cropped_answer)


# Introduce bot - Some commands to explain what the bot is for
# Help command - Help command to explain what the bot is for
# Contact command - Contact command to explain what the bot is for
# Feedback command - Feedback command to explain what the bot is for
class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.markdown_explanation = open("bot_explanation.md", "r").read()

    @app_commands.command(name="help", description="Help command")
    async def help(self, interaction: Interaction):
        await interaction.response.send_message(self.markdown_explanation)

    @app_commands.command(name="info", description="Info command (alias for help)")
    async def info(self, interaction: Interaction):
        await self.help(interaction)


class Contact(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="contact", description="Contact command")
    async def contact(self, interaction: Interaction):
        await interaction.response.send_message("Contact command")


class Feedback(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="feedback", description="Feedback command")
    async def feedback(self, interaction: Interaction):
        await interaction.response.send_message("Feedback command")


async def setup(bot):
    await bot.add_cog(Ask(bot))
    await bot.add_cog(Help(bot))
    await bot.add_cog(Contact(bot))
    await bot.add_cog(Feedback(bot))


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    if settings.DISCORD_GUILD_ID:
        print(f"Syncing commands to guild {settings.DISCORD_GUILD_ID}")
        guild = Object(id=int(settings.DISCORD_GUILD_ID))
        bot.tree.copy_global_to(guild=guild)
        print("Commands synced to guild")

    print("Syncing commands to global scope")
    await bot.tree.sync()


if __name__ == "__main__":
    import asyncio

    async def main():
        await setup(bot)
        await bot.start(settings.DISCORD_BOT_TOKEN)

    asyncio.run(main())
