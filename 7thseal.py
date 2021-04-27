#!/usr/bin/env python3
import tkinter as tk
import os
import sys
Interface = os.popen('ip a|grep w |awk -F : \'{print $2}\'|head -1').read()
BSSIDS=[]
def Scan():
    global BSSIDS
    global Interface
    os.system('airmon-ng start' + Interface)
    Interface = os.popen('ip a|grep w |awk -F : \'{print $2}\'|head -1').read()
    os.system('xterm -title \"7thsealSCAN\" -e airodump-ng --gpsd --band abg -w /etc/7thseal/breacher --output-format csv '+ Interface)
    breacher = open("/etc/7thseal/breacher.csv","r")
    for i in breacher:
        BSSIDS.append(i)
    breacher.close
def Menu():
    seal = tk.Tk()
    seal.title("7thSeal")
    WifiScan = tk.Button(text=Interface + " Scan",width=25,height=5,bg="black",fg="white")
    WifiScan.grid(row=3,column=3)
    seal.mainloop()


def main():
    global BSSIDS
    os.system('mkdir /etc/7thseal')
    Menu()
    print(BSSIDS)
if __name__ == '__main__':
    main()

