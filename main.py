import sys
import os
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QFileDialog, QListWidget, QListWidgetItem, QHBoxLayout,
    QMessageBox, QMenu
)
from PyQt5.QtGui import QPixmap, QIcon, QPainter
from PyQt5.QtCore import Qt, QSize, QPoint

CONFIG_FILE = "trainers.json"
ICON_SIZE = 128

class OniMod(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OniMod - Biblioteca de Trainers")
        self.setWindowIcon(QIcon("onimod_icon_transparent.ico"))
        self.setMinimumSize(700, 500)

        self.trainers = []

        self.layout = QVBoxLayout(self)

        self.logo_label = QLabel()
        self.logo_label.setPixmap(QPixmap("onimod_icon_transparent.ico").scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.logo_label.setFixedSize(36, 36)
        self.layout.addWidget(self.logo_label, alignment=Qt.AlignLeft)

        self.list_widget = QListWidget()
        self.list_widget.setViewMode(QListWidget.IconMode)
        self.list_widget.setIconSize(QSize(ICON_SIZE, ICON_SIZE))
        self.list_widget.setResizeMode(QListWidget.Adjust)
        self.list_widget.setSpacing(20)
        self.list_widget.setMovement(QListWidget.Static)
        self.list_widget.setWrapping(True)
        self.list_widget.setFlow(QListWidget.LeftToRight)
        self.list_widget.setGridSize(QSize(180, 160))
        self.list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_widget.customContextMenuRequested.connect(self.open_context_menu)
        self.list_widget.itemDoubleClicked.connect(self.launch_trainer)

        self.layout.addWidget(self.list_widget)

        self.button_row = QHBoxLayout()
        self.add_button = QPushButton("+ Agregar trainer")
        self.add_button.clicked.connect(self.add_trainer)
        self.button_row.addWidget(self.add_button)

        self.delete_button = QPushButton("Eliminar seleccionado")
        self.delete_button.clicked.connect(self.remove_selected)
        self.button_row.addWidget(self.delete_button)

        self.layout.addLayout(self.button_row)

        self.load_trainers()

    def load_trainers(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                self.trainers = json.load(f).get("trainers", [])
                for t in self.trainers:
                    self.add_trainer_item(t)

    def add_trainer(self):
        exe_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar Trainer", "", "Ejecutables (*.exe)")
        if not exe_path:
            return

        icon_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar Imagen", "", "Imagen (*.png *.jpg *.ico)")
        if not icon_path:
            return

        name = os.path.basename(exe_path)

        trainer = {
            "name": name,
            "exe": exe_path,
            "icon": icon_path
        }
        self.trainers.append(trainer)
        self.add_trainer_item(trainer)
        self.save_trainers()

    def add_trainer_item(self, trainer):
        icon = QIcon(trainer['icon']) if os.path.exists(trainer['icon']) else QIcon()
        item = QListWidgetItem(icon, trainer['name'])
        item.setData(Qt.UserRole, trainer['exe'])
        item.setData(Qt.UserRole + 1, trainer['icon'])
        self.list_widget.addItem(item)

    def save_trainers(self):
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump({"trainers": self.trainers}, f, indent=4)

    def remove_selected(self):
        row = self.list_widget.currentRow()
        if row >= 0:
            confirm = QMessageBox.question(self, "Eliminar Trainer", "¿Estás seguro de que deseas eliminar este trainer de tu lista?", QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                self.trainers.pop(row)
                self.list_widget.takeItem(row)
                self.save_trainers()

    def open_context_menu(self, position: QPoint):
        item = self.list_widget.itemAt(position)
        if item:
            menu = QMenu()
            delete_action = menu.addAction("Eliminar")
            action = menu.exec_(self.list_widget.mapToGlobal(position))
            if action == delete_action:
                row = self.list_widget.row(item)
                confirm = QMessageBox.question(self, "Eliminar Trainer", "¿Estás seguro de que deseas eliminar este trainer de tu lista?", QMessageBox.Yes | QMessageBox.No)
                if confirm == QMessageBox.Yes:
                    self.trainers.pop(row)
                    self.list_widget.takeItem(row)
                    self.save_trainers()

    def launch_trainer(self, item):
        exe_path = item.data(Qt.UserRole)
        if os.path.exists(exe_path):
            os.startfile(exe_path)
        else:
            QMessageBox.critical(self, "Error", f"No se encontró el archivo:\n{exe_path}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("onimod_icon_transparent.ico"))
    window = OniMod()
    window.show()
    sys.exit(app.exec_())

