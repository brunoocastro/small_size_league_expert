import asyncio
import traceback

from discord import Intents, Interaction, Object, app_commands
from discord.ext import commands

from discord_settings import DiscordSettings
from src.small_size_league_expert.crew import SmallSizeLeagueExpert

settings = DiscordSettings()

intents = Intents.default()
# intents.message_content = True
bot = commands.AutoShardedBot(command_prefix="!", intents=intents)


class Ask(commands.Cog):
    crew_instance = None

    def __init__(self, bot):
        self.bot = bot

    async def _run_crew_safely(self, inputs):
        """Run the crew async, ensuring no blocking in Discord's event loop."""
        try:
            self.crew_instance = SmallSizeLeagueExpert()
            result = await self.crew_instance.crew().kickoff_async(inputs=inputs)
            return result
        except Exception as e:
            print(f"Error in crew execution: {e}")
            traceback.print_exc()
            raise e
        finally:
            if self.crew_instance:
                self.crew_instance.cleanup_mcp_tools()

    @app_commands.command(name="ask", description="Ask any question")
    @app_commands.describe(
        question="Your question related to RoboCUP Small Size League category"
    )
    async def ask(self, interaction: Interaction, question: str):
        await interaction.response.defer(thinking=True)

        try:
            inputs = {"original_question": question}

            print("🚀 Kicking off SSL expert crew...")

            # Use the safer crew execution method
            result = await self._run_crew_safely(inputs)

            if not result or not result.pydantic:
                print(
                    "❌ Crew execution returned no result or invalid pydantic output."
                )
                await interaction.followup.send(
                    f"{interaction.user.mention}, I couldn't find an answer to your question. Please try rephrasing it."
                )
                return

            crew_markdown_result = result.pydantic.get_final_answer(
                user_mention=interaction.user.mention, original_question=question
            )

            print(
                f"✅ Crew execution completed successfully. Returning result to Discord with size {len(crew_markdown_result)}."
            )

            print(f"Full result: {result.pydantic.model_dump_json(indent=2)}")

            await interaction.followup.send(crew_markdown_result)

        except Exception as e:
            print(f"❌ Error in ask command: {e}")
            traceback.print_exc()

            error_message = (
                f"{interaction.user.mention}, I encountered an error while processing your question. "
                "This might be due to:\n"
                "• MCP server connection issues\n"
                "• Temporary service unavailability\n"
                "• Network connectivity problems\n\n"
                "Please try again in a moment. If the issue persists, the bot administrator has been notified."
            )

            try:
                await interaction.followup.send(error_message)
            except Exception as followup_error:
                print(f"Failed to send error message: {followup_error}")


# Introduce bot - Some commands to explain what the bot is for
# Help command - Help command to explain what the bot is for
# Contact command - Contact command to explain what the bot is for
# Feedback command - Feedback command to explain what the bot is for
class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        try:
            self.markdown_explanation = open("bot_explanation.md", "r").read()
        except FileNotFoundError:
            self.markdown_explanation = (
                "# SSL Expert Bot\n\n"
                "I'm an AI assistant specialized in RoboCup Small Size League (SSL). "
                "Ask me anything about SSL rules, technical specifications, strategies, or general information!\n\n"
                "Use `/ask` to ask questions about SSL topics."
            )

    @app_commands.command(name="help", description="Help command")
    async def help(self, interaction: Interaction):
        await interaction.response.send_message(self.markdown_explanation)


class Contact(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="contact", description="Contact command")
    async def contact(self, interaction: Interaction):
        contact_info = (
            "📧 **Contact Information**\n\n"
            "For technical support or feedback about this SSL Expert Bot:\n"
            "• Report issues on our GitHub repository\n"
            "• Contact the bot administrator\n"
            "• Join our SSL community discussions\n\n"
            "This bot is powered by AI and connects to SSL knowledge sources."
        )
        await interaction.response.send_message(contact_info)


class Feedback(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="feedback", description="Feedback command")
    async def feedback(self, interaction: Interaction):
        feedback_info = (
            "💬 **Feedback & Suggestions**\n\n"
            "We value your feedback! Help us improve the SSL Expert Bot:\n"
            "• Report inaccurate information\n"
            "• Suggest new features\n"
            "• Share your experience\n\n"
            "Your input helps us provide better SSL knowledge and support!"
        )
        await interaction.response.send_message(feedback_info)


async def setup(bot):
    await bot.add_cog(Ask(bot))
    await bot.add_cog(Help(bot))
    await bot.add_cog(Contact(bot))
    await bot.add_cog(Feedback(bot))


@bot.event
async def on_ready():
    print(f"🤖 Logged in as {bot.user}")
    if settings.DISCORD_GUILD_ID:
        print(f"🔄 Syncing commands to guild {settings.DISCORD_GUILD_ID}")
        guild = Object(id=int(settings.DISCORD_GUILD_ID))
        bot.tree.copy_global_to(guild=guild)
        print("✅ Commands synced to guild")

    print("🌐 Syncing commands to global scope")
    await bot.tree.sync()
    print("✅ Bot is ready and commands are synced!")


@bot.event
async def on_error(event, *args, **kwargs):
    """Global error handler for the bot."""
    print(f"❌ Bot error in event {event}: {args}, {kwargs}")
    traceback.print_exc()


if __name__ == "__main__":
    import asyncio

    async def main():
        try:
            await setup(bot)
            await bot.start(settings.DISCORD_BOT_TOKEN)
        except KeyboardInterrupt:
            print("🛑 Bot shutdown requested")
        except Exception as e:
            print(f"❌ Fatal error: {e}")
            traceback.print_exc()
        finally:
            print("🔄 Cleaning up...")
            await bot.close()

    asyncio.run(main())
