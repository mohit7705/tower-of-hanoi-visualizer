"""
Graphical User Interface for Tower of Hanoi.
"""

import tkinter as tk
from tkinter import ttk
from tower_of_hanoi import generate_hanoi_moves
from typing import Dict, List, Tuple, Optional

from constants import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    CANVAS_BG,
    TOWER_WIDTH,
    TOWER_HEIGHT,
    BASE_Y,
    TOWER_POSITIONS,
    ROD_COLOR,
    BASE_COLOR,
    TEXT_COLOR,
    DISK_HEIGHT,
    DISK_COLORS
)


class TowerOfHanoiGUI:
    """
    Main GUI class for Tower of Hanoi visualization.
    """

    def __init__(self, num_disks: int) -> None:

        self.root = tk.Tk()

        # Window configuration
        self.root.title("Tower of Hanoi Visualizer")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.resizable(False, False)

        # Create canvas
        self.canvas = tk.Canvas(
            self.root,
            width=WINDOW_WIDTH,
            height=520,
            bg=CANVAS_BG
        )

        self.canvas.pack(fill="both", expand=True)

        # Control frame
        self.control_frame = tk.Frame(
            self.root,
            bg=CANVAS_BG
        )

        self.control_frame.pack(pady=10)

        # Number of disks
        self.num_disks = num_disks

        # Dropdown variable
        self.disk_var = tk.StringVar(
            value=str(self.num_disks)
        )

        # Disk selector label
        self.disk_label = tk.Label(
            self.control_frame,
            text="Disks:",
            bg=CANVAS_BG,
            fg="white",
            font=("Arial", 11, "bold")
        )

        self.disk_label.pack(side="left", padx=5)

        # Disk selector dropdown
        self.disk_selector = ttk.Combobox(
            self.control_frame,
            textvariable=self.disk_var,
            values=["3", "5", "7"],
            width=5,
            state="readonly"
        )

        self.disk_selector.pack(side="left", padx=5)

        # Detect selection changes
        self.disk_selector.bind(
            "<<ComboboxSelected>>",
            self.change_disk_count
        )

        # Start button
        self.start_button = ttk.Button(
            self.control_frame,
            text="Start Animation",
            command=self.start_animation
        )

        self.start_button.pack(side="left", padx=10)

        # Reset button
        self.reset_button = ttk.Button(
            self.control_frame,
            text="Reset",
            command=self.reset_game
        )

        self.reset_button.pack(side="left", padx=10)

        # Store disk objects
        self.disks: List[int] = []

        # Store tower states
        self.towers: Dict[str, List[int]] = {
            "A": [],
            "B": [],
            "C": []
        }

        # Store recursive move list
        self.moves: List[Tuple[str, str]] = []

        # Draw interface
        self.draw_base()
        self.draw_towers()
        self.draw_disks()

    def draw_base(self) -> None:
        """
        Draw bottom platform.
        """

        self.canvas.create_rectangle(
            100,
            BASE_Y,
            900,
            BASE_Y + 20,
            fill=BASE_COLOR,
            outline=""
        )

    def draw_towers(self) -> None:
        """
        Draw tower rods and labels.
        """

        tower_names = ["A", "B", "C"]

        for index, x in enumerate(TOWER_POSITIONS):

            self.canvas.create_rectangle(
                x - TOWER_WIDTH // 2,
                BASE_Y - TOWER_HEIGHT,
                x + TOWER_WIDTH // 2,
                BASE_Y,
                fill=ROD_COLOR,
                outline=""
            )

            self.canvas.create_text(
                x,
                BASE_Y + 40,
                text=tower_names[index],
                fill=TEXT_COLOR,
                font=("Arial", 16, "bold")
            )

    def draw_disks(self) -> None:
        """
        Draw disks correctly stacked on Tower A.
        """

        tower_x = TOWER_POSITIONS[0]

        max_disk_width = 220
        min_disk_width = 80

        width_step = (
            (max_disk_width - min_disk_width)
            / max(self.num_disks - 1, 1)
        )

        # Draw largest -> smallest
        for i in range(self.num_disks):

            disk_size = self.num_disks - i

            disk_width = (
                min_disk_width
                + ((disk_size - 1) * width_step)
            )

            x1 = tower_x - disk_width / 2
            y1 = BASE_Y - ((i + 1) * DISK_HEIGHT)

            x2 = tower_x + disk_width / 2
            y2 = y1 + DISK_HEIGHT

            color = DISK_COLORS[i % len(DISK_COLORS)]

            disk: int = self.canvas.create_rectangle(
                x1,
                y1,
                x2,
                y2,
                fill=color,
                outline=""
            )

            self.disks.append(disk)

        # Proper stack order
        self.towers["A"] = self.disks[::-1]

    def start_animation(self) -> None:
        """
        Generate recursive moves and start animation.
        """

        self.start_button.config(state="disabled")

        self.moves.clear()

        generate_hanoi_moves(
            self.num_disks,
            "A",
            "B",
            "C",
            self.moves
        )

        self.animate_moves()

    def animate_moves(self) -> None:
        """
        Animate recursive moves.
        """

        if not self.moves:
            return

        source, destination = self.moves.pop(0)

        self.move_disk(source, destination)

        self.root.after(
            500,
            self.animate_moves
        )

    def move_disk(
        self,
        source: str,
        destination: str
    ) -> None:
        """
        Move disk visually between towers.
        """

        if not self.towers[source]:
            return

        # Remove top disk
        disk: int = self.towers[source].pop()

        # Add to destination
        self.towers[destination].append(disk)

        destination_index = {
            "A": 0,
            "B": 1,
            "C": 2
        }[destination]

        tower_x = TOWER_POSITIONS[destination_index]

        stack_height = len(self.towers[destination])

        x1, _, x2, _ = self.canvas.coords(disk)

        disk_width = x2 - x1

        new_x1 = tower_x - disk_width / 2
        new_y1 = BASE_Y - (stack_height * DISK_HEIGHT)

        new_x2 = tower_x + disk_width / 2
        new_y2 = new_y1 + DISK_HEIGHT

        self.canvas.coords(
            disk,
            new_x1,
            new_y1,
            new_x2,
            new_y2
        )

    def change_disk_count(
        self,
        event: Optional[tk.Event] = None
    ) -> None:
        """
        Change number of disks dynamically.
        """

        self.num_disks = int(self.disk_var.get())

        self.reset_game()

    def reset_game(self) -> None:
        """
        Reset complete game state.
        """

        # Clear disk storage
        self.disks.clear()

        # Clear canvas
        self.canvas.delete("all")

        # Reset towers
        self.towers = {
            "A": [],
            "B": [],
            "C": []
        }

        # Clear moves
        self.moves.clear()

        # Enable button again
        self.start_button.config(state="normal")

        # Redraw interface
        self.draw_base()
        self.draw_towers()
        self.draw_disks()

    def run(self) -> None:
        """
        Start GUI loop.
        """

        self.root.mainloop()