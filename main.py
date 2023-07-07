import argparse
import asyncio
import json

from bot.discordbot import DiscordBot


def load_config(path_to_config: str) -> dict:
    with open(path_to_config, 'r') as f:
        return json.load(f)


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config',
                        default='config.json',
                        help='Path to config file')
    args = parser.parse_args()
    config = load_config(args.config)

    bot = DiscordBot(**config)
    await bot.start()


if __name__ == '__main__':
    asyncio.run(main())
