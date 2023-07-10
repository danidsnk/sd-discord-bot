from aiohttp import ClientSession
import backoff
import openai
from openai.error import OpenAIError, RateLimitError


class ChatGpt:
    def __init__(self,
                 system_prompt: str = 'You are helpful assistant',
                 one_message: bool = False):
        openai.aiosession.set(ClientSession())
        self.__system_prompt = {'role': 'system', 'content': system_prompt}
        self.__message_history = [self.__system_prompt]
        self.__one_message = one_message

    # TODO: close session

    @backoff.on_exception(backoff.expo, RateLimitError)
    def __gpt_request(self):
        return openai.ChatCompletion.acreate(
            model='gpt-3.5-turbo',
            messages=self.__message_history,
        )

    def __get_response(self, response) -> str:
        return response['choices'][0].message.content

    def __print_api_error(self, error: OpenAIError):
        print(f'OpenAIError: {error}')

    async def chat(self, prompt: str) -> str | None:
        self.__message_history.append({'role': 'user', 'content': prompt})
        try:
            response = await self.__gpt_request()
            res = self.__get_response(response)
            if self.__one_message:
                self.__message_history.pop()
            else:
                self.__message_history.append({'role': 'assistant',
                                               'content': res})
            return res

        except OpenAIError as e:
            self.__print_api_error(e)
            self.__message_history.pop()

    def add_to_history(self, prompt: str, role: str = 'user'):
        message = {'role': role, 'content': prompt}
        self.__message_history.append(message)

    def clear_history(self):
        self.__message_history = [self.__system_prompt]

    def set_system_prompt(self, system_prompt: str):
        self.__system_prompt['content'] = system_prompt
        self.clear_history()

    def last_response(self) -> str:
        if len(self.__message_history) == 1:
            return ''
        return self.__message_history[-1]['content']
