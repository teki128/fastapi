from pydantic import BaseModel
from typing import Union

class Test(BaseModel):
    num: int; # Field 函数约束
    name: str;