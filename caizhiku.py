#  -*- coding: utf-8 -*-
import maya.cmds as cmds
import os
import sys

# 添加模块的查找路径
module_folder = r'C:\Maya_toolbox\plug-in\material'
if module_folder not in sys.path:
    sys.path.append(module_folder)

# 材质库窗口类
class MaterialLibrary:
    def __init__(self):
        self.window_name = "material_library"
        self.preview_width = 80
        self.preview_height = 80
        self.material_folder = r'C:\Maya_toolbox\plug-in\material\template\Material_library'
        self.init_materials()

    # 初始化材质球列表
    def init_materials(self):
        self.materials = []
        files = os.listdir(self.material_folder)
        for filename in files:
            if filename.endswith(".mtl") or filename.endswith(".ma"):
                name, ext = os.path.splitext(filename)
                preview_file = os.path.join(self.material_folder, "%s.png" % name)
                if not os.path.isfile(preview_file):
                    preview_file = os.path.join(self.material_folder, "Material.png")
                else:
                    preview_file = os.path.join(self.material_folder, "%s.png" % name)
                self.materials.append(
                    {"name": name, "preview": preview_file, "file": os.path.join(self.material_folder, filename)})

    # 打开材质库窗口
    def open(self):
        if cmds.window(self.window_name, exists=True):
            cmds.deleteUI(self.window_name)
        cmds.window(self.window_name, title="材质库", width=500, height=600)
        cmds.menuBarLayout()
        cmds.columnLayout()
        cmds.separator(height=15)
        self.create_material_buttons()
        self.menu = cmds.menu(label="编辑")
        cmds.menuItem(label="刷新材质库", command=lambda x: self.refresh_materials(), parent=self.menu)
        cmds.menuItem(label="导出材质球", command=lambda x: self.export_selected_material(), parent=self.menu)
        cmds.showWindow()

    # 创建材质球按钮
    def create_material_buttons(self):
        material_layout = cmds.rowColumnLayout(nc=5, cw=[(1, self.preview_width), (2, self.preview_width),
                                                         (3, self.preview_width), (4, self.preview_width),
                                                         (5, self.preview_width)], columnSpacing=[(1, 10), (2, 10),
                                                                                                  (3, 10), (4, 10),
                                                                                                  (5, 10)],
                                               rowSpacing=[(1, 10), (2, 10), (3, 10), (4, 10), (5, 10)])
        for material in self.materials:
            cmds.columnLayout()
            cmds.iconTextButton(label=material["name"], image1=material["preview"], width=self.preview_width,
                                height=self.preview_height, style="iconAndTextVertical",
                                command=lambda x, material=material: self.preview_material(material))
            cmds.setParent("..")
            cmds.popupMenu(button=3)
            cmds.menuItem(label="导入材质球", command=lambda x, material=material: self.import_material(material))

            cmds.setParent(material_layout)

    # 预览材质球
    def preview_material(self, material):
        cmds.select(clear=True)
        shading_group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name="%s_sg" % material["name"])
        cmds.shadingNode("lambert", asShader=True, name=material["name"])
        cmds.sets(forceElement=shading_group, e=True)
        cmds.select(clear=True)
        cmds.select(shading_group)
        cmds.rename("preview", shading_group)
        file_node = cmds.shadingNode('file', asTexture=True, name="preview_texture")
        cmds.setAttr('%s.fileTextureName' % file_node, material["preview"], type='string')
        cmds.connectAttr('%s.outColor' % file_node, '%s.color' % shading_group)

    # 导入材质球
    def import_material(self, material):
        selection = cmds.ls(selection=True)

        cmds.select(selection)
        cmds.file(material["file"], i=True)

    # 导出所选材质球
    def export_selected_material(self):
        materials = cmds.ls(selection=True, mat=True)
        if materials:
            material_name = materials[0]
            file = os.path.join(self.material_folder, material_name + ".ma")
            cmds.select(material_name)
            cmds.file(file, op="v=0;", typ="mayaAscii", es=True, f=True, ch=False)
            print("成功导出材质球：" + material_name)
        else:
            print("请先选择需要导出的材质球")

    # 刷新材质库
    def refresh_materials(self):
        self.init_materials()
        cmds.deleteUI(self.window_name)
        library = MaterialLibrary()
        library.open()


# 创建材质库对象，并打开窗口
library = MaterialLibrary()
library.open()
