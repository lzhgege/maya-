#  -*- coding: utf-8 -*-

import sys
import os
import maya.cmds as cmds
import maya.OpenMayaUI as omui
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget, QTextEdit, QGroupBox, QMenuBar, QPushButton, QGridLayout
import maya.utils as utils
import maya.mel as mel
from shiboken2 import wrapInstance
from PySide2.QtGui import QIcon
from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QLabel
from PySide2.QtWidgets import QSpacerItem
from PySide2.QtWidgets import QSizePolicy
from PySide2.QtWidgets import QScrollArea
from PySide2.QtCore import QSize
import json



# 添加模块的查找路径
module_folder = r'C:\Maya_toolbox\plug-in\material\template'
if module_folder not in sys.path:
    sys.path.append(module_folder)



import material_dialog1
import material_dialog2
import material_dialog3
import material_dialog4
import material_dialog5
import material_dialog6
import material_dialog7
import material_dialog8
import material_dialog9
import material_dialog10

class ToolBox(QWidget):
    def __init__(self, parent=None):
        super(ToolBox, self).__init__(parent)
        self.setWindowTitle(u"场景工具箱")
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # 垂直布局
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        # 标签页窗口
        tab_widget = QTabWidget()
        main_layout.addWidget(tab_widget)

        # 常用工具页
        common_tools_page = QWidget()
        common_tools_layout = QVBoxLayout()
        common_tools_page.setLayout(common_tools_layout)
        tab_widget.addTab(common_tools_page, u"常用工具")

        # 实用工具页
        useful_tools_page = QWidget()
        useful_tools_layout = QVBoxLayout()
        useful_tools_page.setLayout(useful_tools_layout)
        tab_widget.addTab(useful_tools_page, u"材质库")

        # 获取JSON文件的路径
        toolDatajson_path = ("C:/Maya_toolbox/plug-in/toolData.json")

        # 加载JSON文件中的按钮信息
        with open(toolDatajson_path, 'r') as file:
            data = json.load(file)

        buttons = data["toolData"]

        # 创建一个新的网格布局
        maya_tools_layout = QGridLayout()

        # 设置按钮之间的水平和垂直间距为 0
        maya_tools_layout.setHorizontalSpacing(0)
        maya_tools_layout.setVerticalSpacing(0)

        # 添加按钮和名称
        for i, button_info in enumerate(buttons):
            button = QPushButton()
            button.setFixedSize(60, 60)
            button.setIcon(QIcon(button_info["icon"]))
            button.clicked.connect(lambda command=button_info["command"]: eval(command))

            # 创建一个垂直布局，以便排列按钮和名称
            button_layout = QVBoxLayout()
            button_layout.addWidget(button, alignment=Qt.AlignCenter)

            name_label = QLabel(button_info["name"])
            name_label.setAlignment(Qt.AlignCenter)
            button_layout.addWidget(name_label, alignment=Qt.AlignCenter)

            # 添加一个QSpacerItem控件，以便调整按钮之间的间距
            spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
            button_layout.addItem(spacer)

            # 将垂直布局添加到QWidget中
            button_widget = QWidget()
            button_widget.setLayout(button_layout)

            # 将QWidget添加到网格布局中
            maya_tools_layout.addWidget(button_widget, i // 4, i % 4)



        # 将滑动条添加到布局中
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(300)
        scroll_widget = QWidget()
        scroll_widget.setLayout(maya_tools_layout)
        scroll.setWidget(scroll_widget)

        common_tools_layout.addWidget(scroll)

        # 获取JSON文件的路径
        scriptDatajson_path = ("C:/Maya_toolbox/plug-in/scriptData.json")

        # 加载JSON文件中的按钮信息
        with open(scriptDatajson_path, 'r') as file:
            data = json.load(file)

        buttons = data["script"]

        # 创建一个新的网格布局
        plugin_layout = QGridLayout()

        # 设置按钮之间的水平和垂直间距为 0
        plugin_layout.setHorizontalSpacing(0)
        plugin_layout.setVerticalSpacing(0)

        # 添加按钮和名称
        for i, button_info in enumerate(buttons):
            button = QPushButton()
            button.setFixedSize(60, 60)
            button.setIcon(QIcon(button_info["icon"]))
            button.clicked.connect(lambda command=button_info["command"]: run_script(command))


            # 创建一个垂直布局，以便排列按钮和名称
            button_layout = QVBoxLayout()
            button_layout.addWidget(button, alignment=Qt.AlignCenter)

            name_label = QLabel(button_info["name"])
            name_label.setAlignment(Qt.AlignCenter)
            button_layout.addWidget(name_label, alignment=Qt.AlignCenter)

            # 创建一个垂直布局，以便排列按钮和名称
            button_layout = QVBoxLayout()
            button_layout.addWidget(button, alignment=Qt.AlignCenter)

            name_label = QLabel(button_info["name"])
            name_label.setAlignment(Qt.AlignCenter)
            button_layout.addWidget(name_label, alignment=Qt.AlignCenter)

            # 添加一个QSpacerItem控件，以便调整按钮之间的间距
            spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
            button_layout.addItem(spacer)

            # 将垂直布局添加到QWidget中
            button_widget = QWidget()
            button_widget.setLayout(button_layout)

            # 将QWidget添加到网格布局中
            plugin_layout.addWidget(button_widget, i // 4, i % 4)

        # 将可滚动区域添加到 QVBoxLayout 中
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(300)
        scroll_widget = QWidget()
        scroll_widget.setLayout(plugin_layout)
        scroll.setWidget(scroll_widget)

        common_tools_layout.addWidget(scroll)

        # 预设材质球按钮
        preset_material_group = QGroupBox(u"预设材质球")
        preset_material_layout = QGridLayout()
        preset_material_group.setLayout(preset_material_layout)

        json_file = 'material_dialogs.json'
        json_path = os.path.abspath(os.path.join(module_folder, json_file))

        # 定义icons_folder变量
        icons_folder = os.path.join(module_folder, 'icons')

        # 读取json文件
        with open(json_path, 'r') as f:
            material_dialogs = json.load(f)

        # 添加预设材质球按钮
        row = 0
        column = 0
        for dialog in material_dialogs:
            button = QPushButton()
            icon = QIcon(os.path.join(icons_folder, dialog['icon']))
            button.setIcon(icon)
            button.setIconSize(QSize(70, 70))
            button.setFixedSize(80, 80)
            button.clicked.connect(eval(dialog['function']))

            label = QLabel(dialog['name'])
            label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
            label.setWordWrap(True)

            layout = QVBoxLayout()
            layout.addWidget(button)
            layout.addWidget(label)

            widget = QWidget()
            widget.setLayout(layout)

            preset_material_layout.addWidget(widget, row, column)

            # 每行最多显示3个按钮，超出的换行显示
            column += 1
            if column > 2:
                row += 1
                column = 0

        # 如果按钮数不足 3
        # 个，则将 layout 的高度扩充到 2 行
        if len(material_dialogs) < 3:
            preset_material_layout.setRowStretch(1, 1)


        # 添加滑动条
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(300)
        scroll.setWidget(preset_material_group)

        useful_tools_layout.addWidget(scroll)  # 将滑动条加到布局中

        useful_material_group = QGroupBox(u"实用材质球")
        useful_material_layout = QVBoxLayout()
        useful_material_text_box = QTextEdit()
        useful_material_text_box.setReadOnly(True)
        useful_material_text_box.setPlainText(u"这是中文测试")
        useful_material_text_box.setMinimumHeight(150)
        useful_material_layout.addWidget(useful_material_text_box)
        useful_material_group.setLayout(useful_material_layout)
        useful_tools_layout.addWidget(useful_material_group)

        # 菜单栏
        menu_bar = QMenuBar()
        self.layout().setMenuBar(menu_bar)

        menu = menu_bar.addMenu(u"菜单")
        material_settings_menu = menu_bar.addMenu(u"材质库设置")

        menu.addAction(u"aaa")
        menu.addAction(u"bbb")
        menu.addAction(u"ccc")

        material_settings_menu.addAction(u"路径设置")
        material_settings_menu.addAction(u"保存到实用材质库")


def create_toolbox():
    maya_win = maya_main_window()
    workspace_control_name = "ToolboxWorkspaceControl"

    if cmds.workspaceControl(workspace_control_name, q=1, exists=1):
        cmds.deleteUI(workspace_control_name)

    toolbox = ToolBox(parent=maya_win)

    control = cmds.workspaceControl(
        workspace_control_name,
        label=u"场景工具箱",
        floating=1,
        retain=1,
        w=310,
        h=600
    )



    qt_ctrl = omui.MQtUtil.findControl(control)
    widget = wrapInstance(long(qt_ctrl), QWidget)
    layout = widget.layout()
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(toolbox)

    toolbox.show()

    # 更新UI
    QApplication.processEvents()

    return toolbox


def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    if main_window_ptr is None:
        return None
    return wrapInstance(long(main_window_ptr), QWidget)

def run_script(script):
    extension = script.split('.')[-1]
    if extension == 'py':
        import maya.cmds as cmds
        cmds.file(new=True, force=True)
        exec(open(script).read())
    elif extension == 'mel':
        import maya.mel as mel
        mel.eval(open(script).read())
    else:
        print("Unsupported script format")
if __name__ == "__main__":
    toolbox = create_toolbox()
