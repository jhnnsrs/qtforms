from  dataclasses import dataclass
from typing import Optional

@dataclass
class FieldError:
    msg: str
    loc: tuple[str, ...]
    type: str
    ctx: Optional[dict[str, str]] = None
