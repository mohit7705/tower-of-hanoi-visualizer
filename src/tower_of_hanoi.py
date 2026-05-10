"""
Recursive Tower of Hanoi game logic.
"""

from typing import List, Tuple


def generate_hanoi_moves(
    n: int,
    source: str,
    auxiliary: str,
    destination: str,
    moves: List[Tuple[str, str]]
) -> None:
    """
    Recursively generate Tower of Hanoi moves.

    Parameters:
    n           -> Number of disks
    source      -> Source tower
    auxiliary   -> Helper tower
    destination -> Destination tower
    moves       -> Stores all moves
    """

    if n == 1:
        moves.append((source, destination))
        return

    generate_hanoi_moves(
        n - 1,
        source,
        destination,
        auxiliary,
        moves
    )


    moves.append((source, destination))

    generate_hanoi_moves(
        n - 1,
        auxiliary,
        source,
        destination,
        moves
    )