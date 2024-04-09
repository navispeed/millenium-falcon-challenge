from typing import TypedDict

from calculator.models.bounty_hunter import BountyHunter
from pydantic import BaseModel

class Empire(TypedDict):
    countdown: int
    bounty_hunters: list[BountyHunter]
