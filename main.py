import sys, os, json
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QFileDialog, QListWidget, QListWidgetItem, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize

SAVE_FILE = "trainers.json"

class OniMod(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OniMod - Biblioteca de Trainers")
        self.setGeometry(300, 150, 800, 600)
        self.setStyleSheet("background-color: #1e1e1e; color: white;")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.trainerList = QListWidget()
        self.trainerList.setViewMode(QListWidget.IconMode)
        self.trainerList.setIconSize(QSize(200, 120))
        self.trainerList.setResizeMode(QListWidget.Adjust)
        self.trainerList.setSpacing(15)
        self.trainerList.setStyleSheet("border: none;")
        self.trainerList.itemClicked.connect(self.launch_trainer)

        self.layout.addWidget(self.trainerList)

        self.btn_add = QPushButton("+ Agregar trainer")
        self.btn_add.setStyleSheet("padding: 10px; font-size: 16px;")
        self.btn_add.clicked.connect(self.add_trainer)
        self.layout.addWidget(self.btn_add)

        self.trainers = []
        self.load_trainers()

    def add_trainer(self):
        exe_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar Trainer (.exe)", "", "Ejecutables (*.exe)")
        if not exe_path:
            return

        img_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar Imagen (carátula)", "", "Imágenes (*.png *.jpg *.jpeg)")
        if not img_path:
            return

        name = os.path.basename(exe_path).replace(".exe", "")
        item = QListWidgetItem(QIcon(img_path), name)
        item.setData(1000, exe_path)
        item.setData(1001, img_path)
        self.trainerList.addItem(item)

        self.trainers.append({"name": name, "exe": exe_path, "img": img_path})
        self.save_trainers()

    def launch_trainer(self, item):
        exe_path = item.data(1000)
        try:
            os.startfile(exe_path)
        except Exception as e:
            QMessageBox.critical(self, "Error al iniciar trainer", str(e))

    def save_trainers(self):
        with open(SAVE_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.trainers, f, indent=2)

    def load_trainers(self):
        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE, 'r', encoding='utf-8') as f:
                self.trainers = json.load(f)
                for t in self.trainers:
                    item = QListWidgetItem(QIcon(t['img']), t['name'])
                    item.setData(1000, t['exe'])
                    item.setData(1001, t['img'])
                    self.trainerList.addItem(item)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = OniMod()
    window.show()
    sys.exit(app.exec_())
