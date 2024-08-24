import sys
from PyQt5.QtWidgets import QApplication
from zoe.zoe_Interfaz import ZoeInterface

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ZoeInterface()
    window.show()
    sys.exit(app.exec_())
