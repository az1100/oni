import sys
import os
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QListWidget, QFileDialog,
    QVBoxLayout, QHBoxLayout, QMessageBox, QListWidgetItem
)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt

CONFIG_FILE = "trainers.json"
ICON_FILE = "onimod_icon_transparent.ico"

class Trainer:
    def __init__(self, exe, img, json_file):
        self.exe = exe
        self.img = img
        self.json_file = json_file
        self.mods = []
        self.load_json()

    def load_json(self):
        try:
            with open(self.json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.mods = data.get("modos", [])
        except:
            pass

class OniMod(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OniMod - Biblioteca de Trainers")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon(ICON_FILE))

        self.trainers = []
        self.load_trainers()

        self.list_widget = QListWidget()
        self.list_widget.itemClicked.connect(self.launch_trainer)

        self.add_button = QPushButton("+ Agregar trainer")
        self.add_button.clicked.connect(self.add_trainer)

        self.remove_button = QPushButton("Eliminar trainer seleccionado")
        self.remove_button.clicked.connect(self.remove_selected)

        layout = QVBoxLayout()
        layout.addWidget(self.list_widget)

        btn_row = QHBoxLayout()
        btn_row.addWidget(self.add_button)
        btn_row.addWidget(self.remove_button)
        layout.addLayout(btn_row)

        self.setLayout(layout)
        self.refresh_list()

    def load_trainers(self):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                self.trainers = json.load(f)
        except:
            self.trainers = []

    def save_trainers(self):
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.trainers, f, indent=2)

    def refresh_list(self):
        self.list_widget.clear()
        for entry in self.trainers:
            item = QListWidgetItem(entry['nombre'])
            if os.path.exists(entry['img']):
                item.setIcon(QIcon(entry['img']))
            self.list_widget.addItem(item)

    def add_trainer(self):
        exe, _ = QFileDialog.getOpenFileName(self, "Seleccionar trainer (.exe)", "", "Trainers (*.exe)")
        if not exe:
            return

        img, _ = QFileDialog.getOpenFileName(self, "Seleccionar imagen del juego", "", "Imagenes (*.png *.jpg *.jpeg)")
        if not img:
            return

        nombre, ok = QFileDialog.getSaveFileName(self, "Guardar JSON del trainer", "", "JSON (*.json)")
        if not nombre:
            return

        nombre_juego = os.path.basename(exe)
        self.trainers.append({
            'nombre': nombre_juego,
            'exe': exe,
            'img': img,
            'json': nombre
        })
        self.save_trainers()
        self.refresh_list()

    def remove_selected(self):
        selected = self.list_widget.currentRow()
        if selected >= 0:
            confirm = QMessageBox.question(self, "Eliminar", "¿Seguro que deseas eliminar este trainer de la lista?", QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                self.trainers.pop(selected)
                self.save_trainers()
                self.refresh_list()

    def launch_trainer(self, item):
        index = self.list_widget.row(item)
        os.startfile(self.trainers[index]['exe'])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = OniMod()
    window.show()
    sys.exit(app.exec_())
