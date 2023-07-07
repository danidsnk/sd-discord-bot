from asyncio import Task

from webuiapi import HiResUpscaler, WebUIApi, WebUIApiResult


class ImageGenerator:
    def __init__(self,
                 host: str,
                 port: int,
                 use_https: bool = False,
                 save_images: bool = True):
        self.__api = WebUIApi(host=host,
                                       port=port,
                                       use_https=use_https)
        # self.__sampler = 'UniPC'
        # self.__steps = 10
        # self.__cfg_scale = 5
        # self.__sampler = 'Euler a'
        self.__sampler = 'DPM++ 2M Karras'
        self.__steps = 20
        self.__cfg_scale = 7
        self.__save_images = save_images

    def generate_grid(self, prompt: str, seed: int, batch_size: int = 4
                      ) -> Task[WebUIApiResult]:
        return self.__api.txt2img(prompt=prompt,
                                  use_async=True,
                                  negative_prompt='EasyNegative',
                                  seed=seed,
                                  sampler_name=self.__sampler,
                                  steps=self.__steps,
                                  cfg_scale=self.__cfg_scale,
                                  save_images=self.__save_images,
                                  width=512,
                                  height=768,
                                  batch_size=batch_size)  # type: ignore

    # TODO optimize upscaling
    def generate_hires(self, prompt: str, seed: int
                       ) -> Task[WebUIApiResult]:
        return self.__api.txt2img(prompt=prompt,
                                  use_async=True,
                                  negative_prompt='EasyNegative',
                                  seed=seed,
                                  sampler_name=self.__sampler,
                                  steps=self.__steps,
                                  cfg_scale=self.__cfg_scale,
                                  save_images=self.__save_images,
                                  width=512,
                                  height=768,
                                  batch_size=1,
                                  enable_hr=True,
                                  hr_scale=2,
                                  hr_upscaler=HiResUpscaler.ESRGAN_4x,
                                  hr_second_pass_steps=12,
                                  denoising_strength=0.42)  # type: ignore
