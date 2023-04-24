# ����maya����ģ��
import maya.cmds as cmds

# ����һ�����������ڴ�������ʾ����
def create_window():
    # ��鴰���Ƿ��Ѿ����ڣ�����ǣ���ɾ����
    if cmds.window("my_window", exists=True):
        cmds.deleteUI("my_window", window=True)
    
    # ����һ�����ڣ����ñ���ʹ�С
    window = cmds.window("my_window", title="�ҵ�maya����", widthHeight=(600, 800))
    
    # ����һ����ֱ���֣����ڷ����������
    main_layout = cmds.columnLayout(adjustableColumn=True)
    
    # ������һ����飺����
    setting_layout = cmds.frameLayout(label="����", collapsable=True, parent=main_layout)
    # �����ð���ڴ���һ��ˮƽ���֣����ڷ�����ߵ����ú��ұߵ��û���¼
    setting_sub_layout = cmds.rowLayout(numberOfColumns=2, columnWidth2=(300, 300), adjustableColumn=1, parent=setting_layout)
    # ����ߵ������ڴ���һ����ֱ���֣����ڷ����������ܰ�ť
    setting_left_layout = cmds.columnLayout(adjustableColumn=True, parent=setting_sub_layout)
    # �����������ܰ�ť��������Ӧ�ĺ���
    add_tool_button = cmds.button(label="���maya�Դ�����", command=add_tool)
    add_script_button = cmds.button(label="��ӽű�����", command=add_script)
    topmost_button = cmds.checkBox(label="�����ö�", changeCommand=topmost)
    # ���ұߵ��û���¼�ڴ���һ����ֱ���֣����ڷ��õ�¼��ע�Ṧ��
    setting_right_layout = cmds.columnLayout(adjustableColumn=True, parent=setting_sub_layout)
    # ������¼��ע�Ṧ�ܣ�������Ӧ�ĺ���
    login_button = cmds.button(label="��¼", command=login)
    register_button = cmds.button(label="ע��", command=register)

    # �����ڶ�����飺����maya����
    tool_layout = cmds.frameLayout(label="����maya����", collapsable=True, parent=main_layout)
    # �ڳ���maya���߰���ڴ���һ����ֱ���֣����ڷ����û���ӵĹ��߰�ť
    tool_sub_layout = cmds.scrollLayout(parent=tool_layout)
    
    # ������������飺�ű����
    script_layout = cmds.frameLayout(label="�ű����", collapsable=True, parent=main_layout)
    # �ڽű��������ڴ���һ����ֱ���֣����ڷ����û���ӵĽű���ť
    script_sub_layout = cmds.scrollLayout(parent=script_layout)

    # ��ʾ����
    cmds.showWindow(window)

# ����һ���������������maya�Դ����ߵ�����maya���߰��
def add_tool(*args):
    # ����û��Ƿ��Ѿ���¼�����û�У�������ʾ��
    if not check_login():
        cmds.confirmDialog(title="��ʾ", message="���ȵ�¼����ӹ���")
        return
    
    # �����Ի������û�����Ҫ��ӵĹ������ƺ�ͼ��·������ѡ��
    result = cmds.promptDialog(title="��ӹ���",message="������Ҫ��ӵĹ������ƺ�ͼ��·������ѡ�����ö��ŷָ�",
    button=["ȷ��", "ȡ��"],
    defaultButton="ȷ��",
    cancelButton="ȡ��",
    dismissString="ȡ��")
    
    # ����û������ȷ����ť����ȡ�û���������ݣ����ָ�ɹ������ƺ�ͼ��·��
    if result == "ȷ��":
        text = cmds.promptDialog(query=True, text=True)
        if text:
            parts = text.split(",")
            tool_name = parts[0].strip()
            tool_icon = parts[1].strip() if len(parts) > 1 else None
            # �ڳ���maya���߰���ڴ���һ����ť�����ñ�ǩΪ�������ƣ�ͼ��Ϊ����ͼ�꣨����У�������Ϊִ�й���
            tool_button = cmds.iconTextButton(label=tool_name, image=tool_icon, command=tool_name, parent=tool_sub_layout)
            # ����ť����Ҽ��˵�����������ͼ���ɾ������
            tool_menu = cmds.popupMenu(parent=tool_button)
            cmds.menuItem(label="����ͼ��", command=lambda x: set_icon(tool_button))
            cmds.menuItem(label="ɾ������", command=lambda x: delete_tool(tool_button))
            # �Ѱ�ť����Ϣ���浽MySQL���ݿ��У��Ա��´δ򿪴���ʱ�ָ�
            save_to_mysql(tool_name, tool_icon, "tool")

# ����һ��������������ӽű����뵽�ű�������
def add_script(*args):
    # ����û��Ƿ��Ѿ���¼�����û�У�������ʾ��
    if not check_login():
        cmds.confirmDialog(title="��ʾ", message="���ȵ�¼����ӽű�")
        return
    
    # �����Ի������û�����Ҫ��ӵĽű����ƺʹ���
    result = cmds.promptDialog(title="��ӽű�",
    message="������Ҫ��ӵĽű����ƺʹ��룬�ö��ŷָ�",
    button=["ȷ��", "ȡ��"],
    defaultButton="ȷ��",
    cancelButton="ȡ��",
    dismissString="ȡ��")
    
    # ����û������ȷ����ť����ȡ�û���������ݣ����ָ�ɽű����ƺʹ���
    if result == "ȷ��":
        text = cmds.promptDialog(query=True, text=True)
        if text:
            parts = text.split(",")
            script_name = parts[0].strip()
            script_code = parts[1].strip()
            # �ڽű��������ڴ���һ����ť�����ñ�ǩΪ�ű����ƣ�����Ϊִ�нű�
            script_button = cmds.button(label=script_name, command=script_code, parent=script_sub_layout)
            # ����ť����Ҽ��˵�����������ͼ���ɾ���ű�
            script_menu = cmds.popupMenu(parent=script_button)
            cmds.menuItem(label="����ͼ��", command=lambda x: set_icon(script_button))
            cmds.menuItem(label="ɾ���ű�", command=lambda x: delete_script(script_button))
            # �Ѱ�ť����Ϣ���浽MySQL���ݿ��У��Ա��´δ򿪴���ʱ�ָ�
            save_to_mysql(script_name, script_code, "script")

# ����һ���������������ô����Ƿ��ö�
def topmost(value):
    # ��ȡ��ǰ���ڵľ��
    window = cmds.window("my_window", query=True)
    # ���ݸ�ѡ���ֵ�����ô����Ƿ��ö�
    if value:
        cmds.window(window, edit=True, topEdge=0, leftEdge=0)
        cmds.window(window, edit=True, retain=True)
    else:
        cmds.window(window, edit=True, retain=False)

# ����һ�����������ڵ�¼�û�
def login(*args):
    # �����Ի������û������û���������
    result = cmds.promptDialog(title="��¼",
    message="�������û��������룬�ö��ŷ� ��",
    button=["ȷ��", "ȡ��"],
    defaultButton="ȷ��",
    cancelButton="ȡ��",
    dismissString="ȡ��")
    
    # ����û������ȷ����ť����ȡ�û���������ݣ����ָ���û���������
    if result == "ȷ��":
        text = cmds.promptDialog(query=True, text=True)
        if text:
            parts = text.split(",")
            username = parts[0].strip()
            password = parts[1].strip()
            # ��MySQL���ݿ��в�ѯ�û���Ϣ����֤�û����������Ƿ���ȷ
            user_info = query_from_mysql(username, "user")
            if user_info and user_info["password"] == password:
                # �����ȷ��������ʾ����ʾ��¼�ɹ�
                cmds.confirmDialog(title="��ʾ", message="��¼�ɹ�")
                # ���û������浽ȫ�ֱ����У��Ա����ʹ��
                global current_user
                current_user = username
            else:
                # ������󣬵�����ʾ����ʾ��¼ʧ��
                cmds.confirmDialog(title="��ʾ", message="��¼ʧ��")

# ����һ������������ע���û�
def register(*args):
    # �����Ի������û������û���������
    result = cmds.promptDialog(title="ע��",
    message="�������û��������룬�ö��ŷָ�",
    button=["ȷ��", "ȡ��"],
    defaultButton="ȷ��",
    cancelButton="ȡ��",
    dismissString="ȡ��")
    
    # ����û������ȷ����ť����ȡ�û���������ݣ����ָ���û���������
    if result == "ȷ��":
        text = cmds.promptDialog(query=True, text=True)
        if text:
            parts = text.split(",")
            username = parts[0].strip()
            password = parts[1].strip()
            # ����û����Ƿ��Ѿ����ڣ�����ǣ�������ʾ����ʾע��ʧ��
            if query_from_mysql(username, "user"):
                cmds.confirmDialog(title="��ʾ", message="ע��ʧ�ܣ��û����Ѵ���")
                return
            # ���û��������뱣�浽MySQL���ݿ���
            save_to_mysql(username, password, "user")
            # ������ʾ����ʾע��ɹ�
            cmds.confirmDialog(title="��ʾ", message="ע��ɹ�")

# ����һ���������������ð�ť��ͼ��
def set_icon(button):
    # �����ļ��Ի������û�ѡ��ͼ���ļ���·��
    file_path = cmds.fileDialog2(fileMode=1, caption="ѡ��ͼ���ļ�")
    # ����û�ѡ�����ļ������ð�ť��ͼ��Ϊ�ļ�·��
    if file_path:
        cmds.iconTextButton(button, edit=True, image=file_path[0])
        # ����MySQL���ݿ��еİ�ť��Ϣ
        update_mysql(button)

# ����һ������������ɾ�����߰�ť
def delete_tool(button):
    # ����ȷ�϶Ի������û�ȷ���Ƿ�ɾ�����߰�ť
    result = cmds.confirmDialog(title="ɾ������",
    message="��ȷ��Ҫɾ�����������",
    button=["��", "��"],
    defaultButton="��",
    cancelButton="��",
    dismissString="��")
    
    # ����û�������ǰ�ť��ɾ�����߰�ť
    if result == "��":
        cmds.deleteUI(button)
        # ɾ��MySQL���ݿ��еİ�ť��Ϣ
        delete_from_mysql(button)

# ����һ������������ɾ���ű���ť
def delete_script(button):
    # ����ȷ�϶Ի������û�ȷ���Ƿ�ɾ���ű���ť
    result = cmds.confirmDialog(title="ɾ���ű�",
    message="��ȷ��Ҫɾ������ű���",
    button=["��", "��"],
    defaultButton="��",
    cancelButton="��",
    dismissString="��")
    
    # ����û�������ǰ�ť��ɾ���ű���ť
    if result == "��":
        cmds.deleteUI(button)
        # ɾ��MySQL���ݿ��еİ�ť��Ϣ
        delete_from_mysql(button)

# ����һ�����������ڼ���û��Ƿ��Ѿ���¼
def check_login():
    # ��ȡȫ�ֱ���
    global current_user
    # ���ȫ�ֱ���Ϊ�գ�˵���û�û�е�¼������False
    if not current_user:
        return False
    # ���򣬷���True
    else:
        return True

# ����һ�����������ڱ������ݵ�MySQL���ݿ�
def save_to_mysql(*args):
    # ����MySQL���ݿ⣬�����û��������룬���ݿ����Ȳ���
    connection = mysql.connector.connect(user="root", password="123456", database="maya_window")
    # ����һ���α��������ִ��SQL���
    cursor = connection.cursor()
    # ���ݲ�ͬ�����ͣ�ִ�в�ͬ��SQL��䣬�������ݵ���Ӧ�ı���
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
    # �ύ���񣬹ر�����
    connection.commit()
    connection.close()

# ����һ�����������ڴ�MySQL���ݿ��в�ѯ����
def query_from_mysql(*args):
    # ����MySQL���ݿ⣬�����û��������룬���ݿ����Ȳ���
    connection = mysql.connector.connect(user="root", password="123456", database="maya_window")
    # ����һ���α��������ִ��SQL���
    cursor = connection.cursor(dictionary=True)
    # ���ݲ�ͬ�����ͣ�ִ�в�ͬ��SQL��䣬��ѯ���ݴ���Ӧ�ı���
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
    # �ر����ӣ����ز�ѯ���
    connection.close()
    return result

# ����һ�����������ڸ���MySQL���ݿ��е�����
def update_mysql(button):
    # ����MySQL���ݿ⣬�����û��������룬���ݿ����Ȳ���
    connection = mysql.connector.connect(user="root", password="123456", database="maya_window")
    # ����һ���α��������ִ��SQL���
    cursor = connection.cursor()
    # ��ȡ��ť�ı�ǩ��ͼ��
    button_label = cmds.iconTextButton(button, query=True, label=True)
    button_icon = cmds.iconTextButton(button, query=True, image=True)
    # ���ݰ�ť�ı�ǩ���ж��ǹ��߰�ť���ǽű���ť����ִ����Ӧ��SQL��䣬�������ݵ���Ӧ�ı���
    if button_label in cmds.toolset(query=True):
        sql = "UPDATE tool SET tool_icon = %s WHERE tool_name = %s AND user_id = %s"
        values = (button_icon, button_label, get_user_id())
        cursor.execute(sql, values)
    else:
        sql = "UPDATE script SET script_icon = %s WHERE script_name = %s AND user_id = %svalues = (button_icon, button_label, get_user_id())
        cursor.execute(sql, values)
    # �ύ���񣬹ر�����
    connection.commit()
    connection.close()

# ����һ������������ɾ��MySQL���ݿ��е�����
def delete_from_mysql(button):
    # ����MySQL���ݿ⣬�����û��������룬���ݿ����Ȳ���
    connection = mysql.connector.connect(user="root", password="123456", database="maya_window")
    # ����һ���α��������ִ��SQL���
    cursor = connection.cursor()
    # ��ȡ��ť�ı�ǩ
    button_label = cmds.iconTextButton(button, query=True, label=True)
    # ���ݰ�ť�ı�ǩ���ж��ǹ��߰�ť���ǽű���ť����ִ����Ӧ��SQL��䣬ɾ�����ݴ���Ӧ�ı���
    if button_label in cmds.toolset(query=True):
        sql = "DELETE FROM tool WHERE tool_name = %s AND user_id = %s"
        values = (button_label, get_user_id())
        cursor.execute(sql, values)
    else:
        sql = "DELETE FROM script WHERE script_name = %s AND user_id = %s"
        values = (button_label, get_user_id())
        cursor.execute(sql, values)
    # �ύ���񣬹ر�����
    connection.commit()
    connection.close()

# ����һ�����������ڻ�ȡ��ǰ�û���id
def get_user_id():
    # ��ȡȫ�ֱ���
    global current_user
    # ��MySQL���ݿ��в�ѯ�û���Ϣ�������û�id
    user_info = query_from_mysql(current_user, "user")
    return user_info["id"]

# ���ô������ڵĺ���
create_window()
