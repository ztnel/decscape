
class NonLand:
    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return "X"


class Land:
    def __init__(self) -> None:
        self.blue = True
        self.black = True
        self.basic = True

    def is_colored(self) -> bool:
        return self.blue or self.black

    def is_multicolored(self) -> bool:
        return self.blue and self.black

    def is_tapped(self, _) -> bool:
        return False


class Island(Land):
    def __init__(self) -> None:
        super().__init__()
        self.basic = True
        self.blue = True
        self.black = False

    def __str__(self) -> str:
        return "[U] Island"

    def is_tapped(self, _: list[Land]) -> bool:
        return False


class Swamp(Land):
    def __init__(self) -> None:
        super().__init__()
        self.basic = True
        self.blue = False
        self.black = True

    def __str__(self) -> str:
        return "[B] Swamp"

    def is_tapped(self, _: list[Land]) -> bool:
        return True


class FabledPassage(Land):
    def __init__(self) -> None:
        super().__init__()
        self.basic = True
        self.blue = True
        self.black = True

    def __str__(self) -> str:
        return "[X] Fabled Passage"

    def is_tapped(self, _: list[Land]) -> bool:
        return True


class WateryGrave(Land):
    def __init__(self) -> None:
        super().__init__()
        self.basic = True
        self.blue = True
        self.black = True

    def __str__(self) -> str:
        return "[UB] Watery Grave"

    def is_tapped(self, _: list[Land]) -> bool:
        return False


class FieldOfRuin(Land):
    def __init__(self) -> None:
        super().__init__()
        self.basic = False
        self.blue = False
        self.black = False

    def __str__(self) -> str:
        return "[X] Field of Ruin"

    def is_tapped(self, _: list[Land]) -> bool:
        return False


class ShipwreckMarsh(Land):
    def __init__(self) -> None:
        super().__init__()
        self.basic = False
        self.blue = True
        self.black = True

    def __str__(self) -> str:
        return "[UB] Shipwreck Marsh"

    def is_tapped(self, _: list[Land]) -> bool:
        return True


class Otawara(Land):
    def __init__(self) -> None:
        super().__init__()
        self.basic = False
        self.blue = True
        self.black = False

    def __str__(self) -> str:
        return "[U] Otawara"

    def is_tapped(self, _: list[Land]) -> bool:
        return False


class HallOfStormGiants(Land):
    def __init__(self) -> None:
        super().__init__()
        self.basic = False
        self.blue = True
        self.black = False

    def __str__(self) -> str:
        return "[U] Hall of Storm Giants"

    def is_tapped(self, _: list[Land]) -> bool:
        return False


class HiveOfTheEyeTyrant(Land):
    def __init__(self) -> None:
        super().__init__()
        self.basic = False
        self.blue = False
        self.black = True

    def __str__(self) -> str:
        return "[B] Hive Of The Eye Tyrant"

    def is_tapped(self, _: list[Land]) -> bool:
        return False


class DrownedCatacomb(Land):
    def __init__(self) -> None:
        super().__init__()
        self.basic = False
        self.blue = True
        self.black = True

    def __str__(self) -> str:
        return "[UB] Drowned Catacomb"

    def is_tapped(self, play: list[Land]) -> bool:
        return sum(1 for x in play if x.is_colored() and x.basic) < 1
