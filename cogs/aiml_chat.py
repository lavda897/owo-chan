import asyncio
import os
import random

import aiml
import discord
import pkg_resources
from discord.ext import commands

from variables import BOT_PREFIX, STARTUP_FILE


class AIMLchat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.channel_name = "chat-with-owo"

        # Load AIML kernel
        self.aiml_kernel = aiml.Kernel()
        initial_dir = os.getcwd()
        os.chdir(pkg_resources.resource_filename(__name__, '../'))  # Change directories to load AIML files properly
        startup_filename = pkg_resources.resource_filename(__name__, STARTUP_FILE)
        self.aiml_kernel.learn(startup_filename)
        self.aiml_kernel.respond("LOAD AIML B")
        os.chdir(initial_dir)

        self.setup()

    def setup(self):

        @self.bot.event
        async def on_message(message):

            if message.content is None:
                print("Empty message received.")
                print("Message: " + str(message.content))
                return

            if message.content.startswith(BOT_PREFIX):
                # Pass on to rest of the client commands
                await self.bot.process_commands(message)
            elif message.author.bot or str(message.channel) != self.channel_name:
                return
            else:
                aiml_response = self.aiml_kernel.respond(message.content)
                async with message.channel.typing():
                    await asyncio.sleep(random.randint(1,3))
                    await message.channel.send(aiml_response)

def setup(bot):
    bot.add_cog(AIMLchat(bot))
