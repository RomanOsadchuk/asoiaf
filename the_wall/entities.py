from dataclasses import dataclass


@dataclass
class UnfinishedSection:
    height: int  # initial height
    profile: int  # order of profile in the wall
    order: int  # order of section in profile
