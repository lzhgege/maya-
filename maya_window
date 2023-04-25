# 导入模块
import maya.cmds as cmds
import maya.mel as mel
import os
import shutil

# 定义全局变量
global windowName # 窗口名称
global windowWidth # 窗口宽度
global windowHeight # 窗口高度
global userName # 用户名
global userPassword # 用户密码
global userLoggedIn # 用户是否已登录
global toolList # 工具列表
global scriptList # 脚本列表
global pluginList # 插件列表

# 初始化变量
windowName = "myMayaWindow" # 可以自定义窗口名称
windowWidth = 600 # 可以自定义窗口宽度
windowHeight = 800 # 可以自定义窗口高度
userName = "" # 用户名为空
userPassword = "" # 用户密码为空
userLoggedIn = False # 用户未登录
toolList = [] # 工具列表为空
scriptList = [] # 脚本列表为空
pluginList = [] # 插件列表为空

# 定义函数

# 创建MySQL连接，需要安装MySQLdb模块，这里假设已经安装并配置好了MySQL数据库，数据库名为myMayaDB，用户名为root，密码为123456，表名为myMayaTable，字段有id, name, password, tool, script, plugin，可以根据实际情况修改
def createMySQLConnection():
    import MySQLdb
    global db # 数据库连接对象
    global cursor # 数据库游标对象
    db = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="myMayaDB") # 连接数据库
    cursor = db.cursor() # 创建游标

# 关闭MySQL连接
def closeMySQLConnection():
    global db # 数据库连接对象
    global cursor # 数据库游标对象
    cursor.close() # 关闭游标
    db.close() # 关闭数据库

# 检查用户是否存在，如果存在返回True，否则返回False，参数为用户名和密码，如果只传入用户名则只检查用户名是否存在，如果传入用户名和密码则检查用户名和密码是否匹配
def checkUserExist(name, password=None):
    global cursor # 数据库游标对象
    if password: # 如果传入了密码，则检查用户名和密码是否匹配
        sql = "SELECT * FROM myMayaTable WHERE name='%s' AND password='%s'" % (name, password) # SQL语句，根据用户名和密码查询数据表
    else: # 如果没有传入密码，则只检查用户名是否存在
        sql = "SELECT * FROM myMayaTable WHERE name='%s'" % name # SQL语句，根据用户名查询数据表
    cursor.execute(sql) # 执行SQL语句
    result = cursor.fetchone() # 获取查询结果，如果有匹配的记录则返回一个元组，否则返回None
    if result: # 如果有匹配的记录，则返回True
        return True
    else: # 如果没有匹配的记录，则返回False
        return False

# 注册用户，参数为用户名和密码，如果注册成功则返回True，否则返回False，并在窗口中显示提示信息，注册成功后会自动登录并更新用户数据到全局变量中
def registerUser(name, password):
    global cursor # 数据库游标对象
    global db # 数据库连接对象
    global userName # 用户名
    global userPassword # 用户密码
    global userLoggedIn # 用户是否已登录
    global toolList # 工具列表
    global scriptList # 脚本列表
    global pluginList # 插件列表
    if checkUserExist(name): # 如果用户名已存在，则注册失败，并显示提示信息
        cmds.confirmDialog(title="注册失败", message="用户名已存在，请换一个用户名", button="确定") # 弹出对话框
        return False # 返回False
    else: # 如果用户名不存在，则注册成功，并显示提示信息
        sql = "INSERT INTO myMayaTable (name, password) VALUES ('%s', '%s')" % (name, password) # SQL语句，向数据表中插入新的记录
        cursor.execute(sql) # 执行SQL语句
        db.commit() # 提交数据库操作
        cmds.confirmDialog(title="注册成功", message="恭喜你，注册成功！", button="确定") # 弹出对话框
        userName = name # 更新用户名到全局变量中
        userPassword = password # 更新用户密码到全局变量中
        userLoggedIn = True # 更新用户登录状态到全局变量中
        toolList = [] # 初始化工具列表为空
        scriptList = [] # 初始化脚本列表为空
        pluginList = [] # 初始化插件列表为空
        updateUI() # 更新界面显示
        return True # 返回True

# 登录用户，参数为用户名和密码，如果登录成功则返回True，否则返回False，并在窗口中显示提示信息，登录成功后会更新用户数据到全局变量中，并从数据库中读取用户的工具、脚本和插件数据
def loginUser(name, password):
    global cursor # 数据库游标对象
    global userName # 用户名
    global userPassword # 用户密码
    global userLoggedIn # 用户是否已登录
    global toolList # 工具列表
    global scriptList # 脚本列表
    global pluginList # 插件列表
    if checkUserExist(name, password): # 如果用户名和密码匹配，则登录成功，并显示提示信息
        cmds.confirmDialog(title="登录成功", message="欢迎你，%s！" % name, button="确定") # 弹出对话框
        userName = name # 更新用户名到全局变量中
        userPassword = password # 更新用户密码到全局变量中
        userLoggedIn = True # 更新用户登录状态到全局变量中
        sql = "SELECT tool, script, plugin FROM myMayaTable WHERE name='%s'" % name # SQL语句，根据用户名查询数据表中的工具、脚本和插件字段，这些字段存储的是字符串，用逗号分隔每个元素，例如"move,scale,rotate"
        cursor.execute(sql) # 执行SQL语句
        result = cursor.fetchone() # 获取查询结果，返回一个元组，例如("move,scale,rotate", "printHelloWorld.py", "myPlugin")
        if result: # 如果有查询结果，则解析字符串并更新到全局变量中的列表中，如果没有查询结果，则说明用户没有设置过工具、脚本和插件，则初始化为空列表
            toolList = result[0].split(",") if result[0] else [] # 解析工具字符串并更新到工具列表中，如果字符串为空则赋值为空列表
            scriptList = result[1].split(",") if result[1] else [] # 解析脚本字符串并更新到脚本列表中，如果字符串为空则赋值为空列表
            pluginList = result[2].split(",") if result[2] else [] # 解析插件字符串并更新到插件列表中，如果字符串为空则赋值为空列表
        else: 
            toolList = [] # 初始化工具列表为空
            scriptList = [] # 初始化脚本列表为空
            pluginList = [] # 初始化插件列表为空
        updateUI() # 更新界面显示
        return True # 返回True
    else: # 如果用户名和密码不匹配，则登录失败，并显示提示信息
        cmds.confirmDialog(title="登录失败", message="用户名或密码错误，请重新输入", button="确定") # 弹出对话框
        return False # 返回False

# 退出用户，无参数，会将用户数据从全局变量中清空，并更新界面显示
def logoutUser():
    global userName # 用户名
    global userPassword # 用户密码
    global userLoggedIn # 用户是否已登录
    global toolList # 工具列表
    global scriptList # 脚本列表
    global pluginList # 插件列表
    userName = "" # 清空用户名
    userPassword = "" # 清空用户密码
    userLoggedIn = False # 清空用户登录状态
    toolList = [] # 清空工具列表
    scriptList = [] # 清空脚本列表
    pluginList = [] # 清空插件列表
    updateUI() # 更新界面显示

# 添加maya自带工具，无参数，会弹出一个对话框让用户输入工具名称，如果输入的工具名称是maya自带的，则添加到工具列表中，并更新数据库和界面显示，否则提示用户输入错误，并让用户重新输入，添加前必须登录，否则提示用户登录
def addMayaTool():
    global cursor # 数据库游标对象
    global db # 数据库连接对象
    global userName # 用户名
    global userPassword # 用户密码
    global userLoggedIn # 用户是否已登录
    global toolList # 工具列表
    if userLoggedIn: # 如果用户已登录，则可以添加工具
        toolName = cmds.promptDialog(title="添加maya自带工具", message="请输入工具名称：", button=["确定", "取消"], defaultButton="确定", cancelButton="取消", dismissString="取消") # 弹出对话框让用户输入工具名称，返回用户点击的按钮或者关闭对话框的字符串
        if toolName == "确定": # 如果用户点击了确定按钮，则获取用户输入的文本，并检查是否是maya自带的工具名称，这里假设maya自带的工具名称都是小写字母，可以根据实际情况修改判断条件
            toolName = cmds.promptDialog(query=True, text=True) # 获取用户输入的文本
            if toolName.islower(): # 如果用户输入的文本都是小写字母，则认为是maya自带的工具名称，可以根据实际情况修改判断条件
                if toolName not in toolList: # 如果用户输入的工具名称不在工具列表中，则添加到工具列表中，并更新数据库和界面显示，否则提示用户该工具已存在，并让用户重新输入或取消
                    toolList.append(toolName) # 添加工具名称到工具列表中
                    sql = "UPDATE myMayaTable SET tool='%s' WHERE name='%s'" % (",".join(toolList), userName) # SQL语句，根据用户名更新数据表中的工具字段，用逗号分隔每个元素，例如"move,scale,rotate"
                    cursor.execute(sql) # 执行SQL语句
                    db.commit() # 提交数据库操作
                    updateUI() # 更新界面显示
                    cmds.confirmDialog(title="添加成功", message="你已成功添加了%s工具" % toolName, button="确定") # 弹出对话框提示用户添加成功
                else: # 如果用户输入的工具名称已在工具列表中，则提示用户该工具已存在，并让用户重新输入或取消
                    cmds.confirmDialog(title="添加失败", message="你已经添加了%s工具，请换一个工具名称" % toolName, button="确定") # 弹出对话框提示用户添加失败
                    addMayaTool() # 递归调用自身函数，让用户重新输入或取消
            else: # 如果用户输入的文本不都是小写字母，则认为不是maya自带的工具名称，可以根据实际情况修改判断条件
                cmds.confirmDialog(title="添加失败", message="你输入的不是maya自带的工具名称，请重新输入", button="确定") # 弹出对话框提示用户添加失败
                addMayaTool() # 递归调用自身函数，让用户重新输入或取消
        elif toolName == "取消": # 如果用户点击了取消按钮，则不做任何操作，直接返回
            return
        else: # 如果用户关闭了对话框，则不做任何操作，直接返回
            return
    else: # 如果用户未登录，则提示用户登录，并弹出登录对话框
        cmds.confirmDialog(title="提示", message="请先登录再添加工具", button="确定") # 弹出对话框提示用户登录
        loginWindow() # 调用登录窗口函数

# 添加脚本代码，无参数，会弹出一个对话框让用户输入脚本名称和脚本代码，如果输入的脚本名称和脚本代码都不为空，则添加到脚本列表中，并更新数据库和界面显示，否则提示用户输入错误，并让用户重新输入，添加前必须登录，否则提示用户登录
def addScriptCode():
    global cursor # 数据库游标对象
    global db # 数据库连接对象
    global userName # 用户名
    global userPassword # 用户密码
    global userLoggedIn # 用户是否已登录
    global scriptList # 脚本列表
    if userLoggedIn: # 如果用户已登录，则可以添加脚本代码
        scriptName = cmds.promptDialog(title="添加脚本代码", message="请输入脚本名称：", button=["确定", "取消"], defaultButton="确定", cancelButton="取消", dismissString="取消") # 弹出对话框让用户输入脚本名称，返回用户点击的按钮或者关闭对话框的字符串
        if scriptName == "确定": # 如果用户点击了确定按钮，则获取用户输入的文本，并检查是否为空，如果为空则提示用户输入错误，并让用户重新输入或取消，否则继续弹出另一个对话框让用户输入脚本代码
            scriptName = cmds.promptDialog(query=True, text=True) # 获取用户输入的文本
            if scriptName: # 如果用户输入的文本不为空，则继续弹出另一个对话框让用户输入脚本代码
                scriptCode = cmds.scrollFieldDialog(title="添加脚本代码", wordWrap=False, text="", button=["确定", "取消"], defaultButton="确定", cancelButton="取消", dismissString="取消") # 弹出对话框让用户输入脚本代码，返回用户点击的按钮或者关闭对话框的字符串，这里用scrollFieldDialog来显示一个可以滚动的文本框，方便用户输入长文本，也可以用其他方式来实现
                if script# Code was too long to be generated in one turn. Please wait for the next turn.
                if scriptCode == "确定": # 如果用户点击了确定按钮，则获取用户输入的文本，并检查是否为空，如果为空则提示用户输入错误，并让用户重新输入或取消，否则添加到脚本列表中，并更新数据库和界面显示
                    scriptCode = cmds.scrollFieldDialog(query=True, text=True) # 获取用户输入的文本
                    if scriptCode: # 如果用户输入的文本不为空，则添加到脚本列表中，并更新数据库和界面显示
                        if scriptName not in scriptList: # 如果用户输入的脚本名称不在脚本列表中，则添加到脚本列表中，并更新数据库和界面显示，否则提示用户该脚本已存在，并让用户重新输入或取消
                            scriptList.append(scriptName) # 添加脚本名称到脚本列表中
                            sql = "UPDATE myMayaTable SET script='%s' WHERE name='%s'" % (",".join(scriptList), userName) # SQL语句，根据用户名更新数据表中的脚本字段，用逗号分隔每个元素，例如"printHelloWorld.py,myScript.py"
                            cursor.execute(sql) # 执行SQL语句
                            db.commit() # 提交数据库操作
                            updateUI() # 更新界面显示
                            cmds.confirmDialog(title="添加成功", message="你已成功添加了%s脚本" % scriptName, button="确定") # 弹出对话框提示用户添加成功
                            # 保存脚本代码到一个文件中，文件名为脚本名称，文件路径为maya的scripts目录下的myMayaWindow文件夹，如果文件夹不存在则创建，如果文件已存在则覆盖，可以根据实际情况修改文件路径和文件名
                            scriptPath = os.path.join(mel.eval("getenv MAYA_SCRIPT_PATH"), "myMayaWindow") # 获取文件路径，使用mel命令获取maya的scripts目录，并拼接上myMayaWindow文件夹
                            if not os.path.exists(scriptPath): # 如果文件夹不存在，则创建
                                os.makedirs(scriptPath) # 创建文件夹
                            scriptFile = os.path.join(scriptPath, scriptName) # 获取文件名，拼接上文件路径和脚本名称
                            with open(scriptFile, "w") as f: # 打开文件，如果文件不存在则创建，如果文件已存在则覆盖
                                f.write(scriptCode) # 写入脚本代码到文件中
                                f.close() # 关闭文件
                        else: # 如果用户输入的脚本名称已在脚本列表中，则提示用户该脚本已存在，并让用户重新输入或取消
                            cmds.confirmDialog(title="添加失败", message="你已经添加了%s脚本，请换一个脚本名称" % scriptName, button="确定") # 弹出对话框提示用户添加失败
                            addScriptCode() # 递归调用自身函数，让用户重新输入或取消
                    else: # 如果用户输入的文本为空，则提示用户输入错误，并让用户重新输入或取消
                        cmds.confirmDialog(title="添加失败", message="你没有输入任何脚本代码，请重新输入", button="确定") # 弹出对话框提示用户添加失败
                        addScriptCode() # 递归调用自身函数，让用户重新输入或取消
                elif scriptCode == "取消": # 如果用户点击了取消按钮，则不做任何操作，直接返回
                    return
                else: # 如果用户关闭了对话框，则不做任何操作，直接返回
                    return
            else: # 如果用户输入的文本为空，则提示用户输入错误，并让用户重新输入或取消
                cmds.confirmDialog(title="添加失败", message="你没有输入任何脚本名称，请重新输入", button="确定") # 弹出对话框提示用户添加失败
                addScriptCode() # 递归调用自身函数，让用户重新输入或取消
        elif scriptName == "取消": # 如果用户点击了取消按钮，则不做任何操作，直接返回
            return
        else: # 如果用户关闭了对话框，则不做任何操作，直接返回
            return
    else: # 如果用户未登录，则提示用户登录，并弹出登录对话框
        cmds.confirmDialog(title="提示", message="请先登录再添加脚本代码", button="确定") # 弹出对话框提示用户登录
        loginWindow() # 调用登录窗口函数

# 添加插件，无参数，会弹出一个文件浏览器让用户选择插件文件夹，并复制到软件特定目录内，然后弹出一个对话框让用户输入安装插件代码，并识别安装到工具列表中，并更新数据库和界面显示，添加前必须登录，否则提示用户登录
def addPlugin():
    global cursor # 数据库游标对象
    global db # 数据库连接对象
    global userName # 用户名
    global userPassword # 用户密码
    global userLoggedIn # 用户是否已登录
    global toolList # 工具列表
    global pluginList # 插件列表
    if userLoggedIn: # 如果用户已登录，则可以添加插件
        pluginFolder = cmds.fileDialog2(fileMode=3, caption="选择插件文件夹") # 弹出文件浏览器让用户选择插件文件夹，返回一个列表，包含用户选择的文件夹路径，如果用户没有选择任何文件夹，则返回None
        if pluginFolder: # 如果用户选择了文件夹，则获取文件夹路径，并复制到软件特定目录内，这里假设软件特定目录为maya的plug-ins目录下的myMayaWindow文件夹，如果文件夹不存在则创建，如果文件已存在则覆盖，可以根据实际情况修改文件路径和文件名
            pluginFolder = pluginFolder[0] # 获取文件夹路径，由于返回的是一个列表，所以取第一个元素
            pluginPath = os.path.join(mel.eval("getenv MAYA_PLUG_IN_PATH"), "myMayaWindow") # 获取文件路径，使用mel命令获取maya的plug-ins目录，并拼接上myMayaWindow文件夹
            if not os.path.exists(pluginPath): # 如果文件夹不存在，则创建
                os.makedirs(pluginPath) # 创建文件夹
            shutil.copytree(pluginFolder, pluginPath) # 复制文件夹到目标路径，如果目标路径已存在则覆盖
            pluginName = os.path.basename(pluginFolder) # 获取插件名称，即文件夹的最后一级名称，例如myPlugin
            if pluginName not in pluginList: # 如果插件名称不在插件列表中，则添加到插件列表中，并更新数据库和界面显示，否则提示用户该插件已存在，并让用户重新输入或取消
                pluginList.append(pluginName) # 添加插件名称到插件列表中
                sql = "UPDATE myMayaTable SET plugin='%s' WHERE name='%s'" % (",".join(pluginList), userName) # SQL语句，根据用户名更新数据表中的插件字段，用逗号分隔每个元素，例如"myPlugin,anotherPlugin"
                cursor.execute(sql) # 执行SQL语句
                db.commit() # 提交数据库操作
                updateUI() # 更新界面显示
                cmds.confirmDialog(title="添加成功", message="你已成功添加了%s插件" % pluginName, button="确定") # 弹出对话框提示用户添加成功
                # 弹出一个对话框让用户输入安装插件代码，并识别安装到工具列表中，这里假设安装插件代码的格式为"loadPlugin myPlugin"，可以根据实际情况修改判断条件和执行方式
                pluginCode = cmds.promptDialog(title="添加插件代码", message="请输入安装插件代码：", button=["确定", "取消"], defaultButton="确定", cancelButton="取消", dismissString="取消") # 弹出对话框让用户输入安装插件代码，返回用户点击的按钮或者关闭对话框的字符串
                if pluginCode == "确定": # 如果用户点击了确定按钮，则获取用户输入的文本，并检查是否符合格式，如果符合则执行并添加到工具列表中，并更新数据库和界面显示，否则提示用户输入错误，并让用户重新输入或取消
                    pluginCode = cmds.promptDialog(query=True, text=True) # 获取用户输入的文本
                    if pluginCode.startswith("loadPlugin") and pluginName in pluginCode: # 如果用户输入的文本以"loadPlugin"开头，并且包含插件名称，则认为符合格式，可以根据实际情况修改判断条件
                        if pluginCode not in toolList: # 如果用户输入的安装插件代码不在工具列表中，则添加到工具列表中，并更新数据库和界面显示，否则提示用户该工具已存在，并让用户重新输入或取消
                            toolList.append(pluginCode) # 添加安装插件代码到工具列表中
                            sql = "UPDATE myMayaTable SET tool='%s' WHERE name='%s'" % (",".join(toolList), userName) # SQL语句，根据用户名更新数据表中的工具字段，用逗号分隔每个元素，例如"move,scale,rotate,loadPlugin myPlugin"
                            cursor.execute(sql) # 执行SQL语句
                            db.commit() # 提交数据库操作
                            updateUI() # 更新界面显示
                            cmds.confirmDialog(title="添加成功", message="你已成功添加了%s工具" % pluginCode, button="确定") # 弹出对话框提示用户添加成功
                            mel.eval(pluginCode) # 执行安装插件代码，使用mel命令执行，也可以用其他方式来实现
                        else: # 如果用户输入的安装插件代码已在工具列表中，则提示用户该工具已存在，并让用户重新输入或取消
                            cmds.confirmDialog(title="添加失败", message="你已经添加了%s工具，请换一个工具名称" % pluginCode, button="确定") # 弹出对话框提示用户添加失败
                            addPlugin() # 递归调用自身函数，让用户重新输入或取消
                    else: # 如果用户输入的文本不符合格式，则提示用户输入错误，并让用户重新输入或取消
                        cmds.confirmDialog(title="添加失败", message="你输入的不是正确的安装插件代码，请重新输入", button="确定") # 弹出对话框提示用户添加失败
                        addPlugin() # 递归调用自身函数，让用户重新输入或取消
                elif pluginCode == "取消": # 如果用户点击了取消按钮，则不做任何操作，直接返回
                    return
                else: # 如果用户关闭了对话框，则不做任何操作，直接返回
                    return
            else: # 如果插件名称已在插件列表中，则提示用户该插件已存在，并让用户重新输入或取消
                cmds.confirmDialog(title="添加失败", message="你已经添加了%s插件，请换一个插件名称" % pluginName, button="确定") # 弹出对话框提示用户添加失败
                addPlugin() # 递归调用自身函数，让用户重新输入或取消
        else: # 如果用户没有选择任何文件夹，则不做任何操作，直接返回
            return
    else: # 如果用户未登录，则提示用户登录，并弹出登录对话框
        cmds.confirmDialog(title="提示", message="请先登录再添加插件", button="确定") # 弹出对话框提示用户登录
        loginWindow() # 调用登录窗口函数

# 窗口置顶，参数为复选框的值，如果为True，则将窗口置顶，如果为False，则取消窗口置顶
def windowTop(value):
    global windowName # 窗口名称
    if value: # 如果复选框的值为True，则将窗口置顶
        cmds.window(windowName, edit=True, topEdge=0) # 将窗口的上边缘设置为0，即屏幕的最上方
        cmds.window(windowName, edit=True, retain=True) # 将窗口的保持属性设置为True，即保持窗口的位置和大小不变
    else: # 如果复选框的值为False，则取消窗口置顶
        cmds.window(windowName, edit=True, retain=False) # 将窗口的保持属性设置为False，即允许窗口的位置和大小改变

# 更新界面显示，无参数，会根据全局变量中的用户数据和列表数据来更新界面中的控件的显示内容和状态
def updateUI():
    global windowName # 窗口名称
    global userName # 用户名
    global userPassword # 用户密码
    global userLoggedIn # 用户是否已登录
    global toolList # 工具列表
    global scriptList # 脚本列表
    global pluginList # 插件列表
    if userLoggedIn: # 如果用户已登录，则更新界面中的控件显示用户的信息和列表的内容，并启用相关的控件，否则清空界面中的控件显示内容，并禁用相关的控件
        cmds.text("userNameText", edit=True, label="用户名：%s" % userName) # 更新用户名文本控件显示用户名
        cmds.button("logoutButton", edit=True, enable=True) # 启用退出按钮控件
        cmds.button("addMayaToolButton", edit=True, enable=True) # 启用添加maya自带工具按钮控件
        cmds.button("addScriptCodeButton", edit=True, enable=True) # 启用添加脚本代码按钮控件
        cmds.button("addPluginButton", edit=True, enable=True) # 启用添加插件按钮控件
        cmds.textScrollList("toolList", edit=True, removeAll=True) # 清空工具列表文本滚动列表控件中的所有元素
        cmds.textScrollList("toolList", edit=True, append=toolList) # 添加工具列表中的所有元素到工具列表文本滚动列表控件中
        cmds.textScrollList("scriptList", edit=True, removeAll=True) # 清空脚本列表文本滚动列表控件中的所有元素
        cmds.textScrollList("scriptList", edit=True, append=scriptList) # 添加脚本列表中的所有元素到脚本列表文本滚动列表控件中
        cmds.textScrollList("pluginList", edit=True, removeAll=True) # 清空插件列表文本滚动列表控件中的所有元素
        cmds.textScrollList("pluginList", edit=True, append=pluginList) # 添加插件列表中的所有元素到插件列表文本滚动列表控件中
    else: # 如果用户未登录，则清空界面中的控件显示内容，并禁用相关的控件
        cmds.text("userNameText", edit=True, label="用户名：") # 清空用户名文本控件显示内容
        cmds.button("logoutButton", edit=True, enable=False) # 禁用退出按钮控件
        cmds.button("addMayaToolButton", edit=True, enable=False) # 禁用添加maya自带工具按钮控件
        cmds.button("addScriptCodeButton", edit=True, enable=False) # 禁用添加脚本代码按钮控件
        cmds.button("addPluginButton", edit=True, enable=False) # 禁用添加插件按钮控件
        cmds.textScrollList("toolList", edit=True, removeAll=True) # 清空工具列表文本滚动列表控件中的所有元素
        cmds.textScrollList("scriptList", edit=True, removeAll=True) # 清空脚本列表文本滚动列表控件中的所有元素
        cmds.textScrollList("pluginList", edit=True, removeAll=True) # 清空插件列表文本滚动列表控件中的所有元素

# 注册窗口，无参数，会弹出一个对话框让用户输入用户名和密码，如果输入的用户名和密码都不为空，则调用注册用户函数，否则提示用户输入错误，并让用户重新输入或取消
def registerWindow():
    registerName = cmds.promptDialog(title="注册", message="请输入用户名：", button=["确定", "取消"], defaultButton="确定", cancelButton="取消", dismissString="取消") # 弹出对话框让用户输入用户名，返回用户点击的按钮或者关闭对话框的字符串
    if registerName == "确定": # 如果用户点击了确定按钮，则获取用户输入的文本，并检查是否为空，如果为空则提示用户输入错误，并让用户重新输入或取消，否则继续弹出另一个对话框让用户输入密码
        registerName = cmds.promptDialog(query=True, text=True) # 获取用户输入的文本
        if registerName: # 如果用户输入的文本不为空，则继续弹出另一个对话框让用户输入密码
            registerPassword = cmds.promptDialog(title="注册", message="请输入密码：", button=["确定", "取消"], defaultButton="确定", cancelButton="取消", dismissString="取消") # 弹出对话框让用户输入密码，返回用户点击的按钮或者关闭对话框的字符串
            if registerPassword == "确定": # 如果用户点击了确定按钮，则获取用户输入的文本，并检查是否为空，如果为空则提示用户输入错误，并让用户重新输入或取消，否则调用注册用户函数
                registerPassword = cmds.promptDialog(query=True, text=True) # 获取用户输入的文本
                if registerPassword: # 如果用户输入的文本不为空，则调用注册用户函数
                    registerUser(registerName, registerPassword) # 调用注册用户函数，传入用户名和密码作为参数
                else: # 如果用户输入的文本为空，则提示用户输入错误，并让用户重新输入或取消
                    cmds.confirmDialog(title="注册失败", message="你没有输入任何密码，请重新输入", button="确定") # 弹出对话框提示用户注册失败
                    registerWindow() # 递归调用自身函数，让用户重新输入或取消
            elif registerPassword == "取消": # 如果用户点击了取消按钮，则不做任何操作，直接返回
                return
            else: # 如果用户关闭了对话框，则不做任何操作，直接返回
                return
        else: # 如果用户输入的文本为空，则提示用户输入错误，并让用户重新输入或取消
            cmds.confirmDialog(title="注册失败", message="你没有输入任何用户名，请重新输入", button="确定") # 弹出对话框提示用户注册失败
            registerWindow() # 递归调用自身函数，让用户重新输入或取消
    elif registerName == "取消": # 如果用户点击了取消按钮，则不做任何操作，直接返回
        return
    else: # 如果用户关闭了对话框，则不做任何操作，直接返回
        return

# 登录窗口，无参数，会弹出一个对话框让用户输入用户名和密码，如果输入的用户名和密码都不为空，则调用登录用户函数，否则提示用户输入错误，并让用户重新输入或取消
def loginWindow():
    loginName = cmds.promptDialog(title="登录", message="请输入用户名：", button=["确定", "取消"], defaultButton="确定", cancelButton="取消", dismissString="取消") # 弹出对话框让用户输入用户名，返回用户点击的按钮或者关闭对话框的字符串
    if loginName == "确定": # 如果用户点击了确定按钮，则获取用户输入的文本，并检查是否为空，如果为空则提示用户输入错误，并让用户重新输入或取消，否则继续弹出另一个对话框让用户输入密码
        loginName = cmds.promptDialog(query=True, text=True) # 获取用户输入的文本
        if loginName: # 如果用户输入的文本不为空，则继续弹出另一个对话框让用户输入密码
            loginPassword = cmds.promptDialog(title="登录", message="请输入密码：", button=["确定", "取消"], defaultButton="确定", cancelButton="取消", dismissString="取消") # 弹出对话框让用户输入密码，返回用户点击的按钮或者关闭对话框的字符串
            if loginPassword == "确定": # 如果用户点击了确定按钮，则获取用户输入的文本，并检查是否为空，如果为空则提示用户输入错误，并让用户重新输入或取消，否则调用登录用户函数
                loginPassword = cmds.promptDialog(query=True, text=True) # 获取用户输入的文本
                if loginPassword: # 如果用户输入的文本不为空，则调用登录用户函数
                    loginUser(loginName, loginPassword) # 调用登录用户函数，传入用户名和密码作为参数
                else: # 如果用户输入的文本为空，则提示用户输入错误，并让用户重新输入或取消
                    cmds.confirmDialog(title="登录失败", message="你没有输入任何密码，请重新输入", button="确定") # 弹出对话框提示用户登录失败
                    loginWindow() # 递归调用自身函数，让用户重新输入或取消
            elif loginPassword == "取消": # 如果用户点击了取消按钮，则不做任何操作，直接返回
                return
            else: # 如果用户关闭了对话框，则不做任何操作，直接返回
                return
        else: # 如果用户输入的文本为空，则提示用户输入错误，并让用户重新输入或取消
            cmds.confirmDialog(title="登录失败", message="你没有输入任何用户名，请重新输入", button="确定") # 弹出对话框提示用户登录失败
            loginWindow() # 递归调用自身函数，让用户重新输入或取消
    elif loginName == "取消": # 如果用户点击了取消按钮，则不做任何操作，直接返回
        return
    else: # 如果用户关闭了对话框，则不做任何操作，直接返回
        return

# 创建窗口，无参数，会创建一个maya窗口，窗口大致分三个板块纵向排列，第一板块为设置，第二板块为常见maya工具，第三板块为脚本插件，在第一板块：设置内分为左边为设置，右边为用户登录，在第二板块：常见maya工具内显示工具列表中的所有元素，在第三板块：脚本插件内显示脚本列表和插件列表中的所有元素，并添加相关的控件和事件处理函数
def createWindow():
    global windowName # 窗口名称
    global windowWidth # 窗口宽度
    global windowHeight # 窗口高度
    if cmds.window(windowName, exists=True): # 如果窗口已存在，则删除窗口，避免重复创建
        cmds.deleteUI(windowName) # 删除窗口
    cmds.window(windowName, title="我的maya窗口", widthHeight=(windowWidth, windowHeight), sizeable=False) # 创建窗口，设置标题、宽度、高度和不可改变大小属性
    cmds.columnLayout("mainLayout", adjustableColumn=True) # 创建主列布局，设置可调整列宽属性
    cmds.frameLayout("settingLayout", label="设置", collapsable=True, collapse=False, parent="mainLayout") # 创建设置框架布局，设置标签、可折叠、默认展开和父布局属性
    cmds.rowLayout("settingRowLayout", numberOfColumns=2, columnWidth2=(windowWidth/2, windowWidth/2), columnAlign2=("left", "right"), parent="settingLayout") # 创建设置行布局，设置列数、列宽、列对齐和父布局属性
    cmds.columnLayout("settingColumnLayout", adjustableColumn=True, parent="settingRowLayout") # 创建设置列布局，设置可调整列宽和父布局属性
    cmds.button("addMayaToolButton", label="添加maya自带工具", command=lambda x: addMayaTool(), enable=False, parent="settingColumnLayout") # 创建添加maya自带工具按钮控件，设置标签、命令、禁用和父布局属性，命令为调用添加maya自带工具函数
    cmds.button("addScriptCodeButton", label="添加脚本代码", command=lambda x: addScriptCode(), enable=False, parent="settingColumnLayout") # 创建添加脚本代码按钮控件，设置标签、命令、禁用和父布局属性，命令为调用添加脚本代码函数
    cmds.button("addPluginButton", label="添加插件", command=lambda x: addPlugin(), enable=False, parent="settingColumnLayout") # 创建添加插件按钮控件，设置标签、命令、禁用和父布局属性，命令为调用添加插件函数
    cmds.checkBox("windowTopCheckBox", label="窗口置顶", changeCommand=lambda x: windowTop(x), value=False, parent="settingColumnLayout") # 创建窗口置顶复选框控件，设置标签、改变命令、默认值和父布局属性，改变命令为调用窗口置顶函数
    cmds.columnLayout("userColumnLayout", adjustableColumn=True, parent="settingRowLayout") # 创建用户列布局，设置可调整列宽和父布局属性
    cmds.text("userNameText", label="用户名：", parent="userColumnLayout") # 创建用户名文本控件，设置标签和父布局属性
    cmds.button("loginButton", label="登录", command=lambda x: loginWindow(), parent="userColumnLayout") # 创建登录按钮控件，设置标签、命令和父布局属性，命令为调用登录窗口函数
    cmds.button("registerButton", label="注册", command=lambda x: registerWindow(), parent="userColumnLayout") # 创建注册按钮控件，设置标签、命令和父布局属性，命令为调用注册窗口函数
    cmds.button("logoutButton", label="退出", command=lambda x: logoutUser(), enable=False, parent="userColumnLayout") # 创建退出按钮控件，设置标签、命令、禁用和父布局属性，命令为调用退出用户函数
    cmds.frameLayout("toolLayout", label="常见maya工具", collapsable=True, collapse=False, parent="mainLayout") # 创建常见maya工具框架布局，设置标签、可折叠、默认展开和父布局属性
    cmds.textScrollList("toolList", allowMultiSelection=False, deleteKeyCommand=lambda x: deleteTool(), doubleClickCommand=lambda x: executeTool(), dragCallback=lambda x: dragTool(), dropCallback=lambda x: dropTool(), parent="toolLayout") # 创建工具列表文本滚动列表控件，设置不允许多选、删除键命令、双击命令、拖动回调、放下回调和父布局属性，删除键命令为调用删除工具函数，双击命令为调用执行工具函数，拖动回调为调用拖动工具函数，放下回调为调用放下工具函数
    cmds.frameLayout("scriptLayout", label="脚本插件", collapsable=True, collapse=False, parent="mainLayout") # 创建脚本插件框架布局，设置标签、可折叠、默认展开和父布局属性
    cmds.rowLayout("scriptRowLayout", numberOfColumns=2, columnWidth2=(windowWidth/2, windowWidth/2), columnAlign2=("left", "right"), parent="scriptLayout") # 创建脚本插件行布局，设置列数、列宽、列对齐和父布局属性
    cmds.textScrollList("scriptList", allowMultiSelection=False, deleteKeyCommand=lambda x: deleteScript(), doubleClickCommand=lambda x: executeScript(), dragCallback=lambda x: dragScript(), dropCallback=lambda x: dropScript(), parent="scriptRowLayout") # 创建脚本列表文本滚动列表控件，设置不允许多选、删除键命令、双击命令、拖动回调、放下回调和父布局属性，删除键命令为调用删除脚本函数，双击命令为调用执行脚本函数，拖动回调为调用拖动脚本函数，放下回调为调用放下脚本函数
    cmds.textScrollList("pluginList", allowMultiSelection=False, deleteKeyCommand=lambda x: deletePlugin(), doubleClickCommand=lambda x: executePlugin(), dragCallback=lambda x: dragPlugin(), dropCallback=lambda x: dropPlugin(), parent="scriptRowLayout") # 创建插件列表文本滚动列表控件，设置不允许多选、删除键命令、双击命令、拖动回调、放下回调和父布局属性，删除键命令为调用删除插件函数，双击命令为调用执行插件函数，拖动回调为调用拖动插件函数，放下回调为调用放下插件函数
    cmds.showWindow(windowName) # 显示窗口
    updateUI() # 更新界面显示

# 删除工具，无参数，会从工具列表中删除用户选择的元素，并更新数据库和界面显示
def deleteTool():
    global cursor # 数据库游标对象
    global db # 数据库连接对象
    global userName # 用户名
    global userPassword # 用户密码
    global userLoggedIn # 用户是否已登录
    global toolList # 工具列表
    if userLoggedIn: # 如果用户已登录，则可以删除工具
        toolName = cmds.textScrollList("toolList", query=True, selectItem=True) # 获取用户选择的元素，返回一个列表，包含用户选择的元素名称，如果用户没有选择任何元素，则返回None
        if toolName: # 如果用户选择了元素，则获取元素名称，并从工具列表中删除，并更新数据库和界面显示
            toolName = toolName[0] # 获取元素名称，由于返回的是一个列表，所以取第一个元素
            toolList.remove(toolName) # 从工具列表中删除元素名称
            sql = "UPDATE myMayaTable SET tool='%s' WHERE name='%s'" % (",".join(toolList), userName) # SQL语句，根据用户名更新数据表中的工具字段，用逗号分隔每个元素，例如"move,scale,rotate"
            cursor.execute(sql) # 执行SQL语句
            db.commit() # 提交数据库操作
            updateUI() # 更新界面显示
            cmds.confirmDialog(title="删除成功", message="你已成功删除了%s工具" % toolName, button="确定") # 弹出对话框提示用户删除成功
        else: # 如果用户没有选择任何元素，则不做任何操作，直接返回
            return
    else: # 如果用户未登录，则提示用户登录，并弹出登录对话框
        cmds.confirmDialog(title="提示", message="请先登录再删除工具", button="确定") # 弹出对话框提示用户登录
        loginWindow() # 调用登录窗口函数

# 删除脚本，无参数，会从脚本列表中删除用户选择的元素，并更新数据库和界面显示，并删除对应的文件
def deleteScript():
    global cursor # 数据库游标对象
    global db # 数据库连接对象
    global userName # 用户名
    global userPassword # 用户密码
    global userLoggedIn # 用户是否已登录
    global scriptList # 脚本列表
    if userLoggedIn: # 如果用户已登录，则可以删除脚本
        scriptName = cmds.textScrollList("scriptList", query=True, selectItem=True) # 获取用户选择的元素，返回一个列表，包含用户选择的元素名称，如果用户没有选择任何元素，则返回None
        if scriptName: # 如果用户选择了元素，则获取元素名称，并从脚本列表中删除，并更新数据库和界面显示，并删除对应的文件
            scriptName = scriptName[0] # 获取元素名称，由于返回的是一个列表，所以取第一个元素
            scriptList.remove(scriptName) # 从脚本列表中删除元素名称
            sql = "UPDATE myMayaTable SET script='%s' WHERE name='%s'" % (",".join(scriptList), userName) # SQL语句，根据用户名更新数据表中的脚本字段，用逗号分隔每个元素，例如"printHelloWorld.py,myScript.py"
            cursor.execute(sql) # 执行SQL语句
            db.commit() # 提交数据库操作
            updateUI() # 更新界面显示
            cmds.confirmDialog(title="删除成功", message="你已成功删除了%s脚本" % scriptName, button="确定") # 弹出对话框提示用户删除成功
            # 删除对应的文件，文件名为脚本名称，文件路径为maya的scripts目录下的myMayaWindow文件夹，可以根据实际情况修改文件路径和文件名
            scriptPath = os.path.join(mel.eval("getenv MAYA_SCRIPT_PATH"), "myMayaWindow") # 获取文件路径，使用mel命令获取maya的scripts目录，并拼接上myMayaWindow文件夹
            scriptFile = os.path.join(scriptPath, scriptName) # 获取文件名，拼接上文件路径和脚本名称
            if os.path.exists(scriptFile): # 如果文件存在，则删除文件
                os.remove(scriptFile) # 删除文件
        else: # 如果用户没有选择任何元素，则不做任何操作，直接返回
            return
    else: # 如果用户未登录，则提示用户登录，并弹出登录对话框
        cmds.confirmDialog(title="提示", message="请先登录再删除脚本", button="确定") # 弹出对话框提示用户登录
        loginWindow() # 调用登录窗口函数

# 删除插件，无参数，会从插件列表中删除用户选择的元素，并更新数据库和界面显示，并删除对应的文件夹和卸载插件
def deletePlugin():
    global cursor # 数据库游标对象
    global db # 数据库连接对象
    global userName # 用户名
    global userPassword # 用户密码
    global userLoggedIn # 用户是否已登录
    global pluginList # 插件列表
    if userLoggedIn: # 如果用户已登录，则可以删除插件
        pluginName = cmds.textScrollList("pluginList", query=True, selectItem=True) # 获取用户选择的元素，返回一个列表，包含用户选择的元素名称，如果用户没有选择任何元素，则返回None
        if pluginName: # 如果用户选择了元素，则获取元素名称，并从插件列表中删除，并更新数据库和界面显示，并删除对应的文件夹和卸载插件
            pluginName = pluginName[0] # 获取元素名称，由于返回的是一个列表，所以取第一个元素
            pluginList.remove(pluginName) # 从插件列表中删除元素名称
            sql = "UPDATE myMayaTable SET plugin='%s' WHERE name='%s'" % (",".join(pluginList), userName) # SQL语句，根据用户名更新数据表中的插件字段，用逗号分隔每个元素，例如"myPlugin,anotherPlugin"
            cursor.execute(sql) # 执行SQL语句
            db.commit() # 提交数据库操作
            updateUI() # 更新界面显示
            cmds.confirmDialog(title="删除成功", message="你已成功删除了%s插件" % pluginName, button="确定") # 弹出对话框提示用户删除成功
            # 删除对应的文件夹，文件夹名为插件名称，文件夹路径为maya的plug-ins目录下的myMayaWindow文件夹，可以根据实际情况修改文件路径和文件名
            pluginPath = os.path.join(mel.eval("getenv MAYA_PLUG_IN_PATH"), "myMayaWindow") # 获取文件路径，使用mel命令获取maya的plug-ins目录，并拼接上myMayaWindow文件夹
            pluginFolder = os.path.join(pluginPath, pluginName) # 获取文件夹名，拼接上文件路径和插件名称
            if os.path.exists(pluginFolder): # 如果文件夹存在，则删除文件夹
                shutil.rmtree(pluginFolder) # 删除文件夹
            # 卸载插件，这里假设卸载插件代码的格式为"unloadPlugin myPlugin"，可以根据实际情况修改判断条件和执行方式
            unloadCode = "unloadPlugin %s" % pluginName # 获取卸载插件代码，拼接上unloadPlugin和插件名称，例如"unloadPlugin myPlugin"
            if unloadCode in toolList: # 如果卸载插件代码在工具列表中，则从工具列表中删除，并更新数据库和界面显示，并执行卸载插件代码
                toolList.remove(unloadCode) # 从工具列表中删除卸载插件代码
                sql = "UPDATE myMayaTable SET tool='%s' WHERE name='%s'" % (",".join(toolList), userName) # SQL语句，根据用户名更新数据表中的工具字段，用逗号分隔每个元素，例如"move,scale,rotate"
                cursor.execute(sql) # 执行SQL语句
                db.commit() # 提交数据库操作
                updateUI() # 更新界面显示
                mel.eval(unloadCode) # 执行卸载插件代码，使用mel命令执行，也可以用其他方式来实现
        else: # 如果用户没有选择任何元素，则不做任何操作，直接返回
            return
    else: # 如果用户未登录，则提示用户登录，并弹出登录对话框
        cmds.confirmDialog(title="提示", message="请先登录再删除插件", button="确定") # 弹出对话框提示用户登录
        loginWindow() # 调用登录窗口函数

# 执行工具，无参数，会执行用户选择的工具列表中的元素，如果是maya自带工具，则调用maya的命令，如果是安装插件代码，则调用mel命令，可以根据实际情况修改判断条件和执行方式
def executeTool():
    toolName = cmds.textScrollList("toolList", query=True, selectItem=True) # 获取用户选择的元素，返回一个列表，包含用户选择的元素名称，如果用户没有选择任何元素，则返回None
    if toolName: # 如果用户选择了元素，则获取元素名称，并执行对应的命令
        toolName = toolName[0] # 获取元素名称，由于返回的是一个列表，所以取第一个元素
        if toolName in ["move", "scale", "rotate"]: # 如果元素名称是maya自带工具之一，则调用maya的命令，可以根据实际情况修改判断条件和执行方式
            cmds.setToolTo(toolName) # 调用maya的命令，设置当前工具为元素名称对应的工具，例如"move"
        elif toolName.startswith("loadPlugin"): # 如果元素名称是安装插件代码，则调用mel命令，可以根据实际情况修改判断条件和执行方式
            mel.eval(toolName) # 调用mel命令，执行安装插件代码，例如"loadPlugin myPlugin"
        else: # 如果元素名称不属于以上任何一种情况，则不做任何操作，直接返回
            return

# 执行脚本，无参数，会执行用户选择的脚本列表中的元素，并打开对应的文件
def executeScript():
    scriptName = cmds.textScrollList("scriptList", query=True, selectItem=True) # 获取用户选择的元素，返回一个列表，包含用户选择的元素名称，如果用户没有选择任何元素，则返回None
    if scriptName: # 如果用户选择了元素，则获取元素名称，并打开对应的文件
        scriptName = scriptName[0] # 获取元素名称，由于返回的是一个列表，所以取第一个元素
        # 打开对应的文件，文件名为脚本名称，文件路径为maya的scripts目录下的myMayaWindow文件夹，可以根据实际情况修改文件路径和文件名
        scriptPath = os.path.join(mel.eval("getenv MAYA_SCRIPT_PATH"), "myMayaWindow") # 获取文件路径，使用mel命令获取maya的scripts目录，并拼接上myMayaWindow文件夹
        scriptFile = os.path.join(scriptPath, scriptName) # 获取文件名，拼接上文件路径和脚本名称
        if os.path.exists(scriptFile): # 如果文件存在，则打开文件
            cmds.file(scriptFile, open=True) # 调用maya的命令，打开文件

# 执行插件，无参数，会执行用户选择的插件列表中的元素，并打开对应的文件夹
def executePlugin():
    pluginName = cmds.textScrollList("pluginList", query=True, selectItem=True) # 获取用户选择的元素，返回一个列表，包含用户选择的元素名称，如果用户没有选择任何元素，则返回None
    if pluginName: # 如果用户选择了元素，则获取元素名称，并打开对应的文件夹
        pluginName = pluginName[0] # 获取元素名称，由于返回的是一个列表，所以取第一个元素
        # 打开对应的文件夹，文件夹名为插件名称，文件夹路径为maya的plug-ins目录下的myMayaWindow文件夹，可以根据实际情况修改文件路径和文件名
        pluginPath = os.path.join(mel.eval("getenv MAYA_PLUG_IN_PATH"), "myMayaWindow") # 获取文件路径，使用mel命令获取maya的plug-ins目录，并拼接上myMayaWindow文件夹
        pluginFolder = os.path.join(pluginPath, pluginName) # 获取文件夹名，拼接上文件路径和插件名称
        if os.path.exists(pluginFolder): # 如果文件夹存在，则打开文件夹
            os.startfile(pluginFolder) # 调用系统命令，打开文件夹

# 拖动工具，无参数，会获取用户拖动的工具列表中的元素，并设置为当前拖动数据
def dragTool():
    toolName = cmds.textScrollList("toolList", query=True, selectItem=True) # 获取用户拖动的元素，返回一个列表，包含用户拖动的元素名称，如果用户没有拖动任何元素，则返回None
    if toolName: # 如果用户拖动了元素，则获取元素名称，并设置为当前拖动数据
        toolName = toolName[0] # 获取元素名称，由于返回的是一个列表，所以取第一个元素
        cmds.draggerContext("toolDragger", cursor="hand", dragCommand=lambda x: dropTool(), data=toolName) # 创建一个拖动器上下文控件，设置光标、拖动命令、数据属性，拖动命令为调用放下工具函数

# 放下工具，无参数，会获取当前放下位置和当前拖动数据，并根据位置判断是否放到脚本列表或插件列表中，并更新数据库和界面显示
def dropTool():
    global cursor # 数据库游标对象
    global db # 数据库连接对象
    global userName # 用户名
    global userPassword # 用户密码
    global userLoggedIn # 用户是否已登录
    global toolList # 工具列表
    global scriptList # 脚本列表
    global pluginList # 插件列表
    if userLoggedIn: # 如果用户已登录，则可以放下工具
        dropPosition = cmds.draggerContext("toolDragger", query=True, anchorPoint=True) # 获取当前放下位置，返回一个列表，包含放下位置的x和y坐标，例如[100, 200]
        dropData = cmds.draggerContext("toolDragger", query=True, data=True) # 获取当前拖动数据，返回一个字符串，包含拖动数据的内容，例如"move"
        if dropPosition and dropData: # 如果当前放下位置和当前拖动数据都不为空，则根据位置判断是否放到脚本列表或插件列表中，并更新数据库和界面显示
            dropX = dropPosition[0] # 获取放下位置的x坐标，由于返回的是一个列表，所以取第一个元素
            dropY = dropPosition[1] # 获取放下位置的y坐标，由于返回的是一个列表，所以取第二个元素
            scriptX = cmds.textScrollList("scriptList", query=True, x=True) # 获取脚本列表文本滚动列表控件的x坐标，返回一个整数，例如200
            scriptY = cmds.textScrollList("scriptList", query=True, y=True) # 获取脚本列表文本滚动列表控件的y坐标，返回一个整数，例如300
            scriptWidth = cmds.textScrollList("scriptList", query=True, width=True) # 获取脚本列表文本滚动列表控件的宽度，返回一个整数，例如100
            scriptHeight = cmds.textScrollList("scriptList", query=True, height=True) # 获取脚本列表文本滚动列表控件的高度，返回一个整数，例如200
            pluginX = cmds.textScrollList("pluginList", query=True, x=True) # 获取插件列表文本滚动列表控件的x坐标，返回一个整数，例如400
            pluginY = cmds.textScrollList("pluginList", query=True, y=True) # 获取插件列表文本滚动列表控件的y坐标，返回一个整数，例如500
            pluginWidth = cmds.textScrollList("pluginList", query=True, width=True) # 获取插件列表文本滚动列表控件的宽度，返回一个整数，例如100
            pluginHeight = cmds.textScrollList("pluginList", query=True, height=True) # 获取插件列表文本滚动列表控件的高度，返回一个整数，例如200
            if scriptX <= dropX <= scriptX + scriptWidth and scriptY <= dropY <= scriptY + scriptHeight: # 如果放下位置在脚本列表文本滚动列表控件的范围内，则将拖动数据添加到脚本列表中，并更新数据库和界面显示
                if dropData not in scriptList: # 如果拖动数据不在脚本列表中，则添加到脚本列表中，并更新数据库和界面显示，否则提示用户该脚本已存在，并让用户重新输入或取消
                    scriptList.append(dropData) # 添加拖动数据到脚本列表中
                    sql = "UPDATE myMayaTable SET script='%s' WHERE name='%s'" % (",".join(scriptList), userName) # SQL语句，根据用户名更新数据表中的脚本字段，用逗号分隔每个元素，例如"printHelloWorld.py,myScript.py"
                    cursor.execute(sql) # 执行SQL语句
                    db.commit() # 提交数据库操作
                    updateUI() # 更新界面显示
                    cmds.confirmDialog(title="添加成功", message="你已成功添加了%s脚本" % dropData, button="确定") # 弹出对话框提示用户添加成功
                else: # 如果拖动数据已在脚本列表中，则提示用户该脚本已存在，并让用户重新输入或取消
                    cmds.confirmDialog(title="添加失败", message="你已经添加了%s脚本，请换一个脚本名称" % dropData, button="确定") # 弹出对话框提示用户添加失败
            elif pluginX <= dropX <= pluginX + pluginWidth and pluginY <= dropY <= pluginY + pluginHeight: # 如果放下位置在插件列表文本滚动列表控件的范围内，则将拖动数据添加到插件列表中，并更新数据库和界面显示
                if dropData not in pluginList: # 如果拖动数据不在插件列表中，则添加到插件列表中，并更新数据库和界面显示，否则提示用户该插件已存在，并让用户重新输入或取消
                    pluginList.append(dropData) # 添加拖动数据到插件列表中
                    sql = "UPDATE myMayaTable SET plugin='%s' WHERE name='%s'" % (",".join(pluginList), userName) # SQL语句，根据用户名更新数据表中的插件字段，用逗号分隔每个元素，例如"myPlugin,anotherPlugin"
                    cursor.execute(sql) # 执行SQL语句
                    db.commit() # 提交数据库操作
                    updateUI() # 更新界面显示
                    cmds.confirmDialog(title="添加成功", message="你已成功添加了%s插件" % dropData, button="确定") # 弹出对话框提示用户添加成功
                else: # 如果拖动数据已在插件列表中，则提示用户该插件已存在，并让用户重新输入或取消
                    cmds.confirmDialog(title="添加失败", message="你已经添加了%s插件，请换一个插件名称" % dropData, button="确定") # 弹出对话框提示用户添加失败
            else: # 如果放下位置不在脚本列表或插件列表文本滚动列表控件的范围内，则不做任何操作，直接返回
                return

# 拖动脚本，无参数，会获取用户拖动的脚本列表中的元素，并设置为当前拖动数据
def dragScript():
    scriptName = cmds.textScrollList("scriptList", query=True, selectItem=True) # 获取用户拖动的元素，返回一个列表，包含用户拖动的元素名称，如果用户没有拖动任何元素，则返回None
    if scriptName: # 如果用户拖动了元素，则获取元素名称，并设置为当前拖动数据
        scriptName = scriptName[0] # 获取元素名称，由于返回的是一个列表，所以取第一个元素
        cmds.draggerContext("scriptDragger", cursor="hand", dragCommand=lambda x: dropScript(), data=scriptName) # 创建一个拖动器上下文控件，设置光标、拖动命令、数据属性，拖动命令为调用放下脚本函数

# 放下脚本，无参数，会获取当前放下位置和当前拖动数据，并根据位置判断是否放到工具列表或插件列表中，并更新数据库和界面显示
def dropScript():
    global cursor # 数据库游标对象
    global db # 数据库连接对象
    global userName # 用户名
    global userPassword # 用户密码
    global userLoggedIn # 用户是否已登录
    global toolList # 工具列表
    global scriptList # 脚本列表
    global pluginList # 插件列表
    if userLoggedIn: # 如果用户已登录，则可以放下脚本
        dropPosition = cmds.draggerContext("scriptDragger", query=True, anchorPoint=True) # 获取当前放下位置，返回一个列表，包含放下位置的x和y坐标，例如[100, 200]
        dropData = cmds.draggerContext("scriptDragger", query=True, data=True) # 获取当前拖动数据，返回一个字符串，包含拖动数据的内容，例如"printHelloWorld.py"
        if dropPosition and dropData: # 如果当前放下位置和当前拖动数据都不为空，则根据位置判断是否放到工具列表或插件列表中，并更新数据库和界面显示
            dropX = dropPosition[0] # 获取放下位置的x坐标，由于返回的是一个列表，所以取第一个元素
            dropY = dropPosition[1] # 获取放下位置的y坐标，由于返回的是一个列表，所以取第二个元素
            toolX = cmds.textScrollList("toolList", query=True, x=True) # 获取工具列表文本滚动列表控件的x坐标，返回一个整数，例如100
            toolY = cmds.textScrollList("toolList", query=True, y=True) # 获取工具列表文本滚动列表控件的y坐标，返回一个整数，例如200
            toolWidth = cmds.textScrollList("toolList", query=True, width=True) # 获取工具列表文本滚动列表控件的宽度，返回一个整数，例如100
            toolHeight = cmds.textScrollList("toolList", query=True, height=True) # 获取工具列表文本滚动列表控件的高度，返回一个整数，例如200
            pluginX = cmds.textScrollList("pluginList", query=True, x=True) # 获取插件列表文本滚动列表控件的x坐标，返回一个整数，例如400
            pluginY = cmds.textScrollList("pluginList", query=True, y=True) # 获取插件列表文本滚动列表控件的y坐标，返回一个整数，例如500
            pluginWidth = cmds.textScrollList("pluginList", query=True, width=True) # 获取插件列表文本滚动列表控件的宽度，返回一个整数，例如100
            pluginHeight = cmds.textScrollList("pluginList", query=True, height=True) # 获取插件列表文本滚动列表控件的高度，返回一个整数，例如200
            if toolX <= dropX <= toolX + toolWidth and toolY <= dropY <= toolY + toolHeight: # 如果放下位置在工具列表文本滚动列表控件的范围内，则将拖动数据添加到工具列表中，并更新数据库和界面显示
                if dropData not in toolList: #
