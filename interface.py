from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QGridLayout,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
)
import sys
import numpy as np


class MatrixInterface(QWidget):
    def __init__(self, matrix):
        super().__init__()
        self.setWindowTitle("Matrix Display")
        self.matrix = matrix
        self.init_ui()
        self.last_clicked_button: tuple[int, int] = (-1, -1)
        self.waiting_for_click = False
        self.game_restarted = False

    def init_ui(self):
        main_layout = QHBoxLayout()
        self.setMinimumSize(800, 600)

        # Left side - Matrix Display
        left_layout = QVBoxLayout()
        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)

        self.buttons = []
        for i in range(5):
            row_buttons = []
            for j in range(5):
                button = QPushButton(f"{self.matrix[i, j]:.1f}")
                button.setStyleSheet(
                    """
                    QPushButton {
                        border: 2px solid black;
                        min-width: 80px;
                        min-height: 80px;
                        font-size: 18px;
                        background-color: #f0f0f0;
                    }
                    QPushButton:hover {
                        background-color: #e0e0e0;
                    }
                """
                )
                button.clicked.connect(
                    lambda checked, row=i, col=j: self.on_matrix_button_clicked(
                        row, col
                    )
                )
                grid_layout.addWidget(button, i, j)
                row_buttons.append(button)
            self.buttons.append(row_buttons)
        left_layout.addLayout(grid_layout)
        main_layout.addLayout(left_layout)

        # Right side - Controls
        right_layout = QVBoxLayout()
        right_layout.setSpacing(20)

        # Current player label
        self.player_label = QLabel("Current Player: Player 1")
        self.player_label.setStyleSheet(
            """
            QLabel {
                font-size: 18px;
                font-weight: bold;
                padding: 10px;
                background-color: #f0f0f0;
                border-radius: 5px;
            }
        """
        )
        right_layout.addWidget(self.player_label)

        # Status label
        self.status_label = QLabel("")
        self.status_label.setStyleSheet(
            """
            QLabel {
                font-size: 16px;
                padding: 10px;
                background-color: #f8f8f8;
                border-radius: 5px;
                min-height: 50px;
            }
        """
        )
        self.status_label.setWordWrap(True)
        right_layout.addWidget(self.status_label)

        # Winner label
        self.winner_label = QLabel("")
        self.winner_label.setStyleSheet(
            """
            QLabel {
                font-size: 18px;
                padding: 15px;
                border-radius: 5px;
                min-height: 60px;
            }
        """
        )
        right_layout.addWidget(self.winner_label)

        # Restart button
        restart_btn = QPushButton("Restart Game")
        restart_btn.setStyleSheet(
            """
            QPushButton {
                font-size: 16px;
                padding: 10px;
                min-height: 50px;
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """
        )
        restart_btn.clicked.connect(self.restart_game)
        right_layout.addWidget(restart_btn)

        # Exit button
        exit_btn = QPushButton("Exit")
        exit_btn.setStyleSheet(
            """
            QPushButton {
                font-size: 16px;
                padding: 10px;
                min-height: 50px;
                background-color: #f44336;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """
        )
        exit_btn.clicked.connect(self.close)
        right_layout.addWidget(exit_btn)

        # Add some stretching to keep controls at the top
        right_layout.addStretch()

        main_layout.addLayout(right_layout)
        self.setLayout(main_layout)

    def randomize_matrix(self):
        self.matrix = np.random.rand(5, 5) * 10
        self.update_display(self.matrix)

    def clear_matrix(self):
        self.matrix = np.zeros((5, 5))
        self.update_display(self.matrix)

    def update_display(self, matrix):
        self.matrix = matrix
        for i in range(5):
            for j in range(5):
                if matrix[i, j] == 0:  # O player
                    self.buttons[i][j].setText("")
                    self.buttons[i][j].setStyleSheet(
                        """
                        QPushButton {
                            background-image: url(o.png);
                            background-position: center center;
                            background-repeat: none;
                            background-color: transparent;
                            min-width: 80px;
                            min-height: 80px;
                            max-width: 80px; 
                            max-height: 80px;
                            qproperty-iconSize: 60px;
                        }
                    """
                    )
                elif matrix[i, j] == 1:  # X player
                    self.buttons[i][j].setText("")
                    self.buttons[i][j].setStyleSheet(
                        """
                        QPushButton {
                            border: none;
                            background-image: url(x.png);
                            background-position: center center;
                            background-repeat: none;
                            background-color: transparent;
                            min-width: 80px;
                            min-height: 80px;
                            max-width: 80px;
                            max-height: 80px;
                            qproperty-iconSize: 60px;
                        }
                    """
                    )
                else:  # Unturned cells (-1)
                    self.buttons[i][j].setText("")
                    self.buttons[i][j].setStyleSheet(
                        """
                        QPushButton {
                            background-color: #f0f0f0;
                            border: 2px solid black;
                            min-width: 80px;
                            min-height: 80px;
                            max-width: 80px;
                            max-height: 80px;
                        }
                        QPushButton:hover {
                            background-color: #e0e0e0;
                        }
                    """
                    )

    def on_matrix_button_clicked(self, row, col):
        if self.waiting_for_click:
            self.last_clicked_button = (int(col), int(row))
            self.waiting_for_click = False
            print(f"Button clicked at position: ({col}, {row})")

    def set_current_player(self, player_name):
        self.player_label.setText(f"Current Player: {player_name}")

    def set_winner(self, winner_name):
        self.winner_label.setText(f"Winner: {winner_name}")
        self.winner_label.setStyleSheet(
            """
            QLabel {
                font-size: 18px;
                padding: 15px;
                background-color: #90EE90;
                border-radius: 5px;
                min-height: 60px;
                font-weight: bold;
            }
        """
        )

    def restart_game(self):
        self.matrix = np.ones((5, 5)) * -1
        self.winner_label.setText("")
        self.winner_label.setStyleSheet("padding: 10px;")
        self.status_label.setText("Game restarted! Waiting for move...")
        self.update_display(self.matrix)
        self.game_restarted = True
        self.last_clicked_button = (-1, -1)  # Reset button state
        self.waiting_for_click = False  # Reset click stat
        self.close()

    def set_status(self, message: str):
        self.status_label.setText(message)

    def update(self):
        self.player_label.update()
        self.status_label.update()
        self.winner_label.update()

    def close(self):
        self.window.close()
