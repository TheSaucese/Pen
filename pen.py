import sys
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap, QTransform, QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget, QLabel, QTabBar, QWidget, QSizePolicy
import qdarktheme
from tabs.attack import AttackWidget
from tabs.vuln import VulnWidget
from tabs.scan import ScanWidget
from qdarktheme.qtpy.QtCore import Qt
from qdarktheme.qtpy.QtWidgets import QMainWindow

class CustomTabBar(QTabBar):
    def tabSizeHint(self, index):
        size = super(CustomTabBar, self).tabSizeHint(index)
        if index == 3:
            return QSize(size.width(), self.height() - 350)
        return size

class CustomTabWidget(QTabWidget):
    def __init__(self, *args, **kwargs):
        super(CustomTabWidget, self).__init__(*args, **kwargs)
        self.setTabBar(CustomTabBar())
        self.setTabPosition(QTabWidget.West)
        self.setDocumentMode(True)
        self.setMovable(True)

class Pen(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize the toggle attribute
        self.toggle = "dark"

        self.previous_index=0

        self.initUI()

    def initUI(self):
        self.scanWidget = ScanWidget()
        self.vulnWidget = VulnWidget()
        self.attackWdiget = AttackWidget()

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        empty_icon_pixmap = QPixmap(1, 100)
        empty_icon_pixmap.fill(Qt.transparent)
        empty_icon = QIcon(empty_icon_pixmap)

        button_tab = QLabel("", self)

        qdarktheme.setup_theme("auto")

        self.tab_widget = CustomTabWidget(self)
        self.tab_widget.setIconSize(QSize(64, 64))
        self.tab_widget.addTab(self.scanWidget, QIcon(QPixmap("images/scan.svg").transformed(QTransform().rotate(90))), "")
        self.tab_widget.addTab(self.vulnWidget, QIcon(QPixmap("images/vuln.svg").transformed(QTransform().rotate(90))), "")
        self.tab_widget.addTab(self.attackWdiget, QIcon(QPixmap("images/attack.svg").transformed(QTransform().rotate(90))), "")
        self.tab_widget.addTab(spacer, empty_icon, "")
        self.tab_widget.addTab(button_tab, QIcon(QPixmap("images/light.svg").transformed(QTransform().rotate(90))), "")
        self.tab_widget.setTabEnabled(3, False)
        self.tab_widget.currentChanged.connect(self.handle_tab_changed)
        self.tab_widget.setStyleSheet("QTabBar::tab:hover {"
                                      "    "
                                      "}"
                                      ""
                                      "QTabBar::tab:selected{"
                                      "    "
                                      "}"
                                      "QTabBar::tab {"
                                      "    margin: 0px;"
                                      "}")
        self.tab_widget.setUsesScrollButtons(False)


        # Show the tab widget here
        self.setCentralWidget(self.tab_widget)

    def handle_vulnerabilities_clicked(self):
        # Switch to the Vulnerabilities tab when the "vulnerabilities" link is clicked
        self.tab_widget.setCurrentIndex(1)

    def handle_tab_changed(self, index):
        if index == 4:
            if self.toggle == "dark":
                self.tab_widget.setTabIcon(4, QIcon(QPixmap("images/dark.svg").transformed(QTransform().rotate(90))))
                self.toggle = "light"
            else:
                self.tab_widget.setTabIcon(4, QIcon(QPixmap("images/light.svg").transformed(QTransform().rotate(90))))
                self.toggle = "dark"
            qdarktheme.setup_theme(self.toggle)
            self.tab_widget.setCurrentIndex(self.previous_index)
        else:
            self.previous_index = index

if __name__ == "__main__":
    qdarktheme.enable_hi_dpi()
    app = QApplication(sys.argv)
    window = Pen()
    window.setGeometry(100, 100, 800, 600)  # Adjust the window size if needed
    window.setWindowTitle("Pen")
    window.show()
    sys.exit(app.exec())
