import aiohttp

class JokeService:

    JOKE_URL = "https://official-joke-api.appspot.com/random_joke"

    # WHY IS PYTHON ASS
    async def get_joke(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.JOKE_URL) as response:

                if response.status != 200:
                    return None

                data = await response.json()

                # Something something, clean code.. I dunno
                return f"{data['setup']}\n{data['punchline']}"