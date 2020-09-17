import os
import requests
import tkinter as tk
import socket

class Window:
	def __init__(self,master,server_ip,listening_port):
		self.server_ip = str(socket.gethostbyname(socket.gethostname()))
		self.listening_port = listening_port

		self.frame = tk.Frame(width=30,height=80)

		self.server_ip_label = tk.Label(text='Server IP address:' + self.server_ip)
		self.listening_port_label = tk.Label(text="Agent Listening Port:")
		self.url_label = tk.Label(text='URL: ')
		self.status = tk.Label(text='Status: ')
		self.listening_port_entry = tk.Entry()
		self.listening_port_entry.insert(0,self.listening_port)
		self.client_ip_label= tk.Label(text="Client IP address")
		self.client_ip_entry = tk.Entry(width=30)
		self.testButton = tk.Button(text="Test Connection", width=30,command=self.testConnection)

		self.server_ip_label.pack()
		self.listening_port_label.pack()
		self.listening_port_entry.pack()
		self.client_ip_label.pack()
		self.client_ip_entry.pack()
		self.testButton.pack()
		self.url_label.pack()
		self.status.pack()




	def testConnection(self):
		url = 'https://' + self.client_ip_entry.get() + ":" + self.listening_port_entry.get() + "/?CAVIT"
		self.url_label['text'] = 'URL:' + url

		try:
			x = requests.get(url,verify=False)
			print(x.text)
			if '!CRYPT!' in x.text:
				print('Connection OK!')
				self.status['text'] = 'Status: Connection Ok!'
				
		except:
			print("Error: Unable to communicate with Agent")
			self.status['text'] = 'Error: Unable to communicate Agent!'
			
		else:
			print('proceed')

if __name__ == '__main__':
	server_ip_address = '192.168.1.254'

	try:
		os.chdir('C:\\Program Files (x86)\\Trend Micro\\Apex One\\PCCSRV')
		with open('ofcscan.ini','r') as file:
			for line in file:
				if 'Client_LocalServer_Port' in line:
					listening_port = str(int(''.join(filter(str.isdigit,line))))
	except:
		listening_port = ''

	root = tk.Tk()
	Window = Window(master=root,server_ip=server_ip_address, listening_port=listening_port)
	root.title("Server Test Connection")
	root.geometry('250x250')
	root.mainloop()


	




