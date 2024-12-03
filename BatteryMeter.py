import sys
import psutil
# Ensure PyQt5 is installed:
# python -m pip install PyQt5
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QProgressBar
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QMouseEvent

class BatteryWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Window properties for desktop widget behavior
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnBottomHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setGeometry(100, 100, 250, 100)  # Default position and size

        # Set custom style and background
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(0, 0, 0, 150);  /* Semi-transparent black */
                border: 2px solid rgba(255, 255, 255, 100);  /* White border */
                border-radius: 10px;
                color: white;  /* Text color */
            }
            QLabel {
                font-size: 14px;
            }
            QProgressBar {
                border: 2px solid rgba(255, 255, 255, 100);
                border-radius: 5px;
                background: rgba(255, 255, 255, 50);
                text-align: center;
                color: white;
            }
            QProgressBar::chunk {
                background-color: rgba(50, 200, 50, 200);  /* Green chunk */
                width: 10px;
            }
        """)

        # Layout and Widgets
        self.layout = QVBoxLayout()
        self.battery_label = QLabel("Battery Status:")
        self.battery_bar = QProgressBar()
        self.layout.addWidget(self.battery_label)
        self.layout.addWidget(self.battery_bar)
        self.setLayout(self.layout)

        # Update Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_battery)
        self.timer.start(1000)  # Update every second

        self.update_battery()

    def update_battery(self):
        """Fetch and display battery information."""
        battery = psutil.sensors_battery()
        if battery:
            percent = battery.percent
            plugged = "Plugged In" if battery.power_plugged else "On Battery"
            self.battery_label.setText(f"Battery Status: {percent}% ({plugged})")
            self.battery_bar.setValue(percent)
        else:
            self.battery_label.setText("Battery Status: Not Available")

    def mousePressEvent(self, event: QMouseEvent):
        """Capture the initial position when the mouse is pressed."""
        if event.button() == Qt.LeftButton:
            self.oldPos = event.globalPos()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        """Move the widget with the mouse."""
        if event.buttons() == Qt.LeftButton:
            delta = event.globalPos() - self.oldPos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent):
        """Handle mouse release event."""
        if event.button() == Qt.LeftButton:
            event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = BatteryWidget()
    widget.show()
    sys.exit(app.exec_())
