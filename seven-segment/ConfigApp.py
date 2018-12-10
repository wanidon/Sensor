#!/usr/bin/python
#coding:utf-8
from Tkinter import *
from ttk import *
from tkMessageBox import *
from collections import OrderedDict
from Constants import *
import json
import sys

#TODO traceback
class ConfigApp(Frame):
    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.DEBUG = True

        #入力エントリ生成メソッド用のクラス変数
        self.numEntryRow = 0

        #入力エントリを配置するフレーム
        self.entryFrame = Frame(root,padding=10)
        self.entryFrame.grid()
        
        #入力値を格納する辞書
        self.inputDict = OrderedDict()

        self.boundKeyList = [
            UPBOUNDCAREFUL,
            UPBOUNDSAFETY,
            LWBOUNDSAFETY,
            LWBOUNDCAREFUL
        ]
        self.intKeyList = [
            INTERVAL
        ]
        self.stringKeyList = [
            FROMADDR,
            PASSWORD,
            TOADDR
        ]
        
        #辞書の値を初期化
        for k in self.boundKeyList:
           self.inputDict[k] = StringVar()
        for k in self.intKeyList:
            self.inputDict[k] = StringVar()
        for k in self.stringKeyList:
            self.inputDict[k] = StringVar()
        self.inputDict[FROMADDR].set("@gmail.com")

        #GUI上の入力エントリ生成
        for key,value in self.inputDict.items():
            self.genEntry(key,value)
        
        #保存ボタン
        saveButton = Button(root,text="SAVE",command=self.save)
        saveButton.grid()

        #二次元空間上に配置
        self.grid()

    
    #入力エントリを生成するメソッド
    def genEntry(self,text,varname):
        tmpLabel = Label(self.entryFrame,text = text,padding=5)
        tmpLabel.grid(row=self.numEntryRow,column=0,sticky=E)
        tmpEntry = Entry(self.entryFrame,textvariable=varname,width=40)
        tmpEntry.grid(row=self.numEntryRow,column=1)
        self.numEntryRow = self.numEntryRow + 1


    #保存ボタンを押した際に呼び出すメソッド
    def save(self):
        for k,v in self.inputDict.items():
            #空白文字を削除しておく
            v.set("".join(v.get().split()))
            #値が入力されているか確認
            if v.get() == "":
                msg = "input \""+k+"\""
                self.dbg(msg)
                showerror("Error",msg)
                return None

        #境界値がfloatに変換できるかチェック
        try:
            boundVals = []
            for k in self.boundKeyList:
                boundVals.append(float(self.inputDict[k].get()))
        except ValueError:
            msg = "\""+k+"\"" + "can not be conveted to number" 
            self.dbg(msg)
            return None
        except :
            #TODO msg
            self.dbg(msg)
            self.dbg(Exception)
            sys.exit()

        #整数入力値がintに変換できるかチェック
        try:
            intVals = []
            for k in self.intKeyList:
                intVals.append(int(self.inputDict[k].get()))
        except ValueError:
            msg = "\""+k+"\"" + "can not be conveted to integer" 
            self.dbg(msg)
            return None
        except Exception:
            msg = "An unknown error has occurred"
            self.dbg(msg)
            self.dbg(Exception)
            sys.exit()
            #TODO msg

        #境界値の大小チェック
        if not(boundVals[0] > boundVals[1]
        and boundVals[1] > boundVals[2]
        and boundVals[2] > boundVals[3] ):
            #TODO　msg
            self.dbg("incorrect bound value")
            return None

        try:
            #json形式にして書き込み
            outputDict = OrderedDict()
            for k,v in zip(self.boundKeyList,boundVals):
                outputDict[k] = v
            for k,v in zip(self.intKeyList,intVals):
                outputDict[k] = v
            for k in self.stringKeyList:
                outputDict[k] = self.inputDict[k].get()

            with open("config.json","w") as f:
                json.dump(outputDict,f,indent=4)
                self.dbg("complete")
                showinfo("message","succeeded to save the configurations!")
        except IOError:
            self.dbg("An IO error has occurred")
            #TODO msg

            



    def dbg(self,something):
        if self.DEBUG == True:
            print(something)
            
                 


#ルートフレーム
root = Tk()
root.title(u"config")

app = ConfigApp(master=root)
app.mainloop()