from asyncio import Queue
from dataclasses import dataclass
from io import BytesIO
from typing import Callable

from .sdapi import ImageGenerator
from .logger import get_logger

logger = get_logger('bot')


@dataclass
class GenerationInfo:
    prompt: str
    seed: int
    hires: bool


class GenerationTask:
    def __init__(self,
                 generation_info: GenerationInfo,
                 on_start: Callable,
                 on_finish: Callable):
        self.generation_info = generation_info
        self.__on_start = on_start
        self.__on_finish = on_finish

    async def on_start(self):
        await self.__on_start()

    async def on_finish(self, result):
        await self.__on_finish(result)


class GenerationWorker:
    def __init__(self,
                 address: str,
                 port: int,
                 https: bool,
                 queue: Queue):
        self.__generator = ImageGenerator(address, port, https)
        self.__address = address
        self.__queue = queue

    async def __generate(self, gen: GenerationInfo):
        if gen.hires:
            result = await self.__generator.generate_hires(gen.prompt, gen.seed)
        else:
            result = await self.__generator.generate_grid(gen.prompt, gen.seed)

        image_binary = BytesIO()
        result.image.save(image_binary, 'PNG')
        image_binary.seek(0)
        return image_binary

    async def run(self):
        while True:
            task: GenerationTask = await self.__queue.get()
            logger.debug(f'Worker: {self.__address} starting task: (seed: {task.generation_info.seed}, hires: {task.generation_info.hires}, prompt: "{task.generation_info.prompt}")')
            await task.on_start()
            # TODO: error handling
            result = await self.__generate(task.generation_info)
            logger.debug(f'Worker: {self.__address} complete task: (seed: {task.generation_info.seed}, hires: {task.generation_info.hires}, prompt: "{task.generation_info.prompt}")')
            await task.on_finish(result)
            self.__queue.task_done()
