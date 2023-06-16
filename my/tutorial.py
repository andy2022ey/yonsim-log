import sys
import os
import traceback

from PyQt6.QtWidgets import QApplication, QTextBrowser, QWidget, QHBoxLayout, QTreeView, QMessageBox
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QIcon
from PyQt6.QtCore import Qt


class YonsimCatalog(QWidget):
    """永芯教程目录"""

    def __init__(self):
        super().__init__()
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            self.temporary_path = sys._MEIPASS
        else:
            self.temporary_path = os.path.abspath('.')
        # 窗口居中放置
        ico_path = os.path.join(self.temporary_path, 'statics', 'book.ico')
        self.setWindowIcon(QIcon(ico_path))
        screen = QApplication.primaryScreen()
        rect = screen.geometry()
        self.move(int(rect.width() / 2 - self.width() / 2), 0)
        self.setWindowTitle("永芯使用教程")
        layout = QHBoxLayout()
        self.setLayout(layout)
        self.model = QStandardItemModel()

        report = self.add_root_node("报告自动化")
        for i in ['Info', 'TB', '参数', '段落模板', '表格模板', '蓝图模板', '生成报告']:
            self.add_child_node(report, i)
        self.add_root_node("底稿自动化")
        self.add_root_node("终端控制器")
        self.add_root_node("运行队列")
        self.add_root_node("里程碑")
        self.add_root_node("充值系统")

        self.view = QTreeView()
        self.view.setMaximumWidth(200)
        self.view.setModel(self.model)
        self.view.clicked.connect(self.on_node_clicked)
        # 隐藏表头
        self.view.header().hide()

        self.text_browser = Browser()
        layout.addWidget(self.view)
        layout.addWidget(self.text_browser)

    def add_root_node(self, name):
        item = QStandardItem(name)
        self.model.appendRow(item)
        return item

    def add_child_node(self, parent, name):
        item = QStandardItem(name)
        parent.appendRow(item)
        return item

    def on_node_clicked(self, index):
        node = self.model.itemFromIndex(index)
        if node.hasChildren():
            if self.view.isExpanded(index):
                self.view.collapse(index)
            else:
                self.view.expand(index)
        else:
            value = node.text()
            self.text_browser.setText(self.read_html(value))
            # self.text_browser.setAlignment(Qt.AlignmentFlag.AlignTop)

    def read_html(self, name):
        path = os.path.join(self.temporary_path, 'htmls', name + '.html')
        with open(path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        base_path = os.path.join(self.temporary_path)
        html_content = html_content.format(base_path=base_path.replace('\\', '/'))
        return html_content


class Browser(QTextBrowser):
    """教程浏览器"""
    def __init__(self):
        super().__init__()
        self.setText(self.text)
        self.setOpenExternalLinks(True)
        self.setMinimumWidth(500)
        self.setMinimumHeight(600)

    @property
    def text(self):
        text = """
        <h1>永芯教程</h1>
        <p>永芯教程是永芯科技的一套教程，用于指导用户使用永芯软件。</p>
        <p>永芯教程包含以下内容：</p>
        """
        return text


if __name__ == '__main__':
    app = QApplication(sys.argv)
    try:
        demo = YonsimCatalog()
        demo.show()
    except:
        info = traceback.format_exc()
        QMessageBox.critical(None, '错误', info)

    sys.exit(app.exec())


