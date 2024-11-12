from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QGridLayout,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
)
from PyQt5.QtGui import QPixmap, QImage
import sys
import numpy as np
from PIL import Image
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog
from variables import *
from zbd import zbd
import qrcode
import time


class MatrixInterface(QWidget):
    def __init__(self, matrix):
        super().__init__()
        self.setWindowTitle("Matrix Display")
        self.matrix = matrix
        self.init_ui()
        self.last_clicked_button: tuple[int, int] = (-1, -1)
        self.waiting_for_click = False
        self.game_restarted = False
        self.ai_search_depth = 2

    def init_ui(self):
        main_layout = QHBoxLayout()
        self.setMinimumSize(600, 500)

        # Left side - Matrix Display
        left_layout = QVBoxLayout()
        grid_layout = QGridLayout()
        grid_layout.setSpacing(5)

        self.buttons = []
        for i in range(5):
            row_buttons = []
            for j in range(5):
                button = QPushButton("")
                button.setFixedSize(80, 80)
                button.setStyleSheet(
                    """
                    QPushButton {
                        border: 2px solid black;
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
        left_layout.addStretch()
        main_layout.addLayout(left_layout)

        # Right side - Controls
        right_layout = QVBoxLayout()
        right_layout.setSpacing(10)

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
                min-height: 40px;
            }
        """
        )
        self.status_label.setWordWrap(True)
        right_layout.addWidget(self.status_label)

        # # Winner label
        # self.winner_label = QLabel("")
        # self.winner_label.setStyleSheet(
        #     """
        #     QLabel {
        #         font-size: 18px;
        #         padding: 10px;
        #         border-radius: 5px;
        #         min-height: 40px;
        #     }
        # """
        # )
        # right_layout.addWidget(self.winner_label)

        # Difficulty selection
        difficulty_label = QLabel("Select Difficulty Level:")
        difficulty_label.setStyleSheet("font-size: 16px; padding: 5px;")
        right_layout.addWidget(difficulty_label)

        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItems(["Easy", "Medium", "Hard"])
        self.difficulty_combo.setStyleSheet(
            """
            QComboBox {
                font-size: 16px;
                padding: 5px;
                min-height: 30px;
            }
            """
        )
        self.difficulty_combo.currentIndexChanged.connect(self.on_difficulty_changed)
        right_layout.addWidget(self.difficulty_combo)

        # Pay Sat to Start button
        pay_sat_btn = QPushButton("Pay Sat to Start")
        pay_sat_btn.setStyleSheet(
            """
            QPushButton {
                font-size: 16px;
                padding: 10px;
                min-height: 40px;
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            """
        )
        pay_sat_btn.clicked.connect(self.pay_sat_to_start)
        right_layout.addWidget(pay_sat_btn)

        # Take Your Prize button
        take_prize_btn = QPushButton("Take Your Prize!")
        take_prize_btn.setStyleSheet(
            """
            QPushButton {
                font-size: 16px;
                padding: 10px;
                min-height: 40px;
                background-color: #FFD700;
                color: black;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #DAA520;
            }
            """
        )
        take_prize_btn.clicked.connect(self.take_your_prize)
        right_layout.addWidget(take_prize_btn)

        # Exit button
        exit_btn = QPushButton("Exit")
        exit_btn.setStyleSheet(
            """
            QPushButton {
                font-size: 16px;
                padding: 10px;
                min-height: 40px;
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

        right_layout.addStretch()

        # Set a fixed width for the right side
        right_widget = QWidget()
        right_widget.setLayout(right_layout)
        right_widget.setFixedWidth(250)

        main_layout.addWidget(right_widget)
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

    def pay_sat_to_start(self):
        # Implement the functionality to handle payment and start the game
        print("Pay Sat to Start button clicked")

        def show_paywall_qr(self):
            # Create a QDialog for the QR overlay
            dialog = QDialog(self)
            dialog.setWindowTitle("Scan QR to Start Game")
            dialog.setModal(True)

            # Create layout
            layout = QVBoxLayout()

            # Load and display QR image using PIL and QPixmap
            try:
                # Open image with PIL
                pil_image = Image.open("paywall_qr.png")

                # Convert PIL image to QPixmap
                qr_label = QLabel()
                pil_image = pil_image.resize((300, 300))  # Resize for better display
                img_data = pil_image.convert("RGBA").tobytes("raw", "RGBA")
                qimage = QPixmap.fromImage(
                    QImage(
                        img_data,
                        pil_image.size[0],
                        pil_image.size[1],
                        QImage.Format_RGBA8888,
                    )
                )
                qr_label.setPixmap(qimage)

                # Add to layout
                layout.addWidget(qr_label)

                # Add instruction label
                instruction = QLabel("Scan this QR code to pay and start the game")
                instruction.setAlignment(Qt.AlignCenter)
                layout.addWidget(instruction)

                dialog.setLayout(layout)
                dialog.exec_()

            except Exception as e:
                print(f"Error loading QR code: {e}")
                self.set_status("Error loading payment QR code")

        show_paywall_qr(self)

    def take_your_prize(self):
        # Implement the functionality to allow the player to take their prize
        print("Take Your Prize! button clicked")
        # Example: handle prize distribution
        # Generate withdrawal request for the winner
        reward_description = PLAYER_REWARD_DESCRIPTION_TEMPLATE.format(winner_id=winner)
        withdrawal_response = zbd_client.create_withdrawal_request(
            amount_of_seconds_to_expire_after=INVOICE_EXPIRY,
            amount_msats=REWARD_AMOUNT,
            description="Got your reward",
            internal_id="11af01d092444a317cb33faa6b8304b8",
        )

        withdrawal_id = withdrawal_response["id"]
        withdrawal_details = zbd_client.get_withdrawal_request_details(withdrawal_id)
        withdrawal_invoice = withdrawal_details["invoice"]["request"]

        print("Congratulations! Here is your reward:")
        qr = qrcode.make(withdrawal_invoice)
        qr.save("reward_qr.png")
        print(f"QR Code saved as reward_qr.png")
        print(f"Lightning Invoice: {withdrawal_invoice}")

    def on_difficulty_changed(self, index):
        difficulty = self.difficulty_combo.currentText()
        print(f"Difficulty level selected: {difficulty}")
        self.set_difficulty_level(difficulty)

    def set_difficulty_level(self, difficulty):
        # Implement how the difficulty level affects your game
        if difficulty == "Easy":
            self.ai_search_depth = 2
        elif difficulty == "Medium":
            self.ai_search_depth = 3
        elif difficulty == "Hard":
            self.ai_search_depth = 4
        print(self.ai_search_depth)
