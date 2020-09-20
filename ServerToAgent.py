import os
import requests
import tkinter as tk
import socket


class Window:

	def __init__(self,master,server_ip,listening_port):
		self.listening_port = listening_port
		self.server_ip = str(socket.gethostbyname(socket.gethostname()))

		self.title_frame = tk.Frame(master=master,width=500,height=50, pady=5)
		self.title_label = tk.Label(
			master=self.title_frame,
			fg='#d71920',
			text="TEST CONNECTION",
			font=('Helvetica neue',20,'bold'))


		self.title_frame.pack()
		self.title_label.pack()

		self.client_ip_frame=tk.Frame(master=master,width=500,height=50,pady=10)
		self.client_ip_label = tk.Label(master=self.client_ip_frame, text="Client IP address:")
		self.client_ip_entry = tk.Entry(master=self.client_ip_frame, width=30)
		self.client_ip_frame.pack(fill=tk.X,padx=40)
		self.client_ip_label.pack(side=tk.LEFT)
		self.client_ip_entry.pack(side=tk.RIGHT)

		self.listening_frame = tk.Frame(master=master,width=500, height=50)
		self.listening_port_label = tk.Label(master=self.listening_frame, text="Agent Listening Port:")
		self.listening_port_entry = tk.Entry(master=self.listening_frame, width=30)
		self.listening_port_entry.insert(0, self.listening_port)
		self.listening_frame.pack(fill=tk.X,padx=40)
		self.listening_port_label.pack(side=tk.LEFT)
		self.listening_port_entry.pack(side=tk.RIGHT)

		self.server_ip_label = tk.Label(
			text='Server IP address:' + self.server_ip,
			fg='#A9A9A9'
		)

		self.server_ip_label.pack(
			fill=tk.X,
			pady=10
		)

		self.testButton = tk.Button(text="Test Connection",
									width=30,
									command=self.testConnection,
									bg='#0275d8')

		self.testButton.pack()

		self.url_label = tk.Label(text='URL: ',width=30)
		self.url_label.pack()

		self.status = tk.Label(text='Status: ')
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
				self.status['fg'] = '#5cb85c'
				
		except:
			print("Error: Unable to communicate with Agent")
			self.status['text'] = 'Error: Unable to communicate Agent!'
			self.status['fg'] = '#d9534f'
			
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
	root.geometry('500x250')
	root.mainloop()


	




