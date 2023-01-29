from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Category:
    GroupId: str | int | float
    Eval: str
