from httpx import AsyncClient


class Crawler:
    def __init__(self, client: AsyncClient) -> None:
        ...

    async def run(self) -> None:
        ...
