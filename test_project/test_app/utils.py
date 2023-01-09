from enum import Enum, unique


@unique
class ErrorMessages(Enum):
    MODEL_ERROR = "Error raised from model."
    SERIALIZER_ERROR = "Error raised from serializer."
    VIEW_ERROR = "Error raised from view."

    def __str__(self) -> str:
        return self.value
