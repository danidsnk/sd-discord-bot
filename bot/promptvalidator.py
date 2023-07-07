from .chatgpt import ChatGpt


class PromptValidatorError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class PromptValidator:
    def __init__(self):
        system_message = '''You transform sentences according to the pattern,
output must be in english:
input: "A girl with white hair is wearing a red hat and a yellow dress on the beach."
output: "output: a girl with white hair is wearing a red hat and a yellow dress on the beach"
        '''
        self.__chat_gpt = ChatGpt(system_message, one_message=True)
        self.__chat_gpt.add_to_history(
            'Девочка с черными волосами сидит на кресле и держит мороженное')
        self.__chat_gpt.add_to_history(
            'output: a girl with black hair is sitting on a chair holding an ice cream',
            'assistant')
        self.__chat_gpt.add_to_history(
            'A boy with blue eyes is holding a green ball in the park.')
        self.__chat_gpt.add_to_history(
            'output: a boy with blue eyes is holding a green ball in the park',
            'assistant')
        self.__chat_gpt.add_to_history(
            'в лесу красная сова сидит на ветке сосны, идет снег')
        self.__chat_gpt.add_to_history(
            'output: in the woods, a red owl sits on a pine branch, it is snowing',
            'assistant')

    async def validate(self, prompt: str) -> str:
        result = await self.__chat_gpt.chat(prompt)
        if result is None:
            raise PromptValidatorError('Something went wrong...')
        elif result[:6] != 'output':
            raise PromptValidatorError(result)
        else:
            return result[8:]
