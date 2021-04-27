#!/usr/bin/python3
import tkinter as tk
import os
import sys
import time
from time import gmtime, strftime
Interface = os.popen('ip a|grep w |awk -F : \'{print $2}\'|head -1').read()
BSSIDS=[]
def setINT(inter):
	global Interface 
	Interface = inter
def Scan():
	global BSSIDS
	global Interface
	Interface = str(Interface)
	os.system('airmon-ng start' + Interface + ' 1> /dev/null')
	Interface = os.popen('ip a|grep w |awk -F : \'{print $2}\'|head -1').read()
	os.system('xterm -title \"7thsealSCAN\" -e airodump-ng --gpsd --band abg -w /etc/7thseal/breacher --output-format csv '+ Interface )
	time.sleep(5)
	breacher = open("/etc/7thseal/breacher-01.csv","r")
	uniq=[]
	for i in breacher:
		i = i.split(", ")
		z = str(i[0]) + "--->" + str(i[len(i)-2])
		x = str(i[0])
		if x not in uniq:
			uniq.append(x)
			BSSIDS.append(z)
		elif x == "\n":
			break
	breacher.close
	BSSIDS.pop(-(len(BSSIDS)-1))
	logname = strftime("%a,%d-%b-%Y_%H:%M",gmtime())
	os.system('mv /etc/7thseal/breacher-01.csv  /etc/7thseal/logs/' + logname )
def Menu():
	global Interface
	interswitch=0
	seal = tk.Tk()
	seal.title("7thSeal")
	x = 0
	Interface = Interface.split()
	for i in Interface:
		z = tk.Radiobutton(seal,text=i,variable = interswitch,value = i,command =setINT(interswitch))
		z.grid(row=x,column=1)
		x += 1
	WifiScan = tk.Button(text="Scan",width=25,height=5,bg="black",fg="white",command=Scan)
	WifiScan.grid(row=3,column=3)
	seal.mainloop()
def Results():
	global BSSIDS
	seal = tk.Tk()
	seal.title("7thSeal")
	Res = tk.Listbox(seal,width=60,height=50,selectmode="multiple")
	for i in BSSIDS:
		Res.insert(tk.END, i)
	Res.pack()
	seal.mainloop()

def main():
	global BSSIDS
	os.system('rm /etc/7thseal/breacher-01.csv 2> /dev/null')
	os.system('rm /etc/7thseal/breacher-01.gps 2> /dev/null')
	os.system('mkdir /etc/7thseal 2> /dev/null')
	os.system('mkdir /etc/7thseal/logs 2> /dev/null')
	Menu()
	Results()
	os.system('airmon-ng stop '+ Interface + ' 1> /dev/null')
if __name__ == '__main__':
    main()

