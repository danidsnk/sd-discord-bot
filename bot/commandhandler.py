from asyncio import Queue
from datetime import datetime as dt
import random

import discord
from discord.ext import commands

from .generationworker import GenerationInfo, GenerationTask
from .promptvalidator import PromptValidator, PromptValidatorError
from .upscalebuttons import UpscaleButtons
from .logger import get_logger

logger = get_logger('bot')


class DiscordCommandHandler(commands.Bot):
    def __init__(self, queue: Queue, use_paint_plus: bool):
        super().__init__(command_prefix='!', intents=discord.Intents.default())
        self.__queue = queue
        self.__use_paint_plus = use_paint_plus
        if use_paint_plus:
            self.__prompt_validator = PromptValidator()

    @staticmethod
    def __generate_file_name(seed: int):
        timestamp = dt.now().strftime('%Y-%m-%d_%H-%M-%S')
        return f'{timestamp}_{seed}.png'

    async def __on_request(self, interaction: discord.Interaction, prompt: str):
        seed = random.randint(0, 10000000)
        gen_info = GenerationInfo(
            prompt=prompt,
            seed=seed,
            hires=False)

        async def on_start():
            await interaction.edit_original_response(
                content=f'Generating: {prompt}')

        async def on_hires_request(inter: discord.Interaction,
                                   offset: int):
            logger.debug(f'upscalse request from {interaction.user.name} (guild: {interaction.guild_id})')
            await inter.response.send_message('In queue...')

            gen_info = GenerationInfo(
                prompt=prompt,
                seed=seed+offset,
                hires=True)

            async def on_start():
                await inter.edit_original_response(
                    content=f'Upscaling: {prompt}\nseed: {gen_info.seed}')

            async def on_finish(result):
                await inter.edit_original_response(
                    attachments=[discord.File(
                        fp=result,
                        filename=self.__generate_file_name(gen_info.seed))])

            await self.__queue.put(GenerationTask(
                generation_info=gen_info,
                on_start=on_start,
                on_finish=on_finish))
            logger.debug(f'Queued upscalse task: (seed: {gen_info.seed} prompt: "{gen_info.prompt}")')

        async def on_finish(result):
            await interaction.edit_original_response(
                attachments=[discord.File(
                    fp=result,
                    filename=self.__generate_file_name(gen_info.seed))],
                view=UpscaleButtons(interaction, on_hires_request))

        await self.__queue.put(GenerationTask(
            generation_info=gen_info,
            on_start=on_start,
            on_finish=on_finish))
        logger.debug(f'Queued grid task: (seed: {gen_info.seed} prompt: "{gen_info.prompt}")')

    async def start(self, token: str):
        @self.tree.command(name='paint', description='Paint a picture')
        async def paint(interaction: discord.Interaction, prompt: str):
            logger.debug(f'paint request from @{interaction.user.name} (guild: {interaction.guild_id})')
            await interaction.response.send_message('In queue...')
            await self.__on_request(interaction, prompt)

        if self.__use_paint_plus:
            @self.tree.command(name='paint-plus', description='Paint a picture, prompt in any language')
            async def paint_plus(interaction: discord.Interaction, prompt: str):
                logger.debug(f'paint-plus request from @{interaction.user.name} (guild: {interaction.guild_id}) prompt: "{prompt}"')
                await interaction.response.send_message('In queue...')
                try:
                    valid_prompt = await self.__prompt_validator.validate(prompt)
                    logger.debug(f'paint-plus validated prompt: "{valid_prompt}" | original prompt: "{prompt}"')
                    await self.__on_request(interaction, valid_prompt)
                except PromptValidatorError as err:
                    await interaction.edit_original_response(content=str(err))
                    logger.error(f'Validation failed for prompt: "{prompt}" | Error: {err}')

        await super().start(token)
