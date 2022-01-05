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


tk = Tk()
filepath = None
version = "V20220105.004"
show_path = StringVar()

def Build_Drfx(ft,csort):
    # sfp : setting file path
    # ft : file_type "Effects","Generators","Titles","Transitions"
    temp_file_path = ".\\Edit\\"+ft+"\\"+csort
    output_filename = (filepath[0].split("\\")[-1]).split(".")[0]+".drfx"
    spath = os.path.dirname(filepath[0])
    os.makedirs(temp_file_path)
    for i in filepath:
        shutil.copy(i,temp_file_path)

    with zipfile.ZipFile(output_filename, "w") as f:
        for i in os.walk(".\\Edit"):
            for n in i[2]:
                f.write("".join((i[0], "\\", n)))
    shutil.move(output_filename,spath)
    return output_filename

def Unpack_Drfx(drp):
    # dfp : drfx file path
    temp_path = os.path.dirname(drp)+"\\"+drp.split("\\")[-1].split(".")[0]
    with zipfile.ZipFile(drp,"r") as f:
        f.extractall(temp_path)
    return temp_path

def Del_dir(dir_name):
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)

def select_files():
    # select setting files
    global filepath
    temp_list = []
    filepath = tkinter.filedialog.askopenfiles(
        filetypes=[("setting文件", "*.setting *.png"),("drfx文件","*.drfx")], title="请选择setting文件或drfx文件")
    for i in filepath:
        temp_list.append(i.name)
    filepath = temp_list
    show_path.set(filepath)
    
def drag_files(files):
    global filepath
    temp_list = []
    for i in files:
        temp_list.append(i.decode("gbk"))
    filepath = temp_list
    show_path.set(filepath) 

def run():
    Del_dir("Edit")
    for i in filepath:
        if i.split(".")[-1] == "drfx":
            filename = Unpack_Drfx(i)
            tkinter.messagebox.showinfo("提示", "已解包到"+filename)
        else:
            if i is None:
                tkinter.messagebox.showerror("错误", "请选择setting文件")
            elif c_choose_fusiontype.get() == "":
                tkinter.messagebox.showerror("错误", "请选择文件类型")
            else:
                filename = Build_Drfx(c_choose_fusiontype.get(),e_get_customdir.get())
                Del_dir("Edit")
                tkinter.messagebox.showinfo("提示", "已生成"+filename)       

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
