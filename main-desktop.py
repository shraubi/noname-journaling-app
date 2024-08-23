import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QColor, QPalette

class DangerousWritingApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Main text editor
        self.text_edit = QTextEdit(self)
        self.text_edit.textChanged.connect(self.reset_timer_and_update_word_count)

        # Word count label
        self.word_count_label = QLabel("Words: 0", self)

        # Notification label
        self.notification_label = QLabel("", self)
        self.notification_label.setStyleSheet("color: red;")
        self.notification_label.setAlignment(Qt.AlignCenter)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addWidget(self.word_count_label)
        layout.addWidget(self.notification_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Idle timers
        self.idle_threshold = 5000  # 5 seconds before text deletion
        self.dim_threshold = 2000   # 2 seconds before the screen dims red
        self.idle_timer = QTimer()
        self.dim_timer = QTimer()
        self.idle_timer.timeout.connect(self.clear_text)
        self.dim_timer.timeout.connect(self.apply_red_dim)

        self.reset_timer_and_update_word_count()

        self.setWindowTitle("Dangerous Writing App")
        self.resize(600, 400)
        self.show()

    def reset_timer_and_update_word_count(self):
        self.idle_timer.start(self.idle_threshold)
        self.dim_timer.start(self.dim_threshold)
        self.clear_red_dim()
        self.update_word_count()
        self.notification_label.clear()

    def clear_text(self):
        self.text_edit.clear()
        self.notification_label.setText("Text deleted due to idling!")
        self.idle_timer.stop()
        self.dim_timer.stop()
        self.clear_red_dim()

    def apply_red_dim(self):
        # Apply a red dim to the text area to create a sense of panic
        palette = self.text_edit.palette()
        palette.setColor(QPalette.Base, QColor(255, 102, 102))  # Light red background
        self.text_edit.setPalette(palette)

    def clear_red_dim(self):
        # Clear the red dim effect
        palette = self.text_edit.palette()
        palette.setColor(QPalette.Base, QColor(255, 255, 255))  # Reset to white background
        self.text_edit.setPalette(palette)

    def update_word_count(self):
        text = self.text_edit.toPlainText()
        word_count = len(text.split())
        self.word_count_label.setText(f"Words: {word_count}")

def main():
    app = QApplication(sys.argv)
    window = DangerousWritingApp()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
