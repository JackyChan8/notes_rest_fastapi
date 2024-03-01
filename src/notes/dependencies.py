from typing import Annotated

from fastapi import Header


async def get_token_jwt(bearer: Annotated[str, Header()]):
    print(bearer)
