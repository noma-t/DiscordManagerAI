import discord
from discord import app_commands, ui
import config
from bot.gemini_client import GeminiClient
import asyncio


class ConfirmView(ui.View):
    def __init__(self, timeout=180):
        super().__init__(timeout=timeout)
    
    @discord.ui.button(label="OK", style=discord.ButtonStyle.success)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("設定を適用します。")


class DiscordClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tree = app_commands.CommandTree(self)
        self.thread = None
    
    async def on_ready(self):
        print(f"Logged in as {self.user} ({self.user.id})")
    
    async def setup_hook(self) -> None:
        guild_id = 1371566676855886038
        guild = discord.Object(id=guild_id)
        self.tree.copy_global_to(guild=guild)
        
        commands = await self.tree.sync(guild=guild)
        print(commands)
        print("Command tree synced.")
    
    def set_thread(self, thread):
        self.thread = thread

class CommandGroup(app_commands.Group):
    def __init__(self, name: str, description: str, gemini_client: GeminiClient):
        super().__init__(name=name, description=description)
        self.gemini_client = gemini_client
        self.thread = None

    @app_commands.command(name="start", description="AIアシスタントを起動します。")
    async def start(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        self.thread = await interaction.channel.create_thread(
            name="D-MAI",
            type=discord.ChannelType.public_thread,
            auto_archive_duration=60
        )
        await self.thread.send(config.WELCOME_MESSAGE.format(interaction.user.mention))
        await interaction.delete_original_response()
        
        while True:
            try:
                message = await self.thread.wait_for(
                    "message",
                    timeout=180,
                    check=lambda m: m.author == interaction.user
                )
            except asyncio.TimeoutError:
                await self.thread.send(config.TIMEOUT_MESSAGE)
                break
            
            if message.content.lower() == "ok":
                await self.thread.send(config.CONFIRMATION_MESSAGE)
                break
            
            response = self.gemini_client.send_message(message.content)
            await self.thread.send(response.text)

    @app_commands.command(name="stop", description="AIアシスタントを停止します。")
    async def stop(self, interaction: discord.Interaction):
        await interaction.response.send_message("AIアシスタントを停止しました。")
        # TODO: AIアシスタントの停止処理を実装する

    @app_commands.command(name="perms", description="Botの権限を確認します。")
    async def perms(self, interaction: discord.Interaction):
        # TODO: Botの権限を確認する処理を実装する
        await interaction.response.send_message(f"Botの権限: ...")

    @app_commands.command(name="help", description="Botの使い方を表示します。")
    async def help(self, interaction: discord.Interaction):
        # TODO: Botの使い方を表示する処理を実装する
        await interaction.response.send_message("help")
    

def setup_commands(client: DiscordClient, gemini_client: GeminiClient):
    dmai_group = CommandGroup(
        "dmai",
        "Discordサーバーのチャンネルに関する設定を自動化するAIアシスタント",
        gemini_client
    )

    client.tree.add_command(dmai_group)
