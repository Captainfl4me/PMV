import os
import shutil
import psutil
import win32api
from PyQt6.QtWidgets import QComboBox, QVBoxLayout, QWidget, QListWidget, QPushButton, QAbstractItemView, QListWidgetItem, QCheckBox, QDialog, QLineEdit, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt


class RenameFolderDialog(QDialog):
    def __init__(self, previous_name: str, parent: QWidget | None = None):
        super().__init__(parent)
        
        self.setWindowTitle("Rename Folder")
        self.setModal(True)
        
        self.previous_name_label = QLabel(f"Previous name: {previous_name}")
        self.new_name_edit = QLineEdit()
        self.accept_button = QPushButton("Accept")
        self.accept_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        
        layout = QVBoxLayout()
        layout.addWidget(self.previous_name_label)
        layout.addWidget(QLabel("Enter new folder name:"))
        layout.addWidget(self.new_name_edit)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.accept_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
    def get_new_name(self) -> str:
        return self.new_name_edit.text()


class FolderSelector(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Mission Importer")
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        
        self.combo_box = QComboBox()
        disks = psutil.disk_partitions()
        removable_disks = []
        for disk in disks:
            if "removable" not in disk.opts:
                continue
            name, _, _, _, format = win32api.GetVolumeInformation(disk.device)
            removable_disks.append(f"{disk.device} - {name} ({format})")
        self.combo_box.addItems(removable_disks)
        self.combo_box.currentIndexChanged.connect(self.update_folder_list)

        self.folder_list = QListWidget()
        self.folder_list.itemClicked.connect(self.update_selected_item)
        self.folder_list.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection) # Set selection mode to ExtendedSelection
        self.select_all_button = QPushButton("Select All")
        self.select_all_button.clicked.connect(self.select_all_folders)
        self.unselect_all_button = QPushButton("Unselect All")
        self.unselect_all_button.clicked.connect(self.unselect_all_folders)
        
        self.label_and_import_button = QPushButton("Label and Import selection")
        self.label_and_import_button.clicked.connect(self.label_and_import_selection)

        # Create a layout for the main window
        layout = QVBoxLayout()
        layout.addWidget(self.combo_box)
        layout.addWidget(self.folder_list)
        layout.addWidget(self.select_all_button)
        layout.addWidget(self.unselect_all_button)
        layout.addWidget(self.label_and_import_button)
        self.setLayout(layout)
        
        self.update_folder_list()

    def update_folder_list(self):
        selected_disk = self.combo_box.currentText().split(" - ")[0]
        folders = [f.name for f in os.scandir(selected_disk) if f.is_dir()]

        try:
            folders.remove("System Volume Information")
        except:
            print("System Volume Information not present in this directory")

        self.folder_list.clear()
        for folder in folders:
            item = QListWidgetItem()
            checkbox = QCheckBox(folder)
            self.folder_list.addItem(item)
            self.folder_list.setItemWidget(item, checkbox)

    def update_selected_item(self, item: QListWidgetItem):
        self.folder_list.itemWidget(item).setChecked(not self.folder_list.itemWidget(item).isChecked())
    
    def select_all_folders(self):
        for item_index in range(self.folder_list.count()):
            self.folder_list.itemWidget(self.folder_list.item(item_index)).setChecked(True)
    
    def unselect_all_folders(self):
        for item_index in range(self.folder_list.count()):
            self.folder_list.itemWidget(self.folder_list.item(item_index)).setChecked(False)
        
    def label_and_import_selection(self):
        folder_selected = []
        for item_index in range(self.folder_list.count()):
            if self.folder_list.itemWidget(self.folder_list.item(item_index)).isChecked():
                folder_selected.append(item_index)
        
        new_name = []
        for index in folder_selected:
            renamefolder = RenameFolderDialog(self.folder_list.itemWidget(self.folder_list.item(index)).text())
            renamefolder.exec()
            new_name.append(renamefolder.get_new_name())

        if not os.path.exists("save"):
            os.mkdir("save")

        # Copy selected folders to the current directory inside the save folder with the new name
        for index, folder_idx in enumerate(folder_selected):
            if not os.path.exists("save/" + new_name[index]) and new_name[index] != "":
                shutil.copytree(self.combo_box.currentText().split(" - ")[0] + "/" + self.folder_list.itemWidget(self.folder_list.item(folder_idx)).text(), "save/" + new_name[index])
