import sys
import os
import json
import random
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QStackedWidget, QScrollArea
)
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt, QSize, QTimer
from PIL import Image
import io

class TournamentApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Фото Турнир")
        self.setGeometry(100, 100, 1200, 800)
        
        # Data
        self.photos = []
        self.current_round = []
        self.winners = []
        self.round_number = 1
        self.match_index = 0
        
        # UI
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Screens
        self.menu_screen = self.create_menu_screen()
        self.tournament_screen = self.create_tournament_screen()
        self.results_screen = self.create_results_screen()
        
        self.stacked_widget.addWidget(self.menu_screen)
        self.stacked_widget.addWidget(self.tournament_screen)
        self.stacked_widget.addWidget(self.results_screen)
        
        self.stacked_widget.setCurrentWidget(self.menu_screen)
    
    def create_menu_screen(self):
        """Экран загрузки фото"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        title = QLabel("Фото Турнир")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        description = QLabel("Загрузи фото и запусти турнир на выбывание!")
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description_font = QFont()
        description_font.setPointSize(14)
        description.setFont(description_font)
        
        load_btn = QPushButton("Загрузить фото")
        load_btn.setMinimumHeight(50)
        load_btn.setMinimumWidth(300)
        load_btn.clicked.connect(self.load_photos)
        load_font = QFont()
        load_font.setPointSize(12)
        load_btn.setFont(load_font)
        
        self.photos_count_label = QLabel("Загружено фото: 0")
        self.photos_count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        count_font = QFont()
        count_font.setPointSize(12)
        self.photos_count_label.setFont(count_font)
        
        start_btn = QPushButton("Начать турнир")
        start_btn.setMinimumHeight(50)
        start_btn.setMinimumWidth(300)
        start_btn.clicked.connect(self.start_tournament)
        start_font = QFont()
        start_font.setPointSize(12)
        start_btn.setFont(start_font)
        
        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(description)
        layout.addSpacing(30)
        layout.addWidget(load_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.photos_count_label)
        layout.addSpacing(30)
        layout.addWidget(start_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def create_tournament_screen(self):
        """Экран турнира"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Header
        self.round_label = QLabel()
        round_font = QFont()
        round_font.setPointSize(14)
        round_font.setBold(True)
        self.round_label.setFont(round_font)
        self.round_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Photos container
        self.photos_container = QHBoxLayout()
        self.photo_buttons = []
        
        # Bottom info
        self.match_info = QLabel()
        match_font = QFont()
        match_font.setPointSize(12)
        self.match_info.setFont(match_font)
        self.match_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(self.round_label)
        layout.addSpacing(20)
        layout.addLayout(self.photos_container)
        layout.addSpacing(20)
        layout.addWidget(self.match_info)
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def create_results_screen(self):
        """Экран результатов"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        title = QLabel("Победитель!")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.winner_image = QLabel()
        self.winner_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.winner_name = QLabel()
        winner_font = QFont()
        winner_font.setPointSize(14)
        self.winner_name.setFont(winner_font)
        self.winner_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        restart_btn = QPushButton("Новый турнир")
        restart_btn.setMinimumHeight(50)
        restart_btn.setMinimumWidth(300)
        restart_btn.clicked.connect(self.restart)
        restart_font = QFont()
        restart_font.setPointSize(12)
        restart_btn.setFont(restart_font)
        
        layout.addStretch()
        layout.addWidget(title)
        layout.addSpacing(30)
        layout.addWidget(self.winner_image)
        layout.addSpacing(20)
        layout.addWidget(self.winner_name)
        layout.addSpacing(30)
        layout.addWidget(restart_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def load_photos(self):
        """Загрузка фото из папки"""
        folder = QFileDialog.getExistingDirectory(self, "Выбери папку с фото")
        if folder:
            self.photos = []
            valid_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}
            
            for file in Path(folder).iterdir():
                if file.suffix.lower() in valid_extensions:
                    self.photos.append(str(file))
            
            self.photos.sort()
            self.photos_count_label.setText(f"Загружено фото: {len(self.photos)}")
    
    def start_tournament(self):
        """Начало турнира"""
        if len(self.photos) < 2:
            self.photos_count_label.setText("Нужно минимум 2 фото!")
            return
        
        self.current_round = self.photos.copy()
        random.shuffle(self.current_round)
        self.winners = []
        self.round_number = 1
        self.match_index = 0
        
        self.stacked_widget.setCurrentWidget(self.tournament_screen)
        self.show_match()
    
    def show_match(self):
        """Показать матч"""
        # Clear previous buttons
        for button in self.photo_buttons:
            button.setParent(None)
        self.photo_buttons = []
        
        # Determine number of photos in this match
        remaining = len(self.current_round) - self.match_index
        
        # If odd number and first match of round - show 3 photos
        if self.match_index == 0 and len(self.current_round) % 2 == 1:
            match_photos = 3
        else:
            match_photos = 2
        
        if remaining >= match_photos:
            photos_to_show = self.current_round[self.match_index:self.match_index + match_photos]
        else:
            # Last match with remaining photos
            photos_to_show = self.current_round[self.match_index:]
        
        # Update labels
        self.round_label.setText(f"Раунд {self.round_number}")
        total_matches = (len(self.current_round) + 1) // 2
        current_match = (self.match_index // 2) + 1
        self.match_info.setText(f"Матч {current_match} из {total_matches}")
        
        # Create photo buttons
        for photo_path in photos_to_show:
            btn = QPushButton()
            btn.setMinimumSize(QSize(300, 400))
            btn.setMaximumSize(QSize(400, 500))
            
            # Load and set image
            pixmap = QPixmap(photo_path)
            if not pixmap.isNull():
                pixmap = pixmap.scaledToWidth(300, Qt.TransformationMode.SmoothTransformation)
            btn.setIcon(pixmap)
            btn.setIconSize(pixmap.size())
            btn.setStyleSheet("border: 2px solid #333; background: #f0f0f0;")
            
            # Store photo path
            btn.photo_path = photo_path
            btn.clicked.connect(lambda checked, p=photo_path: self.select_winner(p))
            
            self.photo_buttons.append(btn)
            self.photos_container.addWidget(btn)
        
        self.photos_container.addStretch()
    
    def select_winner(self, photo_path):
        """Выбрать победителя матча"""
        self.winners.append(photo_path)
        
        # Determine how many photos were in this match
        remaining = len(self.current_round) - self.match_index
        if self.match_index == 0 and len(self.current_round) % 2 == 1:
            match_photos = 3
        else:
            match_photos = 2
        
        if remaining >= match_photos:
            match_photos = match_photos
        else:
            match_photos = remaining
        
        self.match_index += match_photos
        
        # Check if round is over
        if self.match_index >= len(self.current_round):
            self.next_round()
        else:
            self.show_match()
    
    def next_round(self):
        """Перейти к следующему раунду"""
        if len(self.winners) == 1:
            # Tournament finished
            self.show_winner()
        else:
            # Start next round
            self.current_round = self.winners
            self.winners = []
            self.round_number += 1
            self.match_index = 0
            random.shuffle(self.current_round)
            self.show_match()
    
    def show_winner(self):
        """Показать победителя"""
        winner_path = self.winners[0]
        pixmap = QPixmap(winner_path)
        
        if not pixmap.isNull():
            pixmap = pixmap.scaledToWidth(400, Qt.TransformationMode.SmoothTransformation)
        
        self.winner_image.setPixmap(pixmap)
        self.winner_name.setText(f"Победитель: {Path(winner_path).name}")
        
        self.stacked_widget.setCurrentWidget(self.results_screen)
    
    def restart(self):
        """Перезагрузить приложение"""
        self.stacked_widget.setCurrentWidget(self.menu_screen)
        self.photos = []
        self.photos_count_label.setText("Загружено фото: 0")


def main():
    app = QApplication(sys.argv)
    window = TournamentApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
