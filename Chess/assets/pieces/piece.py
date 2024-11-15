from abc import ABC, abstractmethod
from typing import List

class Piece(ABC):
    """An interface that defines the standard methods that pieces in the game should have.
    """
    @abstractmethod
    def listMoves(self) -> List[int, int]:
        """Uses the piece's current position and gives the available moves that piece has.

        Returns:
            List[int, int]: A list of the valid moves available to that piece.
        """
        pass

    @abstractmethod
    def removeSelf(self) -> int:
        """Handles removing this piece from the board.

        Returns:
            int: The value of this piece.
        """
        pass