from dataclasses import dataclass


@dataclass
class ListProfiles:
    pass


@dataclass
class CreateProfile:
    profile_name: str
    base: str = None


@dataclass
class DeleteProfile:
    profile_name: str


@dataclass
class ProfileSetAlias:
    profile_name: str
    alias_name: str
    alias_val: str = None
