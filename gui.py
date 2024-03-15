from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTextEdit,
)
from PyQt5.QtCore import QDate, QTime, QEvent, Qt
from PyQt5.QtGui import QColor, QTextCursor
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


class HighlightingTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_L and (event.modifiers() & Qt.ControlModifier):
            self.highlightCurrentLine()
        elif event.key() == Qt.Key_BracketRight and (
            event.modifiers() & Qt.ControlModifier
        ):
            self.indentCurrentLine('indent')
        elif event.key() == Qt.Key_BracketLeft and (
            event.modifiers() & Qt.ControlModifier
        ):
            self.indentCurrentLine('dedent')
        elif event.key() == Qt.Key_I and (
            event.modifiers() & Qt.ControlModifier
        ):
            self.autoFormatText(line_length=33, hyphen_split=False)
        else:
            super().keyPressEvent(event)

    def highlightCurrentLine(self):
        cursor = self.textCursor()
        cursor.select(QTextCursor.LineUnderCursor)
        extraSelections = []

        selection = QTextEdit.ExtraSelection()
        selection.format.setBackground(QColor(Qt.yellow).lighter(160))
        selection.cursor = cursor

        extraSelections.append(selection)
        self.setExtraSelections(extraSelections)

    def autoFormatText(self, line_length=80, hyphen_split=False):
        s = self.toPlainText()
        lines = s.split('\n')
        further = 2 * " "

        for i in range(len(lines)):
            idt_level = len(lines[i]) - len(lines[i].lstrip())
            joiner = ' ' * idt_level + further
            if len(lines[i]) > line_length:
                # Initial split into head and tail
                head, tail = lines[i][:line_length], lines[i][line_length:]
                lines[i] = head  # Update the line with just the head to start
                new_length = line_length - len(joiner)
                # Process the tail in chunks, appending each chunk to lines[i] with appropriate indentation
                while len(tail) > new_length:
                    head, tail = tail[:new_length], tail[new_length:]
                    lines[i] += '\n' + joiner + head
                # Append any remaining tail with appropriate indentation
                if tail:
                    lines[i] += '\n' + joiner + tail

        formatted_text = '\n'.join(lines)
        self.setPlainText(formatted_text)

    def indentCurrentLine(self, action='indent'):
        cursor = self.textCursor()  # Get the current cursor position
        current_line_number = cursor.blockNumber()  # Identify the current line
        text = self.toPlainText()  # Capture all text
        lines = text.split('\n')  # Split text into lines

        # Check if current line is within the range of lines
        if 0 <= current_line_number < len(lines):
            if action == 'indent':
                lines[current_line_number] = (
                    "  " + lines[current_line_number]
                )  # Add indentation
            elif action == 'dedent':
                # Remove indentation if present
                lines[current_line_number] = lines[current_line_number].lstrip(
                    ' '
                )
                if lines[current_line_number].startswith("  "):
                    lines[current_line_number] = lines[current_line_number][2:]

            updated_text = "\n".join(lines)  # Rejoin the text
            self.setPlainText(updated_text)  # Update the widget's text

            # Restore the cursor to an appropriate position
            cursor.setPosition(0)
            for _ in range(current_line_number):
                cursor.movePosition(QTextCursor.Down)
            # if action == 'dedent':
            #     cursor.movePosition(QTextCursor.EndOfLine)
            # else:
            #     cursor.movePosition(
            #         QTextCursor.Right, QTextCursor.MoveAnchor, 2
            #     )  # Adjust for added spaces
            cursor.movePosition(QTextCursor.EndOfLine)
            self.setTextCursor(cursor)  # Apply the cursor with the new position


class CustomDateTimePicker(QWidget):
    def __init__(self, overwrite=True):
        super().__init__()
        self.overwrite = overwrite
        self.initUI()

    def initUI(self):
        mainLayout = QVBoxLayout(self)

        self.recipientCombo = QComboBox(self)
        self.recipientCombo.setEditable(True)
        self.recipientCombo.setPlaceholderText("Recipient Name or Number")
        contacts = get_contacts()
        self.recipientCombo.addItems(list(contacts.keys()))
        mainLayout.addWidget(self.recipientCombo)

        self.messageText = HighlightingTextEdit(self)
        self.messageText.setPlaceholderText("Your message...")
        mainLayout.addWidget(self.messageText)

        pickerLayout = QHBoxLayout()
        currentDate = QDate.currentDate()
        currentTime = QTime.currentTime()

        months = [QDate.longMonthName(month) for month in range(1, 13)]
        self.monthBox = ScrollableComboBox(months, self)
        self.monthBox.setCurrentIndex(currentDate.month() - 1)
        pickerLayout.addWidget(self.monthBox)

        days = [str(day) for day in range(1, 32)]
        self.dayBox = ScrollableComboBox(days, self)
        self.dayBox.setCurrentIndex(currentDate.day() - 1)
        pickerLayout.addWidget(self.dayBox)

        hours = [f"{hour:02d}" for hour in range(1, 13)]
        self.hourBox = ScrollableComboBox(hours, wraparound=True, parent=self)
        hourIn12HFormat = (currentTime.hour() % 12) or 12
        self.hourBox.setCurrentIndex(hourIn12HFormat - 1)
        pickerLayout.addWidget(self.hourBox)

        minutes = [f"{minute:02d}" for minute in range(60)]
        self.minuteBox = ScrollableComboBox(minutes, self)
        self.minuteBox.setCurrentIndex(currentTime.minute())
        pickerLayout.addWidget(self.minuteBox)

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
        lines_filtered = [
            e.strip()
            for e in s.split("\n")
            if e != "" and not e.strip().startswith("#")
        ]
        d = {e.split('=')[0]: e.split('=')[1] for e in lines_filtered}
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
            with open("SETTINGS.txt", "w") as file:
                file.write("\n".join([f"{k}={v}" for k, v in d.items()]))

        with open(fileName, "w") as file:
            file.write(message)

        # self.close()
        # clear the message box and contact
        self.messageText.clear()
        self.recipientCombo.clearEditText()
        os.system('python send_scheduled_messages.py')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    picker = CustomDateTimePicker()
    picker.show()
    sys.exit(app.exec_())
