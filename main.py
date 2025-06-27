# OniMod - interfaz estilo WeMod
import sys, os, json
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QListWidget, QListWidgetItem, QPushButton, QFileDialog, QHBoxLayout, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import keyboard

CONFIG_FILE = "trainers.json"

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
        except: pass

class OniMod(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OniMod")
        self.setGeometry(300, 100, 600, 400)
        self.trainers = []
        self.load_config()
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.list = QListWidget()
        self.list.itemClicked.connect(self.show_mods)
        self.layout.addWidget(self.list)

        self.btn_add = QPushButton("+ Añadir trainer")
        self.btn_add.clicked.connect(self.add_trainer)
        self.layout.addWidget(self.btn_add)

        self.mods_area = QVBoxLayout()
        self.layout.addLayout(self.mods_area)
        self.populate_trainers()

    def populate_trainers(self):
        self.list.clear()
        for t in self.trainers:
            name = os.path.basename(t.exe)
            item = QListWidgetItem(QIcon(t.img), name)
            self.list.addItem(item)

    def add_trainer(self):
        exe, _ = QFileDialog.getOpenFileName(self, "Seleccionar trainer", "", "Exe Files (*.exe)")
        img, _ = QFileDialog.getOpenFileName(self, "Seleccionar carátula", "", "Imagenes (*.png *.jpg)")
        j, _ = QFileDialog.getOpenFileName(self, "Seleccionar JSON", "", "JSON (*.json)")
        if exe and img and j:
            t = Trainer(exe, img, j)
            self.trainers.append(t)
            self.save_config()
            self.populate_trainers()
        else:
            QMessageBox.warning(self, "Error", "Todos los archivos son necesarios")

    def show_mods(self, item):
        for i in reversed(range(self.mods_area.count())):
            self.mods_area.itemAt(i).widget().deleteLater()
        idx = self.list.currentRow()
        t = self.trainers[idx]
        for mod in t.mods:
            h = QHBoxLayout()
            lbl = QLabel(mod['nombre'])
            btn = QPushButton("ON/OFF")
            btn.clicked.connect(lambda _, key=mod['tecla']: keyboard.send(key))
            h.addWidget(lbl)
            h.addStretch()
            h.addWidget(btn)
            self.mods_area.addLayout(h)

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    raw = json.load(f)
                    for o in raw:
                        self.trainers.append(Trainer(o['exe'], o['img'], o['json']))
            except: pass

    def save_config(self):
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            out = [{'exe':t.exe, 'img':t.img, 'json':t.json_file} for t in self.trainers]
            json.dump(out, f, indent=2)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OniMod()
    window.show()
    sys.exit(app.exec_())
