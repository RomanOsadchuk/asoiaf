from dataclasses import dataclass


@dataclass
class UnfinishedSection:
    height: int  # initial height
    profile: int  # order of profile in the wall (started with 1)
    order: int  # order of section in profile (started with 1)
