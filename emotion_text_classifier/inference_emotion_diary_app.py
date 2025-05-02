import sys
import pickle
import pandas as pd
import os
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit,
                             QPushButton, QComboBox, QLineEdit, QMessageBox, QFrame, QScrollArea)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QFont


class EmotionDiaryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        # Existing __init__ code remains unchanged
        self.setWindowTitle("Emotion Diary")
        self.setGeometry(100, 100, 900, 700)
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #e6f0fa, stop:1 #b3cde0);
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4a90e2, stop:1 #357abd);
                color: white;
                border-radius: 12px;
                padding: 10px;
                min-width: 130px;
                font-family: 'Segoe UI', Arial;
                font-size: 15px;
                font-weight: bold;
                border: none;
                transition: all 0.3s ease;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #357abd, stop:1 #2a6395);
                box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.2);
            }
            QFrame {
                background-color: rgba(255, 255, 255, 0.95);
                border-radius: 15px;
                padding: 20px;
                border: none;
                box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.1);
            }
            QLabel {
                color: #2c3e50;
                font-family: 'Segoe UI', Arial;
                font-size: 16px;
                padding: 5px;
            }
            QTextEdit {
                background-color: #ffffff;
                border: 1px solid #d5dce5;
                border-radius: 10px;
                padding: 12px;
                font-size: 15px;
                color: #34495e;
            }
            QTextEdit:focus {
                border: 2px solid #4a90e2;
                box-shadow: 0px 0px 8px rgba(74, 144, 226, 0.3);
            }
            QComboBox {
                background-color: #ffffff;
                border: 1px solid #d5dce5;
                border-radius: 10px;
                padding: 10px;
                min-width: 220px;
                color: #34495e;
                font-family: 'Segoe UI', Arial;
                font-size: 15px;
            }
            QComboBox::drop-down {
                border-left: 1px solid #d5dce5;
                width: 25px;
            }
            QComboBox:hover {
                border: 1px solid #4a90e2;
            }
            QLineEdit {
                background-color: #ffffff;
                border: 1px solid #d5dce5;
                border-radius: 10px;
                padding: 10px;
                color: #34495e;
                font-family: 'Segoe UI', Arial;
                font-size: 15px;
            }
            QLineEdit:focus {
                border: 2px solid #4a90e2;
                box-shadow: 0px 0px 8px rgba(74, 144, 226, 0.3);
            }
            QScrollArea {
                border: none;
                background: transparent;
            }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(25)
        layout.setContentsMargins(30, 30, 30, 30)

        self.title_label = QLabel("📓 Emotion Diary", self)
        self.title_label.setFont(QFont("Segoe UI", 28, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("""
            color: #34495e;
            padding: 15px;
            background: rgba(255, 255, 255, 0.5);
            border-radius: 10px;
            text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.2);
        """)
        layout.addWidget(self.title_label)

        self.status_label = QLabel("Loading model...", self)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setFont(QFont("Segoe UI", 14))
        layout.addWidget(self.status_label)

        input_frame = QFrame(self)
        input_layout = QVBoxLayout(input_frame)
        self.text_input = QTextEdit(self)
        self.text_input.setFixedHeight(160)
        self.text_input.setPlaceholderText("Enter your notes here...")
        input_layout.addWidget(self.text_input)
        layout.addWidget(input_frame)

        result_frame = QFrame(self)
        result_layout = QVBoxLayout(result_frame)
        self.result_label = QLabel("No analysis yet", self)
        self.result_label.setAlignment(Qt.AlignLeft)
        self.result_label.setFont(QFont("Segoe UI", 16))
        result_layout.addWidget(self.result_label)
        layout.addWidget(result_frame)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)

        self.analyze_button = QPushButton("🔍 Analyze Emotion", self)
        self.analyze_button.clicked.connect(self.analyze_sentiment)
        button_layout.addWidget(self.analyze_button)

        self.save_button = QPushButton("💾 Save to Diary", self)
        self.save_button.clicked.connect(self.confirm_and_save)
        button_layout.addWidget(self.save_button)

        self.view_button = QPushButton("👁️ View Diary", self)
        self.view_button.clicked.connect(self.view_diary)
        button_layout.addWidget(self.view_button)
        layout.addLayout(button_layout)

        self.model = None
        self.emotion_mapping = None
        self.load_models()
        self.diary_file = "emotion_diary.csv"
        self.diary_entries = self.load_diary_entries()
        self.update_status()

        self.text_input.setLayoutDirection(Qt.LeftToRight)
        self.result_label.setLayoutDirection(Qt.LeftToRight)

    # Existing methods (load_models, update_status, analyze_sentiment, confirm_and_save, etc.) remain unchanged
    def load_models(self):
        try:
            with open("emotion_model.pkl", 'rb') as f:
                self.model = pickle.load(f)
            with open("emotion_mapping.pkl", 'rb') as f:
                self.emotion_mapping = pickle.load(f)
            self.reverse_mapping = {v: k for k, v in self.emotion_mapping.items()}
            print("Model loaded successfully")
        except Exception as e:
            print(f"Error loading model: {e}")

    def update_status(self):
        status_text = "Model ready for use" if (self.model and self.emotion_mapping) else "Model not loaded"
        self.status_label.setText(status_text)
        status_color = "#27ae60" if (self.model and self.emotion_mapping) else "#e74c3c"
        self.status_label.setStyleSheet(
            f"color: {status_color}; font-weight: bold; background: rgba(255, 255, 255, 0.7); padding: 5px 10px; border-radius: 8px;")

    def analyze_sentiment(self):
        if not (self.model and self.emotion_mapping):
            QMessageBox.critical(self, "Error", "Model not loaded. Please ensure model files are available.")
            return

        text = self.text_input.toPlainText().strip()
        if not text:
            QMessageBox.critical(self, "Error", "Please enter text for analysis")
            return

        try:
            prediction = self.model.predict([text])[0]
            emotion = self.reverse_mapping[prediction]
            self.result_label.setText(f"Detected Emotion: {emotion}")
            self.current_emotion = emotion
            self.current_text = text
            print(f"Analyzed: Emotion = {emotion}, Text = {text}")
        except Exception as e:
            QMessageBox.critical(self, "Analysis Error", str(e))

    def confirm_and_save(self):
        print("Save button clicked")
        if not hasattr(self, 'current_emotion') or not hasattr(self, 'current_text'):
            QMessageBox.critical(self, "Error", "Please analyze the text first before saving")
            return

        self.confirm_window = QMainWindow(self)
        self.confirm_window.setWindowTitle("Save Emotion")
        self.confirm_window.setGeometry(200, 200, 450, 300)
        self.confirm_window.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #f5f7fa, stop:1 #d9e4f0);
            }
            QLabel {
                color: #34495e;
                font-family: 'Segoe UI', Arial;
                font-size: 16px;
                padding: 5px;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4a90e2, stop:1 #357abd);
                color: white;
                border-radius: 12px;
                padding: 10px;
                min-width: 130px;
                font-family: 'Segoe UI', Arial;
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #357abd, stop:1 #2a6395);
                box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.2);
            }
            QComboBox {
                background-color: #ffffff;
                border: 1px solid #d5dce5;
                border-radius: 10px;
                padding: 10px;
                min-width: 220px;
                color: #34495e;
                font-family: 'Segoe UI', Arial;
                font-size: 15px;
            }
            QComboBox:hover {
                border: 1px solid #4a90e2;
            }
            QLineEdit {
                background-color: #ffffff;
                border: 1px solid #d5dce5;
                border-radius: 10px;
                padding: 10px;
                color: #34495e;
                font-family: 'Segoe UI', Arial;
                font-size: 15px;
            }
            QLineEdit:focus {
                border: 2px solid #4a90e2;
            }
            QFrame {
                background-color: rgba(255, 255, 255, 0.95);
                border-radius: 12px;
                padding: 20px;
                box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.1);
            }
        """)

        central_widget = QWidget()
        self.confirm_window.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        detected_label = QLabel(f"Detected Emotion: {self.current_emotion}", self)
        detected_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        detected_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(detected_label)

        instruction_label = QLabel("Is this correct?", self)
        instruction_label.setFont(QFont("Segoe UI", 14))
        instruction_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(instruction_label)

        self.emotion_list = list(self.emotion_mapping.keys())
        self.selected_emotion = ""
        self.emotion_combo = QComboBox(self)
        self.emotion_combo.addItems(self.emotion_list)
        self.emotion_combo.setCurrentText(self.current_emotion)
        self.emotion_combo.currentTextChanged.connect(self.on_emotion_select)
        layout.addWidget(self.emotion_combo)

        confirm_button = QPushButton("Confirm and Save", self)
        confirm_button.clicked.connect(self.save_to_diary)
        layout.addWidget(confirm_button)
        self.confirm_window.show()

    def on_emotion_select(self, text):
        self.selected_emotion = text

    def save_to_diary(self):
        print("Saving to diary...")
        self.current_emotion = self.emotion_combo.currentText()
        self.confirm_window.close()

        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = {"text": self.current_text, "emotion": self.current_emotion, "date": current_date}
        self.diary_entries.append(entry)
        self.save_diary_entries()
        QMessageBox.information(self, "Saved", "Entry saved to diary successfully")
        print(f"Saved: Text = {self.current_text}, Emotion = {self.current_emotion}, Date = {current_date}")

    def load_diary_entries(self):
        if os.path.exists(self.diary_file):
            try:
                df = pd.read_csv(self.diary_file, encoding='utf-8')
                if 'date' not in df.columns:
                    df['date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                return df.to_dict('records')
            except Exception as e:
                print(f"Error loading diary: {e}")
                return []
        return []

    def save_diary_entries(self):
        try:
            df = pd.DataFrame(self.diary_entries, columns=["text", "emotion", "date"])
            df.to_csv(self.diary_file, index=False, encoding='utf-8')
            print("Diary entries saved to CSV")
        except Exception as e:
            QMessageBox.critical(self, "Save Error", str(e))

    def view_diary(self):
        """Display all diary entries in a scrollable window with edit and delete options"""
        diary_window = QMainWindow(self)
        diary_window.setWindowTitle("My Diary")
        diary_window.setGeometry(150, 150, 800, 600)
        diary_window.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #f5f7fa, stop:1 #c9d6e5);
            }
            QLabel {
                color: #34495e;
                font-family: 'Segoe UI', Arial;
                font-size: 20px;
                font-weight: bold;
                padding: 15px;
            }
            QTextEdit {
                background-color: rgba(255, 255, 255, 0.98);
                color: #2c3e50;
                border: 1px solid #d5dce5;
                border-radius: 15px;
                padding: 20px;
                font-size: 15px;
                line-height: 1.8;
            }
            QScrollArea {
                border: none;
                background: transparent;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4a90e2, stop:1 #357abd);
                color: white;
                border-radius: 12px;
                padding: 10px;
                min-width: 130px;
                font-family: 'Segoe UI', Arial;
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #357abd, stop:1 #2a6395);
                box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.2);
            }
            QPushButton#deleteButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #e74c3c, stop:1 #c0392b);
            }
            QPushButton#deleteButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #c0392b, stop:1 #a93226);
            }
            QPushButton#editButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #f1c40f, stop:1 #d4ac0d);
            }
            QPushButton#editButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #d4ac0d, stop:1 #b7950b);
            }
        """)

        central_widget = QWidget()
        diary_window.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title_label = QLabel("📓 My Diary", diary_window)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50; text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.2);")
        layout.addWidget(title_label)

        scroll_area = QScrollArea()
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setAlignment(Qt.AlignTop)
        scroll_layout.setContentsMargins(10, 10, 10, 10)
        scroll_layout.setSpacing(20)

        if not self.diary_entries:
            no_entries_label = QLabel("No entries in the diary yet.", diary_window)
            no_entries_label.setStyleSheet("color: #7f8c8d; font-size: 16px;")
            scroll_layout.addWidget(no_entries_label)
        else:
            for idx, entry in enumerate(reversed(self.diary_entries)):
                entry_frame = QFrame()
                entry_layout = QVBoxLayout(entry_frame)
                entry_layout.setSpacing(10)

                date_text = entry.get('date', 'Unknown date')
                text = entry['text']
                emotion = entry['emotion']

                entry_label = QLabel(f"📅 {date_text}\n📝 {text}\n Emotion: {emotion}", diary_window)
                entry_label.setStyleSheet("""
                    color: #2c3e50;
                    font-size: 14px;
                    background-color: rgba(255, 255, 255, 0.9);
                    padding: 10px;
                    border: 1px solid #bdc3c7;
                    border-radius: 8px;
                """)
                entry_layout.addWidget(entry_label)

                button_layout = QHBoxLayout()
                edit_button = QPushButton("✏️ Edit", diary_window)
                edit_button.setObjectName("editButton")
                edit_button.clicked.connect(lambda ch, i=len(self.diary_entries) - 1 - idx: self.edit_entry(i, diary_window))
                button_layout.addWidget(edit_button)

                delete_button = QPushButton("🗑️ Delete", diary_window)
                delete_button.setObjectName("deleteButton")
                delete_button.clicked.connect(lambda ch, i=len(self.diary_entries) - 1 - idx: self.delete_entry(i, diary_window))
                button_layout.addWidget(delete_button)

                entry_layout.addLayout(button_layout)
                scroll_layout.addWidget(entry_frame)

        scroll_content.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_content)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)

        export_button = QPushButton("📥 Export as Text File", diary_window)
        export_button.clicked.connect(lambda: self.export_diary_to_text(diary_window))
        button_layout.addWidget(export_button)

        close_button = QPushButton("Close", diary_window)
        close_button.clicked.connect(diary_window.close)
        button_layout.addWidget(close_button)

        layout.addLayout(button_layout)
        diary_window.show()

    def edit_entry(self, index, diary_window):
        """Open a window to edit an existing diary entry"""
        entry = self.diary_entries[index]
        edit_window = QMainWindow(self)
        edit_window.setWindowTitle("Edit Entry")
        edit_window.setGeometry(200, 200, 450, 300)
        edit_window.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #f5f7fa, stop:1 #d9e4f0);
            }
            QLabel {
                color: #34495e;
                font-family: 'Segoe UI', Arial;
                font-size: 16px;
                padding: 5px;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4a90e2, stop:1 #357abd);
                color: white;
                border-radius: 12px;
                padding: 10px;
                min-width: 130px;
                font-family: 'Segoe UI', Arial;
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #357abd, stop:1 #2a6395);
                box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.2);
            }
            QTextEdit {
                background-color: #ffffff;
                border: 1px solid #d5dce5;
                border-radius: 10px;
                padding: 12px;
                font-size: 15px;
                color: #34495e;
            }
            QComboBox {
                background-color: #ffffff;
                border: 1px solid #d5dce5;
                border-radius: 10px;
                padding: 10px;
                min-width: 220px;
                color: #34495e;
                font-family: 'Segoe UI', Arial;
                font-size: 15px;
            }
        """)

        central_widget = QWidget()
        edit_window.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        text_label = QLabel("Edit Text:", edit_window)
        layout.addWidget(text_label)
        text_edit = QTextEdit(edit_window)
        text_edit.setText(entry['text'])
        layout.addWidget(text_edit)

        emotion_label = QLabel("Edit Emotion:", edit_window)
        layout.addWidget(emotion_label)
        emotion_combo = QComboBox(edit_window)
        emotion_combo.addItems(self.emotion_mapping.keys())
        emotion_combo.setCurrentText(entry['emotion'])
        layout.addWidget(emotion_combo)

        save_button = QPushButton("Save Changes", edit_window)
        save_button.clicked.connect(lambda: self.save_edited_entry(index, text_edit.toPlainText(), emotion_combo.currentText(), edit_window, diary_window))
        layout.addWidget(save_button)

        edit_window.show()

    def save_edited_entry(self, index, new_text, new_emotion, edit_window, diary_window):
        """Save the edited entry and refresh the diary view"""
        if not new_text.strip():
            QMessageBox.critical(edit_window, "Error", "Text cannot be empty")
            return

        self.diary_entries[index]['text'] = new_text
        self.diary_entries[index]['emotion'] = new_emotion
        self.diary_entries[index]['date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Update timestamp
        self.save_diary_entries()
        QMessageBox.information(edit_window, "Success", "Entry updated successfully")
        edit_window.close()
        diary_window.close()
        self.view_diary()  # Refresh the diary view

    def delete_entry(self, index, diary_window):
        """Delete an entry from the diary"""
        reply = QMessageBox.question(diary_window, "Confirm Delete", "Are you sure you want to delete this entry?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            del self.diary_entries[index]
            self.save_diary_entries()
            diary_window.close()
            self.view_diary()  # Refresh the diary view

    def export_diary_to_text(self, parent_window):
        try:
            with open("my_diary.txt", 'w', encoding='utf-8') as f:
                f.write("════════════════ Emotion Diary ════════════════\n\n")
                for entry in reversed(self.diary_entries):
                    date_text = entry.get('date', 'Unknown date')
                    f.write(f"📅 Date: {date_text}\n")
                    f.write(f"📝 Text: {entry['text']}\n")
                    f.write(f" Emotion: {entry['emotion']}\n")
                    f.write("═" * 50 + "\n\n")
            QMessageBox.information(parent_window, "Exported", "Diary exported successfully to 'my_diary.txt'")
        except Exception as e:
            QMessageBox.critical(parent_window, "Export Error", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EmotionDiaryApp()
    window.show()
    sys.exit(app.exec_())