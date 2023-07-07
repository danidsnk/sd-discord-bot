from typing import Callable

import discord


class UpscaleButtons(discord.ui.View):
    def __init__(self, message: discord.Interaction, action: Callable):
        super().__init__(timeout=50)
        self.__message = message
        self.__action = action

    async def on_timeout(self) -> None:
        await self.__disable_all_items()

    async def __disable_all_items(self):
        for item in self.children:
            item.disabled = True  # type: ignore
        await self.__message.edit_original_response(view=self)

    async def __disable_item(self, button):
        button.disabled = True
        await self.__message.edit_original_response(view=self)

    async def __button_click(self,
                             interaction: discord.Interaction,
                             label: str,
                             button: discord.ui.Button):
        index = {'U1': 0, 'U2': 1, 'U3': 2, 'U4': 3}[label]
        await self.__action(interaction, index)
        await self.__disable_item(button)

    @discord.ui.button(label='U1',
                       style=discord.ButtonStyle.primary)
    async def u1(self,
                 interaction: discord.Interaction,
                 button: discord.ui.Button):
        await self.__button_click(interaction, 'U1', button)

    @discord.ui.button(label='U2',
                       style=discord.ButtonStyle.primary)
    async def u2(self,
                 interaction: discord.Interaction,
                 button: discord.ui.Button):
        await self.__button_click(interaction, 'U2', button)

    @discord.ui.button(label='U3',
                       style=discord.ButtonStyle.primary)
    async def u3(self,
                 interaction: discord.Interaction,
                 button: discord.ui.Button):
        await self.__button_click(interaction, 'U3', button)

    @discord.ui.button(label='U4',
                       style=discord.ButtonStyle.primary)
    async def u4(self,
                 interaction: discord.Interaction,
                 button: discord.ui.Button):
        await self.__button_click(interaction, 'U4', button)
