from asyncio import Queue, gather
import os
from typing import List

from .commandhandler import DiscordCommandHandler
from .generationworker import GenerationWorker


class DiscordBot:
    def __init__(self,
                 workers: List[dict],
                 server_white_list: List[int],
                 use_paint_plus: bool = False):
        self.__guild_white_list = server_white_list
        self.__queue = Queue()
        self.__workers: List[GenerationWorker] = [
            self.__worker_constructor(**worker)
            for worker in workers]
        self.__command_handler = DiscordCommandHandler(self.__queue,
                                                       use_paint_plus)

    def __worker_constructor(self,
                             address: str,
                             port: int,
                             https: bool = False):
        return GenerationWorker(address, port, https, self.__queue)

    async def __guild_filter(self, guild):
        if guild.id not in self.__guild_white_list:
            await guild.leave()

    async def start(self):
        token = os.getenv('DISCORD_TOKEN')
        if token is None:
            raise ValueError('DISCORD_TOKEN environment variable not set')

        ch = self.__command_handler

        @ch.event
        async def on_ready():
            for guild in ch.guilds:
                await self.__guild_filter(guild)
            print(f'{ch.user} is now running!')
            await ch.tree.sync()

        @ch.event
        async def on_guild_join(guild):
            await self.__guild_filter(guild)

        workers_run = [worker.run() for worker in self.__workers]
        await gather(self.__command_handler.start(token), *workers_run)
