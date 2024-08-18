from enum import auto, IntEnum


class CardColor(IntEnum):
    """
    Enum class for the color of the card
    """
    RED = 0
    BLUE = auto()
    GREEN = auto()
    YELLOW = auto()
    CRAZY = auto()


class CardLabel(IntEnum):
    """
    Enum class for the value of the card
    """
    ZERO = 0
    ONE = auto()
    TWO = auto()
    THREE = auto()
    FOUR = auto()
    FIVE = auto()
    SIX = auto()
    SEVEN = auto()
    EIGHT = auto()
    NINE = auto()
    SKIP = auto()
    REVERSE = auto()
    DRAW_TWO = auto()
    CRAZY = auto()
    DRAW_FOUR = auto()


class Card:
    def __init__(self, color: CardColor, label: CardLabel) -> None:
        """
        Constructor for the Card class

        Args:
            color (CardColor): The color of the card
            label (CardLabel): The label of the card

        Returns:
            None

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        self.color = color
        self.label = label

    def __lt__(self,other):
        """
        Magic method to redefine less than to compare card color and label elements

        Args:
            self: self card object
            other: other card object
        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        if self.color == other.color: 
            return self.label < other.label
        else:
            return self.color < other.color
        
    def __le__(self,other):
        """
        Magic method to redefine less than/equal to to compare card color and label elements

        Args:
            self: self card object
            other: other card object
        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        if self.color == other.color:
            return self.label <= other.label
        else:
            return self.color <= other.color