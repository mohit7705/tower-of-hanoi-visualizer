import sys

from ui import TowerOfHanoiGUI


def main() -> None:
    """
    Launch GUI with disk count from terminal.
    """
    num_disks = 3

    if len(sys.argv) > 1:

        try:
            num_disks = int(sys.argv[1])

            if num_disks <= 0:
                raise ValueError

        except ValueError:
            print("\nError: Please provide a positive integer.\n")
            return

    app = TowerOfHanoiGUI(num_disks)
    app.run()


if __name__ == "__main__":
    main()