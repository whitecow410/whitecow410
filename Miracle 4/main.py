# The Bot Made By AwkwardTeam. (WhiteCow, Sear_, YT Mango)
# Made For Miracle.
# Comment By  Sear_
# The Comment is for helping the code investigator/developer understand Codes.
# Credits to Miracle Development Team.

# Import Packages #
from core import Bot

import asyncio


async def main() -> None:
    async with Bot() as bot:
        await bot.start(bot.token)

if __name__ == "__main__":
    # Miracle Startup Line #
    asyncio.run(main())
