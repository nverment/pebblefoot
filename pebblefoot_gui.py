# file: app.py

import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel,
    QLineEdit, QPushButton, QRadioButton,
    QFileDialog, QTextEdit, QDialog,
    QVBoxLayout, QHBoxLayout, QFormLayout,
    QButtonGroup, QMenu
)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt
import pebble_utils
import pebblefoot

def save_to_file(text: str) -> None:
    with open("headers.txt", "w", encoding="utf-8") as f:
        f.write(text)


class HeadersDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Headers")
        self.setFixedSize(800, 400)

        layout = QVBoxLayout()

        self.text_edit = QTextEdit()
        self.save_btn = QPushButton("Save")

        layout.addWidget(QLabel("Insert the header text here"))
        layout.addWidget(self.text_edit)
        layout.addWidget(self.save_btn)

        self.setLayout(layout)

        self.save_btn.clicked.connect(self.save_headers)

    def save_headers(self):
        save_to_file(self.text_edit.toPlainText())
        self.accept()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pebblefoot")
        self.setFixedSize(800, 400)

        self.create_menu()
        self.init_ui()

    # ---------- MENU ----------
    def create_menu(self):
        menu_bar = self.menuBar()

        # spacer trick (push next menu to right)
        menu_bar.setLayoutDirection(Qt.RightToLeft)

        header_option = QAction("Headers", self)
        menu_bar.addAction(header_option)
        header_option.triggered.connect(self.open_headers_dialog)

    # ---------- UI ----------
    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout()

        # --- Spotify URL section ---
        self.folder_name_input = QLineEdit()
        form_layout = QFormLayout()
        self.url_input = QLineEdit()
        form_layout.addRow("Spotify Playlist URL:", self.url_input)
        form_layout.addRow("Output Playlist Name:", self.folder_name_input)

        # --- Mode section ---
        mode_layout = QHBoxLayout()
        self.radio_d = QRadioButton("Download locally")
        self.radio_t = QRadioButton("Transfer to YouTube Music")

        self.mode_group = QButtonGroup(self)
        self.mode_group.addButton(self.radio_d, 1)
        self.mode_group.addButton(self.radio_t, 2)

        mode_layout.addWidget(QLabel("Mode:"))
        mode_layout.addWidget(self.radio_d)
        mode_layout.addWidget(self.radio_t)

        # --- Browse section (hidden initially) ---
        self.browse_layout = QVBoxLayout()
        self.browse_lbl1 = QLabel("Select target Directory for the playlist download:")
        self.browse_directory = QHBoxLayout()
        self.browse_btn = QPushButton("Browse")
        self.folder_lbl2 = QLabel("")
        

        self.browse_btn.clicked.connect(self.open_folder)

        self.browse_directory.addWidget(self.browse_btn)
        self.browse_directory.addWidget(self.folder_lbl2)

        self.browse_layout.addWidget(self.browse_lbl1)
        self.browse_layout.addLayout(self.browse_directory)
        
        self.browse_container = QWidget()
        self.browse_container.setLayout(self.browse_layout)
        self.browse_container.hide()

        # --- Start section ---
        self.start_btn = QPushButton("Start")
        self.start_btn.clicked.connect(self.start_process)

        # --- Assemble ---
        main_layout.addLayout(form_layout)
        main_layout.addLayout(mode_layout)
        main_layout.addWidget(self.browse_container)
        main_layout.addWidget(self.start_btn)
        main_layout.addStretch()

        central.setLayout(main_layout)

        # --- Signals ---
        self.mode_group.buttonClicked.connect(self.update_mode_ui)

    #Utils
    def update_mode_ui(self):
        if self.radio_d.isChecked():
            self.browse_container.show()
        else:
            self.browse_container.hide()

    def open_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.folder_lbl2.setText(os.path.abspath(folder))

    def open_headers_dialog(self):
        dialog = HeadersDialog(self)
        dialog.exec()

    def start_process(self):
        url = self.url_input.text()
        name = self.folder_name_input.text()
        mode = "d" if self.radio_d.isChecked() else "t"
        #folder = self.folder_name_input.text() if mode == "d" else None

        if not url:
            return  # Could add error message here

        pebblefoot.main_gui(url, name, mode)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()