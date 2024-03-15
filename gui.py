from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QTextEdit,
    QPushButton,
)
from PyQt5.QtCore import QDate, QTime, QEvent
import sys
import os


def get_contacts(exc=None):
    if exc is None:
        exc = [
            "MAX_OVERTIME_MINS",
            "DEBUG_TEXTING",
            "SCHEDULED_TEXTS_DIRECTORY",
            "sms_myself",
        ]
    with open("SETTINGS.txt", "r") as file:
        lines = file.read().split("\n")
        lines = [line for line in lines if line and not line.startswith("#")]
        lines = [line.split("=") for line in lines]
        lines = [line for line in lines if line[0] not in exc]
        d = {line[0]: line[1] for line in lines}
    return d


class ScrollableComboBox(QComboBox):
    def __init__(self, items=[], wraparound=False, parent=None):
        super().__init__(parent)
        self.setEditable(True)  # Allow for typing in combo box
        self.addItems(items)
        self.wraparound = wraparound
        self.installEventFilter(self)

    def eventFilter(self, source, event):
        if event.type() == QEvent.Wheel and source is self:
            currentIndex = self.currentIndex()
            if event.angleDelta().y() > 0:  # Scroll up
                newIndex = currentIndex - 1
                if self.wraparound and newIndex < 0:
                    newIndex = self.count() - 1
            else:  # Scroll down
                newIndex = currentIndex + 1
                if self.wraparound and newIndex >= self.count():
                    newIndex = 0

            if 0 <= newIndex < self.count() or self.wraparound:
                self.setCurrentIndex(newIndex)
            return True
        return super().eventFilter(source, event)


class CustomDateTimePicker(QWidget):
    def __init__(self, overwrite=True):
        super().__init__()
        self.overwrite = overwrite
        self.initUI()

    def initUI(self):
        mainLayout = QVBoxLayout(self)

        # Recipient dropdown and text input combo box
        self.recipientCombo = QComboBox(self)
        self.recipientCombo.setEditable(True)
        self.recipientCombo.setPlaceholderText("Recipient Name or Number")

        contacts = get_contacts()
        self.recipientCombo.addItems(list(contacts.keys()))
        mainLayout.addWidget(self.recipientCombo)

        # Message text input with adjustable width
        self.messageText = QTextEdit(self)
        self.messageText.setPlaceholderText("Your message...")
        self.messageText.setFixedWidth(240)  # Adjust width as needed
        mainLayout.addWidget(self.messageText)

        pickerLayout = QHBoxLayout()
        currentDate = QDate.currentDate()
        currentTime = QTime.currentTime()

        # Month selection
        months = [QDate.longMonthName(month) for month in range(1, 13)]
        self.monthBox = ScrollableComboBox(months, self)
        self.monthBox.setCurrentIndex(currentDate.month() - 1)
        pickerLayout.addWidget(self.monthBox)

        # Day selection
        days = [
            str(day) for day in range(1, 32)
        ]  # Placeholder, adjust based on the month
        self.dayBox = ScrollableComboBox(days, self)
        self.dayBox.setCurrentIndex(currentDate.day() - 1)
        pickerLayout.addWidget(self.dayBox)

        # Hour selection, adjust for 12-hour format
        hours = [f"{hour:02d}" for hour in range(1, 13)]
        self.hourBox = ScrollableComboBox(hours, wraparound=True, parent=self)
        hourIn12HFormat = (currentTime.hour() % 12) or 12
        self.hourBox.setCurrentIndex(hourIn12HFormat - 1)
        pickerLayout.addWidget(self.hourBox)

        # Minute selection
        minutes = [f"{minute:02d}" for minute in range(60)]
        self.minuteBox = ScrollableComboBox(minutes, self)
        self.minuteBox.setCurrentIndex(currentTime.minute())
        pickerLayout.addWidget(self.minuteBox)

        # AM/PM selection
        ampm = ["AM", "PM"]
        self.ampmBox = ScrollableComboBox(ampm, wraparound=True, parent=self)
        self.ampmBox.setCurrentIndex(0 if currentTime.hour() < 12 else 1)
        pickerLayout.addWidget(self.ampmBox)

        mainLayout.addLayout(pickerLayout)
        self.setLayout(mainLayout)
        self.setWindowTitle("Schedule Message")

        self.scheduleButton = QPushButton("Schedule", self)
        self.scheduleButton.clicked.connect(self.createScheduleFile)
        mainLayout.addWidget(self.scheduleButton)

    def createScheduleFile(self):
        recipientName = self.recipientCombo.currentText()
        message = self.messageText.toPlainText()
        month = self.monthBox.currentText()
        day = self.dayBox.currentText()
        hour = self.hourBox.currentText()
        minute = self.minuteBox.currentText()
        ampm = self.ampmBox.currentText()

        s = open("SETTINGS.txt", "r").read()
        lines = s.split("\n")
        lines_filtered = [
            e.strip()
            for e in lines
            if e != "" and not e.strip().startswith("#")
        ]
        d = {e.split("=")[0]: e.split("=")[1] for e in lines_filtered}
        root = os.path.abspath(d["SCHEDULED_TEXTS_DIRECTORY"])

        fileName = (
            f"Text {recipientName} {month} {day}, {hour}:{minute}{ampm}.txt"
        )
        fileName = os.path.join(root, fileName)

        settingsEdited = False
        if "=" in recipientName:
            name, number = recipientName.split("=")
            if name in d and d[name] != number:
                if self.overwrite:
                    d[name] = number
                    settingsEdited = True
                else:
                    raise ValueError(
                        f"Recipient {name} already exists with a different number."
                    )
            else:
                d[name] = number
                settingsEdited = True

        if settingsEdited:
            print(f"Adding {name}={number} to SETTINGS.txt")
            with open("SETTINGS.txt", "w") as file:
                file.write("\n".join([f"{k}={v}" for k, v in d.items()]))

        with open(fileName, "w") as file:
            file.write(message)

        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    picker = CustomDateTimePicker()
    picker.show()
    sys.exit(app.exec_())
