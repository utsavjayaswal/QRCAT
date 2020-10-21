# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 21:54:38 2020

@author: utsav
"""


# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 12:39:39 2020

@author: utsav
"""
import win32ui
import pymysql
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Combobox
from tkinter.ttk import Treeview
from tkinter import simpledialog
from tkinter import filedialog
from tkinter import messagebox
import datetime as dt
import time as tm
master=Tk()
master.title('Login')
master.geometry("200x70")
import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
#global suma

conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='1234')

cur = conn.cursor()
cur.execute("create database if not exists bills")
conn.commit()
cur.execute("use bills")

cur.execute("create table if not exists billdet(billid int auto_increment primary key,cusname char(20),mno char(10),gstin varchar(15),paymode char(10),bdate date,payamnt float)")
conn.commit()
cur.execute("create table if not exists itemdet(billid int,itname char(20),gstper int,sgst float ,cgst float,rate float,amount float,itmrp int,qty int,tamnt int)")
conn.commit()
cur.execute("create table if not exists paydet(billid int,cusname char(20),tgst float,trate float,tpaid float ,tdisper float)")
conn.commit()        


def open_window():
            la=[]
            univ=['Select type']
            five=['sweet','hhfood','drug']
            twelve=['processfood','milkp']
            eighteen=['shbeauty','computers']
            teight=['carsa','drinks']
            for k in five:
                univ.append(k)
            for k in twelve:
                univ.append(k)
            for k in eighteen:
                univ.append(k)
            for k in teight:
                univ.append(k)
            wdiss=""
            diss=""
            billString = ""
            billString+="----------------------------------------------!!JAI MATA DI!!---------------------------------------------\n"
            billString+="===================================================QRCAT==================================================\n"
            billString+="__________________________________________________Receipt_________________________________________________\n"
            
            billString+="__________________________________________________________________________________________________________\n"
            billString+="{:<15}{:<10}{:<12}{:<12}{:<12}{:<12}{:<12}{:<10}{:<12}\n".format("Itemname", "GST(%)", "SGST(Rs.)", "CGST(Rs.)","Rate(Rs.)","Amount(dc)","MRP(Rs.)",'Quantity',"T.Amount")
            billString+="__________________________________________________________________________________________________________\n"
            suma=0
            i=0
            tgsto=0
            trateo=0
            def newbill():
                
                top.destroy()
                open_window()
                
                
            def camcap():
                nonlocal la
                nonlocal i
                nonlocal suma
                nonlocal tgsto
                nonlocal trateo
                nonlocal wdiss
                nonlocal five
                nonlocal twelve
                nonlocal eighteen
                nonlocal teight
                cap=cv2.VideoCapture(0)
                font=cv2.FONT_HERSHEY_PLAIN
                flag=1
                while flag:
                    _, frame=cap.read()
                    cv2.imshow("Frame", frame)
          
                    decodedObjects=pyzbar.decode(frame)
                    for obj in decodedObjects:
            
            #cv2.putText(frame, str(obj.data), (50, 50), font, 2,
                        #(255, 0, 0), 3)
            
                        y=str(obj.data)
                        x=[]
                        x.append(y[2:len(y)-1].split(','))
                        la.append(x[0])

                        s=simpledialog.askstring("quant","quantity:")
                        if x[0][2] in five:
                            la[i].append(int(5))
                            la[i].append(int(x[0][1])*(.025))
                            la[i].append(int(x[0][1])*(.025))
                        elif x[0][2] in twelve:
                            la[i].append(int(12))
                            la[i].append(int(x[0][1])*(int(6)/100))
                            la[i].append(int(x[0][1])*(int(6)/100))
                        elif x[0][2] in eighteen:
                            la[i].append(int(18))
                            la[i].append(int(x[0][1])*(int(9)/100))
                            la[i].append(int(x[0][1])*(int(9)/100))
                        elif x[0][2]==teight:
                            la[i].append(int(28))
                            la[i].append(int(x[0][1])*(int(14)/100))
                            la[i].append(int(x[0][1])*(int(14)/100))
                            
                        la[i].append(int(la[i][1])-(float(la[i][4])+float(la[i][5])))    
                        la[i].append(int(s))
                        la[i].append(int(la[i][1]))
                        la[i].append(int(la[i][8])*la[i][7])
                        la[i][6]=round(la[i][6],2)
                        tv.insert('','end','item'+str(i),values=(la[i][0],str(la[i][3])+'%',str(round(la[i][4],2))+'Rs.',str(round(la[i][5],2))+'Rs.',str(la[i][6])+'Rs.',la[i][8],la[i][1],la[i][7],la[i][9]),tags=('odd',))
                        tv.tag_configure('odd', background='orange')
                        #print('item'+str(i))
                        suma+=int(la[i][9])
                        e3.delete(0,END)
                        e3.insert(0,str(suma)+'Rs.')
                        tgsto+=round((la[i][4]*2)*la[i][7],2)
                        trateo+=round((la[i][6])*la[i][7],2)
                        e7.delete(0,END)
                        e7.insert(0,str(tgsto)+'Rs.')
                        e8.delete(0,END)
                        e8.insert(0,str(trateo)+'Rs.')
                        #setting default value of discount to zero //will help in printing bill
                        e4.delete(0,END)
                        e4.insert(0,str(0))
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        wdiss+="{:<17}{:<10}{:<12}{:<12}{:<12}{:<12}{:<12}{:<10}{:<12}\n".format(la[i][0], str(la[i][3])+'%', round(la[i][4],2), round(la[i][5],2),round(la[i][6],2),round(la[i][8],2),la[i][1],la[i][7],str(round(la[i][9],2))+'Rs.')
                        i+=1
                        
                        flag=0
                        break
                    if cv2.waitKey(1)&0xFF==ord('q'):
                        break
                cap.release()
                cv2.destroyAllWindows()
            
            def printbill():
                nonlocal billString
                
                csn=str(e1.get())
                mno=str(e2.get())
                gstina=str(e6.get())
                
                billdate=f"{dt.datetime.now():%a, %b %d %Y}"
                now=dt.datetime.now()

                currtime=now.strftime("%H:%M:%S")
                a1=billString
                a2='Customer name:'+csn+'           mobile no:'+mno+'           Billing time:'+billdate+','+currtime+'\n'+'GSTIN:'+gstina+'\n'
                #a3="                    {dt.datetime.now():%a, %b %d %Y}"
                abd=list(a1)
                abd.insert(321,a2)
                billString=''.join(abd)
                if int(e4.get())>0:
                    billString+=diss
                else:
                    billString+=wdiss
                if(pay.get()==0):
                    paymd='Cash'
                else:  
                    paymd='D/C Card'
                
                
                billString+="___________________________________________________________________________________________________________\n"
                billString+="{:<10}{:<10}{:<12}{:<12}{:<12}{:<12}{:<12}{:<10}{:<20}\n".format("Paymode:",paymd," "," ","Total GST:",e7.get()," ","Total discount:",e4.get()+'%')
                billString+="{:<10}{:<10}{:<12}{:<12}{:<12}{:<12}{:<12}{:<10}{:<20}\n".format(" "," "," "," ","Total Rate:",e8.get()," ","Grand Total(To pay):",e3.get())
                billFile = filedialog.asksaveasfile(mode='w',defaultextension=".txt")
                if billFile is None:
                    messagebox.showerror("Invalid file Name", "Please enter valid name")
                else:
                    billFile.write(billString)
                    billFile.close()
                
                cur.execute("insert into billdet(cusname,mno,gstin,paymode,bdate,payamnt) values(%s,%s,%s,%s,curdate(),%s)",(e1.get(),e2.get(),e6.get(),paymd,float(e3.get()[:-3])))
                conn.commit()
                cur.execute("select billid from billdet order by billid desc limit 1")
                for i in cur:
                    x=i[0]
                for line in tv.get_children():
                    tempit=tv.item(line)['values']
                    cur.execute("insert into itemdet(billid,itname,gstper,sgst,cgst,rate,amount,itmrp,qty,tamnt) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(x,tempit[0],tempit[1][:-1],tempit[2][:-3],tempit[3][:-3],tempit[4][:-3],tempit[5],tempit[6],tempit[7],tempit[8]))
                    conn.commit()     
                cur.execute("insert into paydet(billid,cusname,tgst,trate,tpaid,tdisper) values(%s,%s,%s,%s,%s,%s)",(x,e1.get(),float(e7.get()[:-3]),float(e8.get()[:-3]),float(e3.get()[:-3]),float(e4.get())))    
                conn.commit()               
                    

            
            
            
            
            
            top = Toplevel()
            top.title("QRCAT 1.0")
            top.geometry("950x510")
            #top.geometry("800x500")
            button1=Button(top,text="Quit",height=2,width=5,command=lambda:[top.destroy(),master.destroy()]).grid(row=20,column=7)
            #Label(top,text="jai shri ganesh").grid(row=0)
            Label(top,text="jai mata di").grid(row=0,column=0)
            Label(top,text="Customer Name:").grid(row=2,column=0)
            Label(top,text="Mobile no:").grid(row=2,column=2)
            Label(top,text="____WELCOME TO QRCAT____",bg='green',fg='white',bd='4',anchor='center').grid(row=0,column=2)
            e1=Entry(top)
            e1.grid(row=2,column=1)
            e2=Entry(top)
            e2.grid(row=2,column=3)
            Label(top,text='GST_IN:').grid(row=2,column=4)
            e6=Entry(top)
            e6.grid(row=2,column=5)
            
            
            
            baitem=Button(top,text="Add item(QR)",command=camcap).grid(row=4)
            
            style = ttk.Style()
            style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11)) 
            style.configure("mystyle.Treeview.Heading", font=('Calibri', 13,'bold')) 
            style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) 
            tv=ttk.Treeview(top,height=15,columns=('item_name','GST','SGST','CGST','Rate','Amount','MRP','quantity','Total amount'),style="mystyle.Treeview")
            tv.grid(row=8,column=0,columnspan=8)
            tv.heading('#1',text='itemname')
            tv.heading('#2',text='GST(%)')
            tv.heading('#3',text='SGST')
            tv.heading('#4',text='CGST')
            tv.heading('#5',text='Rate(pp)')
            tv.heading('#6',text='Amount(pp/d)')
            tv.heading('#7',text='MRP(pp)')
            tv.heading('#8',text='Quantity')
            tv.heading('#9',text='T.Amount')
            tv['show']='headings'
            tv.column('item_name',width=130,anchor='center')
            tv.column('GST',width=100,anchor='center')
            tv.column('SGST',width=100,anchor='center')
            tv.column('CGST',width=100,anchor='center')
            tv.column('Rate',width=100,anchor='center')
            tv.column('Amount',width=100,anchor='center')
            tv.column('MRP',width=100,anchor='center')
            tv.column('quantity',width=100,anchor='center')
            tv.column('Total amount',width=100,anchor='center')
            Button(top,text='Generate bill',command=printbill).grid(row=15,column=0)
            
            #tv.tag_configure('even', background='#DFDFDF')
            bnewb=Button(top,text="NEW BILL",command=newbill).grid(row=15,column=1)
            
            Label(top,text='GRAND Total(To Pay)').grid(row=16,column=5)
            e3=Entry(top)
            e3.grid(row=16,column=6)
            Label(top,text='Total Discount(%):').grid(row=15,column=5)
            e4=Entry(top)
            e4.grid(row=15,column=6)
            Label(top,text='Total GST(Rs.)').grid(row=15,column=3)
            e7=Entry(top)
            e7.grid(row=15,column=4)
            Label(top,text='Total Rate(Rs.,wgst)').grid(row=16,column=3)
            e8=Entry(top)
            e8.grid(row=16,column=4)
            #e4.bind("<Return>", (lambda event: reply(ent.get())))
            #creating radio buttons
            radioGroup=LabelFrame(top,text="Select Payment mode")
            radioGroup.grid(row=15,column=2)
            pay=IntVar()
            cash=Radiobutton(radioGroup,text="Cash",variable=pay,value=0)
            cash.grid(row=16,column=2)
            dcc=Radiobutton(radioGroup,text="D/C card",variable=pay,value=1)
            dcc.grid(row=16,column=3)
            
            def dbwindow():
                dbwin=Toplevel()
                dbwin.title("Bills & Databases")
                dbwin.geometry('800x400')
                #fr1=Frame(dbwin)
                #fr1.pack(side='top')
                #fr2=Frame(dbwin)
                #fr2.pack(side='bottom')
                sbillab=Label(dbwin,text='To search a Bill:'+'\n'+'(enter name)').grid(row=0,column=0)
                sbill=Entry(dbwin)
                sbill.grid(row=0,column=1)
                fbillab=Label(dbwin,text='To Fetch a bill:'+'\n'+'(enter bill id)').grid(row=0,column=2)
                fbill=Entry(dbwin)
                fbill.grid(row=0,column=3)
                
                
                
                
                tvsb=ttk.Treeview(dbwin,height=8,columns=('billid','csname','mno','gstin','paymode','billdate','payamnt'))
                tvsb.grid(row=2,column=0,columnspan=7)
    
                vsb = ttk.Scrollbar(dbwin, orient="vertical", command=tvsb.yview)
                vsb.grid(row=2,column=8,sticky='nse')   
                
                
                
                
                def showbillstart():
                    
                    
    
                    tvsb.configure(yscrollcommand=vsb.set)
                    tvsb.heading('#1',text='BillId')
                    tvsb.heading('#2',text='Customer name')
                    tvsb.heading('#3',text='mobile_no')
                    tvsb.heading('#4',text='GSTIN')
                    tvsb.heading('#5',text='pay mode')
                    tvsb.heading('#6',text='bill_date')
                    tvsb.heading('#7',text='Total paid')
                    tvsb['show']='headings'
                    tvsb.column('billid',width=100,anchor='center')
                    tvsb.column('csname',width=100,anchor='center')
                    tvsb.column('mno',width=100,anchor='center')
                    tvsb.column('gstin',width=150,anchor='center')
                    tvsb.column('paymode',width=100,anchor='center')
                    tvsb.column('billdate',width=100,anchor='center')
                    tvsb.column('payamnt',width=100,anchor='center')
                    j=1
                    cur.execute("select * from billdet ")
                    for i in cur:
                        tvsb.insert('','end','item'+str(j),values=(i[0],i[1],i[2],i[3],i[4],i[5],i[6]))
                        j+=1
    
                    j=1
                showbillstart()       
                    
                #shbills=Button(dbwin,text="show all bills",command=showbills).grid(row=0,column=0)   
                
                def searchbill():
                    j=1
                    x=sbill.get()
                    if not x:
                        cur.execute("select * from billdet")
                        tvsb.delete(*tvsb.get_children())
                        for i in cur:
        
                            tvsb.insert('','end','item'+str(j),values=(i[0],i[1],i[2],i[3],i[4],i[5],i[6]))
                            j+=1
                    else:
                        
                        cur.execute("select * from billdet where cusname=%s",(x))
                        tvsb.delete(*tvsb.get_children())
                        for i in cur:
        
                            tvsb.insert('','end','item'+str(j),values=(i[0],i[1],i[2],i[3],i[4],i[5],i[6]))
                            j+=1
                sbill.bind("<Return>", (lambda event:searchbill()))
                
                
                def fetchbill():
                    j=1
                    y=fbill.get()
                    if not y:
                        cur.execute("select * from billdet")
                        tvsb.delete(*tvsb.get_children())
                        for i in cur:
        
                            tvsb.insert('','end','item'+str(j),values=(i[0],i[1],i[2],i[3],i[4],i[5],i[6]))
                            j+=1
                    else:
                        billfetchw=Toplevel()
                        billfetchw.geometry('1000x400')
                        frame1=Frame(billfetchw)
                        frame1.pack(side='top')
                        frame2=Frame(billfetchw)
                        frame2.pack(side='top')
                        
                        printbilltb=Text(frame1,width=115,height=20)
                        #printbilltb.grid(row=0,column=0)
                        printbilltb.pack(side='left')
                        vsbtxt = ttk.Scrollbar(frame1, orient="vertical", command=printbilltb.yview)
                        vsbtxt.pack(side='right',fill='y')  
                        printbilltb.configure(yscrollcommand=vsbtxt.set)
                        
                        tempps=[]
                        printstring = ""
                        printstring+="----------------------------------------------!!JAI MATA DI!!---------------------------------------------\n"
                        printstring+="===================================================QRCAT==================================================\n"
                        printstring+="__________________________________________________Receipt_________________________________________________\n"
                        cur.execute("select * from billdet where billid=%s",(y))
                        for i in cur:
                            tempps=[i[0],i[1],i[2],i[3],i[4],i[5],i[6]]
                            #print(tempps)
                            
                        datestr=tempps[5]
                        datetoins=dt.datetime.strftime(datestr,'%Y-%m-%d')
                            
                        printstring+='Customer name:'+tempps[1]+'           mobile no:'+tempps[2]+'           Billing Date:'+datetoins+'\n'+'GSTIN:'+tempps[3]+'\n'
                        printstring+="__________________________________________________________________________________________________________\n"
                        printstring+="{:<15}{:<10}{:<12}{:<12}{:<12}{:<12}{:<12}{:<10}{:<12}\n".format("Itemname", "GST(%)", "SGST(Rs.)", "CGST(Rs.)","Rate(Rs.)","Amount(dc)","MRP(Rs.)",'Quantity',"T.Amount")
                        printstring+="__________________________________________________________________________________________________________\n"
                        cur.execute("select * from itemdet where billid=%s",(y))
                        for i in cur:
                             printstring+="{:<17}{:<10}{:<12}{:<12}{:<12}{:<12}{:<12}{:<10}{:<12}\n".format(i[1],str(i[2])+'%',str(i[3])+'Rs.',str(i[4])+'Rs.',str(i[5])+'Rs.',str(i[6])+'Rs.',str(i[7])+'Rs.',i[8],i[9])
                        paymodeamnt=[]
                        cur.execute("select paymode from billdet where billid=%s",(y))
                        for i in cur:
                            paymodeamnt=[i[0]]
                        cur.execute("select tgst,trate,tpaid,tdisper from paydet where billid=%s",(y))
                        detpay=[]
                        for i in cur:
                            detpay=[i[0],i[1],i[2],i[3]]
                        printstring+="___________________________________________________________________________________________________________\n"
                        printstring+="{:<10}{:<10}{:<12}{:<12}{:<12}{:<12}{:<12}{:<10}{:<20}\n".format("Paymode:",paymodeamnt[0]," "," ","Total GST:",str(detpay[0])+'Rs.'," ","Total discount:",str(detpay[3])+'%')
                        printstring+="{:<10}{:<10}{:<12}{:<12}{:<12}{:<12}{:<12}{:<10}{:<20}\n".format(" "," "," "," ","Total Rate:",str(detpay[1])+'Rs.'," ","Grand Total(To pay):",str(detpay[2])+'Rs.')    
                            
                            
                            
                        
                        
                        printbilltb.insert('end',printstring)
                        printbilltb.config(state='disabled')
                        def savefetchbill():
                            billFile1 = filedialog.asksaveasfile(mode='w',defaultextension=".txt")
                            if billFile1 is None:
                                messagebox.showerror("Invalid file Name", "Please enter valid name")
                            else:
                                billFile1.write(printstring)
                                billFile1.close()
                        printbutt=Button(frame2,text='Save Bill',command=savefetchbill,width=8,height=2)
                        printbutt.pack(side='top')
                        
                        
                            
                        
                        
                        
                        
                fbill.bind("<Return>", (lambda event:fetchbill()))         
                
                
            btdatab=Button(top,text="BILLS",command=dbwindow).grid(row=4,column=6)
            
            
            
            def discount():
                nonlocal suma
                nonlocal la
                nonlocal diss
                tgst=0
                newsum=0
                trate=0
                disa=int(e4.get())
                #suma=int(suma)-int(suma)*(int(e4.get())/100)
                #e3.delete(0,END)
                #e3.insert(0,str(suma))
                for h in range(i):
                    #print(h)
                    #print(i)
                    la[h][8]=int(la[h][1])-(int(la[h][1])*(int(disa)/100))
                    la[h][4]=(int(la[h][8])*(int(la[h][3])/100))/2
                    la[h][5]=la[h][4]
                    la[h][6]=la[h][8]-(2*la[h][4])
                    la[h][6]=round(la[h][6],2)
                    la[h][9]=la[h][8]*la[h][7]
                    tv.item('item'+str(h),values=(la[h][0],str(la[h][3])+'%',str(round(la[h][4],2))+'Rs.',str(round(la[h][5],2))+'Rs.',str(la[h][6])+'Rs.',round(la[h][8],2),la[h][1],la[h][7],round(la[h][9],2)))
                    newsum+=la[h][9]
                    tgst+=round((la[h][4]*2)*la[h][7],2)
                    diss+="{:<17}{:<10}{:<12}{:<12}{:<12}{:<12}{:<12}{:<10}{:<12}\n".format(la[h][0], str(la[h][3])+'%', round(la[h][4],2), round(la[h][5],2),round(la[h][6],2),round(la[h][8],2),la[h][1],la[h][7],str(round(la[h][9],2))+'Rs.')
                    trate+=round((la[h][6])*la[h][7],2)
                e3.delete(0,END)
                e3.insert(0,str(round(newsum,2))+'Rs.')
                e7.delete(0,END)
                e7.insert(0,str(round(tgst,2))+'Rs.')
                e8.delete(0,END)
                e8.insert(0,str(round(trate,2))+'Rs.')
            e4.bind("<Return>", (lambda event:(discount())))
            #tb=Text(top,height=1,width=15)
            #tb.grid(row=0,column=3)
            #tb.insert(INSERT,"BILL_NO."+str)
            #date = dt.datetime.now()
            
            
            Label(top, text=f"{dt.datetime.now():%a, %b %d %Y}", fg="black", bg="white",bd=4).grid(row=0,column=5)
                
            def mancap():
                nonlocal univ
                top1=Toplevel()
                top1.title('add item manually')
                top1.geometry("600x50")
                Label(top1,text="item name:").grid(row=0,column=0)
                em1=Entry(top1)
                em1.grid(row=0,column=1)
                Label(top1,text="MRP").grid(row=0,column=2)
                em2=Entry(top1)
                em2.grid(row=0,column=3)
                Label(top1,text="type:").grid(row=0,column=4)
                #em3=Entry(top1)
                #em3.grid(row=0,column=5)
                em3=ttk.Combobox(top1,values=univ,width=10)
                em3.grid(row=0,column=5)
                em3.current(0)
                
                
                Label(top1,text="quantity:").grid(row=1,column=2)
                em4=Entry(top1)
                em4.grid(row=1,column=3)
                
                def mancapquit():
                    top1.destroy()
                
                
                bmcquit=Button(top1,text='Quit',command=mancapquit).grid(row=1,column=6)
                def addmtl():
                    nonlocal suma
                    nonlocal tgsto
                    nonlocal trateo
                    nonlocal wdiss
                    nonlocal five
                    nonlocal twelve
                    nonlocal eighteen
                    nonlocal teight
                    templ=[em1.get(),int(em2.get()),em3.get()]
                    nonlocal i 
                    la.append(templ)
                    if templ[2] in five:
                            la[i].append(int(5))
                            la[i].append(int(templ[1])*(.025))
                            la[i].append(int(templ[1])*(.025))
                    elif templ[2] in twelve:
                            la[i].append(int(12))
                            la[i].append(int(templ[1])*(int(6)/100))
                            la[i].append(int(templ[1])*(int(6)/100))
                    elif templ[2] in eighteen:
                            la[i].append(int(18))
                            la[i].append(int(templ[1])*(int(9)/100))
                            la[i].append(int(templ[1])*(int(9)/100))
                    elif templ[2] in teight:
                            la[i].append(int(28))
                            la[i].append(int(templ[1])*(int(14)/100))
                            la[i].append(int(templ[1])*(int(14)/100))
                    
                    la[i].append(int(la[i][1])-(float(la[i][4])+float(la[i][5])))    
                    la[i].append(int(em4.get()))
                    la[i].append(int(la[i][1]))
                    la[i].append(int(la[i][8])*la[i][7])
                    la[i][6]=round(la[i][6],2)
                    tv.insert('','end','item'+str(i),values=(la[i][0],str(la[i][3])+'%',str(round(la[i][4],2))+'Rs.',str(round(la[i][5],2))+'Rs.',str(round(la[i][6],2))+'Rs.',round(la[i][8],2),la[i][1],la[i][7],round(la[i][9],2)),tags=('odd',))
                    tv.tag_configure('odd', background='orange')
                        #print('item'+str(i))
                    suma+=int(la[i][9])
                    e3.delete(0,END)
                    e3.insert(0,str(suma)+'Rs.')
                    tgsto+=round((la[i][4]*2)*la[i][7],2)
                    trateo+=round((la[i][6])*la[i][7],2)
                    e7.delete(0,END)
                    e7.insert(0,str(round(tgsto,2))+'Rs.')
                    e8.delete(0,END)
                    e8.insert(0,str(round(trateo,2))+'Rs.')
                        #setting default value of discount to zero //will help in printing bill
                    e4.delete(0,END)
                    e4.insert(0,str(0))
                        
                    wdiss+="{:<17}{:<10}{:<12}{:<12}{:<12}{:<12}{:<12}{:<10}{:<12}\n".format(la[i][0], str(la[i][3])+'%', round(la[i][4],2), round(la[i][5],2),round(la[i][6],2),round(la[i][8],2),la[i][1],la[i][7],str(round(la[i][9],2))+'Rs.')
                    i+=1
                    em1.delete(0,END)
                    em2.delete(0,END)
                    em3.delete(0,END)
                    em4.delete(0,END)
                bsub=Button(top1,text='add',command=addmtl).grid(row=1,column=5)        
                        
            baitemm=Button(top,text="Add item(manually)",command=mancap).grid(row=4,column=2)
            
            def shgst():
                nonlocal five,twelve,eighteen,teight
                
                topg=Toplevel()
                topg.title('GST categories')
                
                f1=Frame(topg)
                f1.pack(side='left')
                topg.geometry('680x165')
                f2=Frame(topg)
                f2.pack(side='left')
                tvg=ttk.Treeview(f1,height=5,columns=('GST(%)','itemtypes'))
                tvg.grid(row=0,column=0)
                tvg.heading('#1',text='GST(%)')
                tvg.heading('#2',text='item type')
                tvg['show']='headings'
                tvg.column('GST(%)',width=100,anchor='center')
                tvg.column('itemtypes',width=300,anchor='center')
                tvg.insert('','end','item5',values=('5%',five))
                tvg.insert('','end','item12',values=('12%',twelve))
                tvg.insert('','end','item18',values=('18%',eighteen))
                tvg.insert('','end','item28',values=('28%',teight))
                
                cats=["select GST category","5%","12%","18%","28%"]
                Label(f2,text="add a new item type:").grid(row=1,column=0)
                Label(f2,text="Choose category").grid(row=2,column=0)
                
                cb=ttk.Combobox(f2,values=cats,width=20)
                cb.grid(row=3,column=0)
                cb.current(0)
                eg1=Entry(f2)
                eg1.grid(row=3,column=1)
                
                def addnewtyp():
                    if(cb.get()=='5%'):
                        five.append(eg1.get())
                        univ.append(eg1.get())
                        tvg.item('item5',values=('5%',five))
                    elif(cb.get()=='12%'):
                        twelve.append(eg1.get())
                        univ.append(eg1.get())
                        tvg.item('item12',values=('12%',twelve))
                    elif(cb.get()=='18%'):
                        eighteen.append(eg1.get())
                        univ.append(eg1.get())
                        tvg.item('item18',values=('18%',eighteen))
                    elif(cb.get()=='28%'):
                        teight.append(eg1.get())
                        univ.append(eg1.get())
                        tvg.item('item28',values=('28%',teight))
                        
                    eg1.delete(0,END)
                    cb.current(0)
                
                
                
                
                def gstcatquit():
                    topg.destroy()
                
                eg1.bind("<Return>", (lambda event:(addnewtyp())))
                bgquit=Button(f2,text='Quit',height=2,width=6,command=gstcatquit).grid(row=10,column=1)
               
            
            
            
            
            
            bshgst=Button (top,text='Show Gst categories',command=shgst).grid(row=4,column=4)
                        
Label(master, text="Username").grid(row=0)
Label(master, text="Password").grid(row=1)
e1=Entry(master)
e2=Entry(master,show='*')
e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
def suba():
    if e1.get()=='utsav' and e2.get()=='123': 
        master.withdraw()
        open_window()
    else:
        messagebox.showinfo("hurrrrr", ":-|hatt be..wrong credentials")
        e1.delete(0,END)
        e2.delete(0,END)
        
        

Button(master,text='Submit',command=suba).grid(row=10,column=0,sticky=W,pady=4)
master.mainloop()