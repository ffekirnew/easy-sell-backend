import dataclasses


@dataclasses.dataclass
class CreateUserDto:
    telegramId: str
    telegramUsername: str
    phoneNumber: int

    @classmethod
    def from_dict(cls, d):
        return cls(**d)

    def to_dict(self):
        return dataclasses.asdict(self)