# encoding : uft-8
import windnd
import os
import sys
import zipfile
import shutil
import zipfile
import tkinter.filedialog
import tkinter.messagebox
from platform import version
from tkinter import *
from tkinter import ttk


def Build_Drfx(ft,csort):
    # ft : file_type "Effects","Generators","Titles","Transitions"
    # csort : custom sort
    temp_file_path = ".\\Edit\\"+ft+"\\"+csort
    output_filename = os.path.split(filepath[0])[-1].split(".")[0]+".drfx"
    spath = os.path.dirname(filepath[0])
    os.makedirs(temp_file_path)
    for i in filepath:
        shutil.copy(i,temp_file_path)
    with zipfile.ZipFile(output_filename, "w") as f:
        for i in os.walk(".\\Edit"):
            for n in i[2]:
                f.write("".join((i[0], "\\", n)))
    try:
        shutil.move(output_filename,spath)
    except:
        pass

    Del_dir("Edit")
    return output_filename
    

def Unpack_Drfx():
    # dfp : drfx file path
    for i in filepath:
        temp_path = os.path.dirname(i)+"\\"+i.split("\\")[-1].split(".")[0]
        with zipfile.ZipFile(i,"r") as f:
            f.extractall(temp_path)
    return temp_path

def Del_dir(dir_name):
    if os.path.exists(dir_name):
        try:
            shutil.rmtree(dir_name)
        except:
            pass

def select_files():
    # select setting files
    global filepath
    temp_list = []
    filepath = tkinter.filedialog.askopenfiles(
        filetypes=[("setting文件", "*.setting *.png"),("drfx文件","*.drfx")], title="请选择文件")
    for i in filepath:
        temp_list.append(i.name)
    filepath = temp_list
    cfile()
    show_path.set(filepath)
    
def drag_files(files):
    global filepath
    temp_list = []
    for i in files:
        path = i.decode("gbk")
        if path.split(".")[-1] not in ["setting","png","drfx"]:
            temp_list = []
            tkinter.messagebox.showerror("错误",str(path)+"不被支持")
            break
        else:
            temp_list.append(path)
            filepath = temp_list
            cfile()
            show_path.set(filepath) 

def ccsort(csort):
    # check custom sort
    forbid_text = [":","*","\"","<",">","|","？"]
    for i in forbid_text:
        if i in csort:
            return True
    return False

def cfile():
    # check files
    temp = []
    if filepath != []:
        for i in filepath:
            if i.split(".")[-1] == "drfx":
                temp.append(True)
            else:
                temp.append(False)
        #if all of temp is True(all files is drfx) return unzip
        if all(temp):
            b_run["text"] = "解包"
            return True
        else:
            b_run["text"] = "打包"
            return False

def run():
    filename = ""
    Del_dir("Edit")
    if filepath is None or len(filepath) == 0:
        tkinter.messagebox.showerror("错误","未选择文件")
    elif ccsort(e_get_customdir.get()):
        tkinter.messagebox.showerror("错误","自定义目录不能使用: * \" < > | ？等字符")
    else:
        if cfile():
            filename = Unpack_Drfx()
            tkinter.messagebox.showinfo("提示", "已解包到"+str(filename))
        else:
            filename = Build_Drfx(c_choose_fusiontype.get(),e_get_customdir.get())
            Del_dir("Edit")
            tkinter.messagebox.showinfo("提示", "已生成"+str(filename))

################################################################################

def get_help():
    text = """    原理:建立Edit/filetype/custom/file.setting并压缩为zip，后缀名改为drfx
    * filetype为Effects Generators Titles Transitions
    * Effects特效 Generators生成器 Titles标题 Transitions转场
    * file.setting为Fusion中导出的setting文件
    * 如需要图标，将png图片改为和setting文件同名并放在相同目录
    * custom可被达芬奇识别为自定义分类目录

    *************************************************************

    打包使用说明:
    * 1.选择或拖动setting文件到本软件中
    * 2.选择相对应的Fusion文件类型
    * 3.输入自定义目录，如purplefire/work (此步骤可选，不建议使用中文名)
    * 4.点击"打包/解包"，会在setting同目录下生成同名的drfx文件
    * 5.打开达芬奇Fusion页面，拖动drfx文件安装即可

    *************************************************************

    解包使用说明:
    * 1.选择或拖动drfx文件到本软件中
    * 2.点击"打包/解包",会在drfx同目录生成Edit文件夹
    """
    tkinter.messagebox.showinfo("帮助", text)

def thanks():
    text = """感谢Vicco及其他达芬奇大佬贡献的思路和方法
    """
    tkinter.messagebox.showinfo("致谢", text)

def info():
    text = """    当前版本号:{0}
    本软件由紫火开发，遵守GPLv3开源协议
    本软件使用Python3开发
    本软件使用TKinter Windnd等第三方包
    本软件开源地址:https://github.com/magician333/drfx_zip-unzip
    使用本软件有任何问题请联系magician33333@163.com
    """.format(version)
    tkinter.messagebox.showinfo("关于", text)

def close():
    sys.exit()

################################################################################

if __name__ == "__main__":
    tk = Tk()
    filepath = None
    version = "V20220106.03"
    show_path = StringVar()
    tk.title("Drfx打包/解包工具 ")
    tk.iconbitmap("icon.ico")
    tk.geometry("280x140")

    menu = Menu(tk)
    tk["menu"] = menu
    menubar1 = Menu(menu)
    menubar1.add_command(label="退出",command=close)
    menu.add_cascade(label="文件",menu=menubar1)
    menu.add_cascade(label="帮助",command=get_help)
    menu.add_cascade(label="致谢",command=thanks)
    menu.add_cascade(label="关于",command=info)

    #l for Label e for Entry b for Button c for Combobox p for PhotoImage
    l_filepath = Label(tk, text="文件位置")
    e_filepath = Entry(tk,state="readonly",textvariable=show_path)
    p_buttonimage = PhotoImage(file="file-72-16.png")
    b_selectfile = Button(tk,command=select_files,image=p_buttonimage)
    windnd.hook_dropfiles(tk, func=drag_files)
    l_fusiontype = Label(tk, text="文件类型")
    c_choose_fusiontype = ttk.Combobox(tk, values=(
        "Effects", "Generators", "Titles", "Transitions"),state="readonly")
    c_choose_fusiontype.current(0)
    l_customdir = Label(tk,text="自定义目录")
    e_get_customdir = Entry(tk)
    b_run = Button(tk, text="打包/解包", command=run)

    l_filepath.grid(row=0,column=0,padx=5,pady=3,sticky="nw")
    e_filepath.grid(row=0,column=1,columnspan=10,padx=5,pady=3,sticky="nw")
    b_selectfile.grid(row=0,column=2,padx=5,pady=3)
    l_fusiontype.grid(row=1,column=0,padx=5,pady=3,sticky="nw")
    c_choose_fusiontype.grid(row=1,column=1,padx=5,pady=3,sticky="nw")
    l_customdir.grid(row=2,column=0,padx=5,pady=3,sticky="nw")
    e_get_customdir.grid(row=2,column=1,padx=5,pady=3,sticky="nw")
    b_run.grid(row=3,columnspan=3,sticky="n")
    tk.mainloop()