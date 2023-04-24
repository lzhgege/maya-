# 导入maya命令模块
import maya.cmds as cmds

# 定义一个函数，用于创建和显示窗口
def create_window():
    # 检查窗口是否已经存在，如果是，就删除它
    if cmds.window("my_window", exists=True):
        cmds.deleteUI("my_window", window=True)
    
    # 创建一个窗口，设置标题和大小
    window = cmds.window("my_window", title="我的maya窗口", widthHeight=(600, 800))
    
    # 创建一个垂直布局，用于放置三个板块
    main_layout = cmds.columnLayout(adjustableColumn=True)
    
    # 创建第一个板块：设置
    setting_layout = cmds.frameLayout(label="设置", collapsable=True, parent=main_layout)
    # 在设置板块内创建一个水平布局，用于放置左边的设置和右边的用户登录
    setting_sub_layout = cmds.rowLayout(numberOfColumns=2, columnWidth2=(300, 300), adjustableColumn=1, parent=setting_layout)
    # 在左边的设置内创建一个垂直布局，用于放置三个功能按钮
    setting_left_layout = cmds.columnLayout(adjustableColumn=True, parent=setting_sub_layout)
    # 创建三个功能按钮，并绑定相应的函数
    add_tool_button = cmds.button(label="添加maya自带工具", command=add_tool)
    add_script_button = cmds.button(label="添加脚本代码", command=add_script)
    topmost_button = cmds.checkBox(label="窗口置顶", changeCommand=topmost)
    # 在右边的用户登录内创建一个垂直布局，用于放置登录和注册功能
    setting_right_layout = cmds.columnLayout(adjustableColumn=True, parent=setting_sub_layout)
    # 创建登录和注册功能，并绑定相应的函数
    login_button = cmds.button(label="登录", command=login)
    register_button = cmds.button(label="注册", command=register)

    # 创建第二个板块：常见maya工具
    tool_layout = cmds.frameLayout(label="常见maya工具", collapsable=True, parent=main_layout)
    # 在常见maya工具板块内创建一个垂直布局，用于放置用户添加的工具按钮
    tool_sub_layout = cmds.scrollLayout(parent=tool_layout)
    
    # 创建第三个板块：脚本插件
    script_layout = cmds.frameLayout(label="脚本插件", collapsable=True, parent=main_layout)
    # 在脚本插件板块内创建一个垂直布局，用于放置用户添加的脚本按钮
    script_sub_layout = cmds.scrollLayout(parent=script_layout)

    # 显示窗口
    cmds.showWindow(window)

# 定义一个函数，用于添加maya自带工具到常见maya工具板块
def add_tool(*args):
    # 检查用户是否已经登录，如果没有，弹出提示框
    if not check_login():
        cmds.confirmDialog(title="提示", message="请先登录再添加工具")
        return
    
    # 弹出对话框，让用户输入要添加的工具名称和图标路径（可选）
    result = cmds.promptDialog(title="添加工具",message="请输入要添加的工具名称和图标路径（可选），用逗号分隔",
    button=["确定", "取消"],
    defaultButton="确定",
    cancelButton="取消",
    dismissString="取消")
    
    # 如果用户点击了确定按钮，获取用户输入的内容，并分割成工具名称和图标路径
    if result == "确定":
        text = cmds.promptDialog(query=True, text=True)
        if text:
            parts = text.split(",")
            tool_name = parts[0].strip()
            tool_icon = parts[1].strip() if len(parts) > 1 else None
            # 在常见maya工具板块内创建一个按钮，设置标签为工具名称，图标为工具图标（如果有），命令为执行工具
            tool_button = cmds.iconTextButton(label=tool_name, image=tool_icon, command=tool_name, parent=tool_sub_layout)
            # 给按钮添加右键菜单，用于设置图标或删除工具
            tool_menu = cmds.popupMenu(parent=tool_button)
            cmds.menuItem(label="设置图标", command=lambda x: set_icon(tool_button))
            cmds.menuItem(label="删除工具", command=lambda x: delete_tool(tool_button))
            # 把按钮的信息保存到MySQL数据库中，以便下次打开窗口时恢复
            save_to_mysql(tool_name, tool_icon, "tool")

# 定义一个函数，用于添加脚本代码到脚本插件板块
def add_script(*args):
    # 检查用户是否已经登录，如果没有，弹出提示框
    if not check_login():
        cmds.confirmDialog(title="提示", message="请先登录再添加脚本")
        return
    
    # 弹出对话框，让用户输入要添加的脚本名称和代码
    result = cmds.promptDialog(title="添加脚本",
    message="请输入要添加的脚本名称和代码，用逗号分隔",
    button=["确定", "取消"],
    defaultButton="确定",
    cancelButton="取消",
    dismissString="取消")
    
    # 如果用户点击了确定按钮，获取用户输入的内容，并分割成脚本名称和代码
    if result == "确定":
        text = cmds.promptDialog(query=True, text=True)
        if text:
            parts = text.split(",")
            script_name = parts[0].strip()
            script_code = parts[1].strip()
            # 在脚本插件板块内创建一个按钮，设置标签为脚本名称，命令为执行脚本
            script_button = cmds.button(label=script_name, command=script_code, parent=script_sub_layout)
            # 给按钮添加右键菜单，用于设置图标或删除脚本
            script_menu = cmds.popupMenu(parent=script_button)
            cmds.menuItem(label="设置图标", command=lambda x: set_icon(script_button))
            cmds.menuItem(label="删除脚本", command=lambda x: delete_script(script_button))
            # 把按钮的信息保存到MySQL数据库中，以便下次打开窗口时恢复
            save_to_mysql(script_name, script_code, "script")

# 定义一个函数，用于设置窗口是否置顶
def topmost(value):
    # 获取当前窗口的句柄
    window = cmds.window("my_window", query=True)
    # 根据复选框的值，设置窗口是否置顶
    if value:
        cmds.window(window, edit=True, topEdge=0, leftEdge=0)
        cmds.window(window, edit=True, retain=True)
    else:
        cmds.window(window, edit=True, retain=False)

# 定义一个函数，用于登录用户
def login(*args):
    # 弹出对话框，让用户输入用户名和密码
    result = cmds.promptDialog(title="登录",
    message="请输入用户名和密码，用逗号分 隔",
    button=["确定", "取消"],
    defaultButton="确定",
    cancelButton="取消",
    dismissString="取消")
    
    # 如果用户点击了确定按钮，获取用户输入的内容，并分割成用户名和密码
    if result == "确定":
        text = cmds.promptDialog(query=True, text=True)
        if text:
            parts = text.split(",")
            username = parts[0].strip()
            password = parts[1].strip()
            # 从MySQL数据库中查询用户信息，验证用户名和密码是否正确
            user_info = query_from_mysql(username, "user")
            if user_info and user_info["password"] == password:
                # 如果正确，弹出提示框，显示登录成功
                cmds.confirmDialog(title="提示", message="登录成功")
                # 把用户名保存到全局变量中，以便后续使用
                global current_user
                current_user = username
            else:
                # 如果错误，弹出提示框，显示登录失败
                cmds.confirmDialog(title="提示", message="登录失败")

# 定义一个函数，用于注册用户
def register(*args):
    # 弹出对话框，让用户输入用户名和密码
    result = cmds.promptDialog(title="注册",
    message="请输入用户名和密码，用逗号分隔",
    button=["确定", "取消"],
    defaultButton="确定",
    cancelButton="取消",
    dismissString="取消")
    
    # 如果用户点击了确定按钮，获取用户输入的内容，并分割成用户名和密码
    if result == "确定":
        text = cmds.promptDialog(query=True, text=True)
        if text:
            parts = text.split(",")
            username = parts[0].strip()
            password = parts[1].strip()
            # 检查用户名是否已经存在，如果是，弹出提示框，显示注册失败
            if query_from_mysql(username, "user"):
                cmds.confirmDialog(title="提示", message="注册失败，用户名已存在")
                return
            # 把用户名和密码保存到MySQL数据库中
            save_to_mysql(username, password, "user")
            # 弹出提示框，显示注册成功
            cmds.confirmDialog(title="提示", message="注册成功")

# 定义一个函数，用于设置按钮的图标
def set_icon(button):
    # 弹出文件对话框，让用户选择图标文件的路径
    file_path = cmds.fileDialog2(fileMode=1, caption="选择图标文件")
    # 如果用户选择了文件，设置按钮的图标为文件路径
    if file_path:
        cmds.iconTextButton(button, edit=True, image=file_path[0])
        # 更新MySQL数据库中的按钮信息
        update_mysql(button)

# 定义一个函数，用于删除工具按钮
def delete_tool(button):
    # 弹出确认对话框，让用户确认是否删除工具按钮
    result = cmds.confirmDialog(title="删除工具",
    message="你确定要删除这个工具吗？",
    button=["是", "否"],
    defaultButton="是",
    cancelButton="否",
    dismissString="否")
    
    # 如果用户点击了是按钮，删除工具按钮
    if result == "是":
        cmds.deleteUI(button)
        # 删除MySQL数据库中的按钮信息
        delete_from_mysql(button)

# 定义一个函数，用于删除脚本按钮
def delete_script(button):
    # 弹出确认对话框，让用户确认是否删除脚本按钮
    result = cmds.confirmDialog(title="删除脚本",
    message="你确定要删除这个脚本吗？",
    button=["是", "否"],
    defaultButton="是",
    cancelButton="否",
    dismissString="否")
    
    # 如果用户点击了是按钮，删除脚本按钮
    if result == "是":
        cmds.deleteUI(button)
        # 删除MySQL数据库中的按钮信息
        delete_from_mysql(button)

# 定义一个函数，用于检查用户是否已经登录
def check_login():
    # 获取全局变量
    global current_user
    # 如果全局变量为空，说明用户没有登录，返回False
    if not current_user:
        return False
    # 否则，返回True
    else:
        return True

# 定义一个函数，用于保存数据到MySQL数据库
def save_to_mysql(*args):
    # 连接MySQL数据库，设置用户名，密码，数据库名等参数
    connection = mysql.connector.connect(user="root", password="123456", database="maya_window")
    # 创建一个游标对象，用于执行SQL语句
    cursor = connection.cursor()
    # 根据不同的类型，执行不同的SQL语句，插入数据到相应的表中
    if args[-1] == "user":
        username = args[0]
        password = args[1]
        sql = "INSERT INTO user (username, password) VALUES (%s, %s)"
        values = (username, password)
        cursor.execute(sql, values)
    elif args[-1] == "tool":
        tool_name = args[0]
        tool_icon = args[1]
        sql = "INSERT INTO tool (tool_name, tool_icon, user_id) VALUES (%s, %s, %s)"
        values = (tool_name, tool_icon, get_user_id())
        cursor.execute(sql, values)
    elif args[-1] == "script":
        script_name = args[0]
        script_code = args[1]
        sql = "INSERT INTO script (script_name, script_code, user_id) VALUES (%s, %s, %s)"
        values = (script_name, script_code, get_user_id())
        cursor.execute(sql, values)
    # 提交事务，关闭连接
    connection.commit()
    connection.close()

# 定义一个函数，用于从MySQL数据库中查询数据
def query_from_mysql(*args):
    # 连接MySQL数据库，设置用户名，密码，数据库名等参数
    connection = mysql.connector.connect(user="root", password="123456", database="maya_window")
    # 创建一个游标对象，用于执行SQL语句
    cursor = connection.cursor(dictionary=True)
    # 根据不同的类型，执行不同的SQL语句，查询数据从相应的表中
    if args[-1] == "user":
        username = args[0]
        sql = "SELECT * FROM user WHERE username = %s"
        values = (username,)
        cursor.execute(sql, values)
        result = cursor.fetchone()
    elif args[-1] == "tool":
        user_id = args[0]
        sql = "SELECT * FROM tool WHERE user_id = %s"
        values = (user_id,)
        cursor.execute(sql, values)
        result = cursor.fetchall()
    elif args[-1] == "script":
        user_id = args[0]
        sql = "SELECT * FROM script WHERE user_id = %s"
        values = (user_id,)
        cursor.execute(sql, values)
        result = cursor.fetchall()
    # 关闭连接，返回查询结果
    connection.close()
    return result

# 定义一个函数，用于更新MySQL数据库中的数据
def update_mysql(button):
    # 连接MySQL数据库，设置用户名，密码，数据库名等参数
    connection = mysql.connector.connect(user="root", password="123456", database="maya_window")
    # 创建一个游标对象，用于执行SQL语句
    cursor = connection.cursor()
    # 获取按钮的标签和图标
    button_label = cmds.iconTextButton(button, query=True, label=True)
    button_icon = cmds.iconTextButton(button, query=True, image=True)
    # 根据按钮的标签，判断是工具按钮还是脚本按钮，并执行相应的SQL语句，更新数据到相应的表中
    if button_label in cmds.toolset(query=True):
        sql = "UPDATE tool SET tool_icon = %s WHERE tool_name = %s AND user_id = %s"
        values = (button_icon, button_label, get_user_id())
        cursor.execute(sql, values)
    else:
        sql = "UPDATE script SET script_icon = %s WHERE script_name = %s AND user_id = %svalues = (button_icon, button_label, get_user_id())
        cursor.execute(sql, values)
    # 提交事务，关闭连接
    connection.commit()
    connection.close()

# 定义一个函数，用于删除MySQL数据库中的数据
def delete_from_mysql(button):
    # 连接MySQL数据库，设置用户名，密码，数据库名等参数
    connection = mysql.connector.connect(user="root", password="123456", database="maya_window")
    # 创建一个游标对象，用于执行SQL语句
    cursor = connection.cursor()
    # 获取按钮的标签
    button_label = cmds.iconTextButton(button, query=True, label=True)
    # 根据按钮的标签，判断是工具按钮还是脚本按钮，并执行相应的SQL语句，删除数据从相应的表中
    if button_label in cmds.toolset(query=True):
        sql = "DELETE FROM tool WHERE tool_name = %s AND user_id = %s"
        values = (button_label, get_user_id())
        cursor.execute(sql, values)
    else:
        sql = "DELETE FROM script WHERE script_name = %s AND user_id = %s"
        values = (button_label, get_user_id())
        cursor.execute(sql, values)
    # 提交事务，关闭连接
    connection.commit()
    connection.close()

# 定义一个函数，用于获取当前用户的id
def get_user_id():
    # 获取全局变量
    global current_user
    # 从MySQL数据库中查询用户信息，返回用户id
    user_info = query_from_mysql(current_user, "user")
    return user_info["id"]

# 调用创建窗口的函数
create_window()
