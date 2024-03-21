from functools import cached_property
import sys
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets


class WebView(QtWebEngineWidgets.QWebEngineView):
    def createWindow(self, type_):
        if not isinstance(self.window(), Browser):
            return

        if type_ == QtWebEngineWidgets.QWebEnginePage.WebBrowserTab:
            return self.window().tab_widget.create_tab()


class TabWidget(QtWidgets.QTabWidget):
    def create_tab(self):
        view = WebView()

        index = self.addTab(view, "(Untitled)")
        self.setTabIcon(index, view.icon())
        view.titleChanged.connect(
            lambda title, view=view: self.update_title(view, title)
        )
        view.iconChanged.connect(lambda icon, view=view: self.update_icon(view, icon))
        self.setCurrentWidget(view)
        return view

    def update_title(self, view, title):
        index = self.indexOf(view)
        self.setTabText(index, title)

    def update_icon(self, view, icon):
        index = self.indexOf(view)
        self.setTabIcon(index, icon)


class Browser(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCentralWidget(self.tab_widget)
        
        

        view = self.tab_widget.create_tab()
        view.load(QtCore.QUrl("https://www.google.com/"))

        QtWebEngineWidgets.QWebEngineProfile.defaultProfile().downloadRequested.connect(self.on_downloadRequested)

    @QtCore.pyqtSlot("QWebEngineDownloadItem*")
    def on_downloadRequested(self, download):
        old_path = download.url().path()  # download.path()
        suffix = QtCore.QFileInfo(old_path).suffix()
        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save File", old_path, "*." + suffix
        )
        if path:
            download.setPath(path)
            download.accept()

    
    @cached_property
    def tab_widget(self):
        return TabWidget()


def main():
    app = QtWidgets.QApplication(sys.argv)
    w = Browser()
    w.show()
    w.showMaximized()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
