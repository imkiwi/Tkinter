# encoding: utf-8
import sys
sys.path.append("./module")
import Tkinter as tk
import ttk as ttk
import tkMessageBox

from PIL import ImageTk, Image
from functools import partial
#from LogManager import *
import RegisterParser
#import SPIModule

treeview = None
RegisterRuleList = []

# {'description': u'Release date \u5f35', 
# 'defaultValue': "32'h20181106", 
# 'name': 'spi_slave_date', 
# 'access': 'RW', 
# 'address': '0x20000000', 
# 'size': 32}
def treeViewClick(event):
    global treeview
    global RegisterRuleList
    for item in treeview.selection():
        item_text = treeview.item(item, "values")
        #print(item_text[0])#输出所选行的第一列的值
        tkMessageBox.showinfo(title='Register Table', message=item_text[0])
        break
 

def updateTreeView(items):
    global treeview
    global RegisterRuleList
    count = 0
    if(treeview != None):
        #SPIModule.setUp({})
        for i in treeview.get_children():
            treeview.delete(i)

        for item in items:
            #values = SPIModule.readSingle32(int(item["address"],16), False)
            #value = byteArrayToInt(values[5:])
            value = 0x00
            treeview.insert("", count ,values=(item["name"],item["access"],item["address"],item["defaultValue"], hex(value)))
            count += 1
        treeview.bind('<Double-Button-1>', treeViewClick)
        #SPIModule.close()


def createWindow():
    global treeview
    global RegisterRuleList
    
    window = tk.Tk()
    window.title('Register Table')
    window.geometry('1000x600+200+200')
    window.bind('<Escape>', lambda e: window.quit())

    # 區別top/bottom 
    frame_top = tk.Frame(window)
    frame_bottom = tk.Frame(window)

    frame_top.pack()
    frame_bottom.pack()

    # 區別bottom的左右
    frame_bottom_left = tk.Frame(frame_bottom)
    frame_bottom_right = tk.Frame(frame_bottom)

    frame_bottom_left.pack(side='left')
    frame_bottom_right.pack(side='right')    

    # 再細分bottom_left左右
    frame_bottom_left_top = tk.Frame(frame_bottom_left)
    frame_bottom_left_bottom = tk.Frame(frame_bottom_left)

    frame_bottom_left_top.pack(side='top')
    frame_bottom_left_bottom.pack(side='bottom')



    # -----------------     
    # | frame_top     |
    # |               |
    # |--------|------|
    # |bl-t    |  br  |
    # |--------|      |
    # |bl-b    |      |
    # |        |      | 
    # -----------------
    count = 0

    #把button 放在frame_bottom_left_bottom位置
    for item in RegisterRuleList:
        btn = tk.Button(frame_bottom_left_bottom, text=item["name"], command=partial(updateTreeView, item["table"]))
        btn.pack(fill='x',pady=5,anchor='center')
        count += 1


    #add treeview
    # ttk.Treeview(frame,height=18, show="headings", columns=('a','b','c','d','e','f'))

    treeview = ttk.Treeview(frame_bottom_right, height = 18, show="headings")
    treeview["columns"]=("name","access","address","defalut","value")  
    treeview.column("name", width=250)  #表示列,不顯示
    treeview.column("access", width=70) 
    treeview.column("address", width=120)
    treeview.column("defalut", width=120)
    treeview.column("value", width=150)

    treeview.heading("name", text="Register Name") #顯示錶頭
    treeview.heading("access", text="Access")
    treeview.heading("address", text="Address")
    treeview.heading("defalut", text="Default")
    treeview.heading("value", text="Value")

    treeview.pack(side='right')

    img = ImageTk.PhotoImage(Image.open("finger.jpg"))
    panel = tk.Label(frame_bottom_left_top, image = img)
    panel.pack(anchor='center', fill = "both", expand = "yes")

    window.mainloop()

def main():
    global RegisterRuleList
    RegisterRuleList = RegisterParser.parseRegisterTables()

    createWindow()
    

if __name__ == '__main__':
    main()