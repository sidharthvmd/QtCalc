import sys
from PyQt5.QtWidgets import(
    QApplication,QWidget,QMainWindow,QGridLayout,QVBoxLayout,QLineEdit,QPushButton
)
from PyQt5.QtCore import Qt
from functools import partial

WINDOW_SIZE=235
DISPLAY_HEIGHT=35
BUTTON_SIZE=40
ERROR="ERROR"

class qtcalcWin(QMainWindow):
    """Main window of calculator"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("QtCalc")
        self.setFixedSize(WINDOW_SIZE,WINDOW_SIZE) #set unchangeable size
        self.generalLayout=QVBoxLayout()
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(centralWidget)
        self._createDisplay()
        self._createButtons()

    def _createDisplay(self):
        self.display=QLineEdit()
        self.display.setFixedHeight(DISPLAY_HEIGHT)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        self.generalLayout.addWidget(self.display)

    def _createButtons(self):
        self.buttonMap={}
        buttonsLayout=QGridLayout()
        keyBoard = [
            ["7","8","9","/","C"],
            ["4","5","6","*","("],
            ["1","2","3","-",")"],
            ["0","00",".","+","="],
            ]
        for rows, keys in enumerate (keyBoard):
            for col,key in enumerate (keys):
                self.buttonMap[key]=QPushButton(key)
                self.buttonMap[key].setFixedSize(BUTTON_SIZE,BUTTON_SIZE)
                buttonsLayout.addWidget(self.buttonMap[key],rows,col)
            self.generalLayout.addLayout(buttonsLayout)

    def setDisplayText(self,text):
        self.display.setText(text)
        self.display.setFocus()#doubt
    
    def displayText(self):
        return self.display.text()

    def clearDisplay(self):
        self.setDisplayText("")

def evaluateExpression(expression):
        try:
            result= str(eval(expression,{},{}))#doubt
        except Exception:
            result= ERROR
        return result


class QTCalc:
    def __init__(self,model,view):
        self._evaluate=model
        self._view=view
        self._connectSignalsAndSlots()

    def _calculateResult(self):
        result=self._evaluate(expression=self._view.displayText())
        self._view.setDisplayText(result)

    def _buildExpression(self,subExpression):
        if self._view.displayText()==ERROR:
            self._view.clearDisplay()
        expression = self._view.displayText() + subExpression
        self._view.setDisplayText(expression)

    def _connectSignalsAndSlots(self):
        for keySymbol, button in self._view.buttonMap.items():
            if keySymbol not in {"=","C"}:
                button.clicked.connect(partial(self._buildExpression,keySymbol))
        self._view.buttonMap["="].clicked.connect(self._calculateResult)
        self._view.display.returnPressed.connect(self._calculateResult)
        self._view.buttonMap["C"].clicked.connect(self._view.clearDisplay)

def main():
    qtcalcApp = QApplication([])
    qtcalcwin = qtcalcWin()
    qtcalcwin.show()
    QTCalc(model=evaluateExpression,view=qtcalcwin)
    sys.exit(qtcalcApp.exec())

if __name__ == "__main__":
    main()
