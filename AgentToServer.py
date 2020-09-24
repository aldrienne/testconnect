import platform
import socket
import subprocess
import tkinter as tk
import winreg as winreg

import requests


class Window:

    def __init__(self, master, server_ip, server_port, agent_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.agent_port = agent_port

        # Frame for title
        self.title_frame = tk.Frame(master=master, width=500, height=50, pady=5)
        self.title_label = tk.Label(
            master=self.title_frame,
            fg='#d71920',
            text="TEST CONNECTION",
            font=('Helvetica neue', 20, 'bold'))
        self.title_frame.pack(pady=15)
        self.title_label.pack()

        # Frame for Server IP
        self.server_ip_frame = tk.Frame(master=master, width=400, height=50)
        self.server_ip_label = tk.Label(master=self.server_ip_frame, text="Server IP Address")
        self.server_ip_entry = tk.Entry(master=self.server_ip_frame)
        self.server_ip_frame.pack(fill=tk.X, padx=80, pady=5)
        self.server_ip_label.pack(side=tk.LEFT)
        self.server_ip_entry.pack(side=tk.RIGHT)

        # Frame for Port
        self.port_frame = tk.Frame(master=master, width=400, height=50)
        self.server_port_label = tk.Label(master=self.port_frame, text="Port")
        self.server_port_entry = tk.Entry(master=self.port_frame)
        self.port_frame.pack(fill=tk.X, padx=80, pady=10)
        self.server_port_label.pack(side=tk.LEFT)
        self.server_port_entry.pack(side=tk.RIGHT)
        self.server_port_entry.insert(0, self.server_port)

        # Frame for Butttons
        self.list_buttons_frames = tk.Frame(master=master, width=400, height=50)
        self.testButton = tk.Button(master=self.list_buttons_frames, text="Test Connection",
                                    command=self.testConnection, width=13)
        self.testSmartScan = tk.Button(master=self.list_buttons_frames, text="Test SmartScan",
                                       command=self.testSmartScan, width=13)
        #self.testPorts_button = tk.Button(master=self.list_buttons_frames, text="Test Ports", command=self.testPorts,
        #                                 width=13)
        self.list_buttons_frames.pack(pady=10)
        self.testButton.pack()
        self.testSmartScan.pack()
        #self.testPorts_button.pack()

        # Test Connection Frame
        self.connection_status_frame = tk.Frame(master=master, width=400, height=50)
        self.connection_status_frame.pack(pady=15)
        self.connection_status_label = tk.Label(master=self.connection_status_frame,text="Connection Status",font=('Helvetica neue', 10, 'bold'),fg='#A9A9A9')
        self.connection_status_label.pack()
        self.ping_status_label = tk.Label(master=self.connection_status_frame,text="PING:")
        self.ping_status_label.pack()
        self.telnet_status_label = tk.Label(master=self.connection_status_frame,text="TELNET:")
        self.telnet_status_label.pack()
        self.cgi_status_label = tk.Label(master=self.connection_status_frame,text="CGI:")
        self.cgi_status_label.pack()

        #Smartscan Frame
        self.smart_scan_frame = tk.Frame(master=master, width=400, height=50)
        self.smart_scan_frame.pack(pady=15)
        self.smartscan_label = tk.Label(master=self.smart_scan_frame,text="Smart Scan",font=('Helvetica neue', 10, 'bold'),fg='#A9A9A9')
        self.smartscan_label.pack()
        self.smart_server_label = tk.Label(master=self.smart_scan_frame,text='SMART SCAN SERVER: ')
        self.smart_server_label.pack()
        self.smart_status_label = tk.Label(master=self.smart_scan_frame, text='CONNECTION: ')
        self.smart_status_label.pack()

        self.server_ip_entry.insert(0, self.server_ip)
        self.connection_status_label.pack()


    def testConnection(self):
        """function to test ping,telnet and cgi from agent to server"""
        # ping test
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '1', self.server_ip_entry.get()]

        if (subprocess.call(command) == 0) == True:
            self.ping_status_label['text'] = 'PING: OK'
            self.ping_status_label['fg'] = '#5cb85c'
        else:
            self.ping_status_label['text'] = 'PING: ERROR!'
            self.ping_status_label['fg'] = '#d9534f'

        # Telnet Test
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((socket.gethostbyname(self.server_ip_entry.get()), int(self.server_port_entry.get())))
        if result == 0:
            self.telnet_status_label['text'] = 'TELNET:OK'
            self.telnet_status_label['fg'] = '#5cb85c'
        else:
            self.telnet_status_label['text'] = 'TELNET: ERROR!'
            self.telnet_status_label['fg'] = '#d9534f'
        sock.close()

        #CGI Test
        url = 'https://' + self.server_ip_entry.get() + ':' + self.server_port_entry.get() + '/officescan/cgi/cgionstart.exe'
        try:
            x = requests.get(url, verify=False)
            if '-2' in x.text:
                self.connection_status_label['text'] = 'CGI: OK'
                self.connection_status_label['fg'] = '#5cb85c'
        except:
            self.cgi_status_label['text'] = 'CGI: ERROR!'
            self.cgi_status_label['fg'] = '#d9534f'

    def testSmartScan(self):
        akey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                              "SOFTWARE\\Wow6432Node\\TrendMicro\\PC-cillinNtCorp\\CurrentVersion\iCRC Scan\Scan Server")
        smart_scan_server = str(winreg.QueryValueEx(akey, 'LocalScanServerAddress')[0])
        smart_scan_url = str(winreg.QueryValueEx(akey, 'LocalScanServerUrl')[0])
        winreg.CloseKey(akey)

        url = smart_scan_url + '/?LCRC=08000000AC41080092000080C4F01936B21D9104'
        self.smart_server_label['text']='SMART SCAN SERVER:' + smart_scan_server

        try:
            x = requests.get(url, verify=False)
            if x.headers['Content-Type'] == 'binary/octet-stream':
                self.smart_status_label['text'] = 'CONNECTION: OK!'
                self.smart_status_label['fg'] = '#5cb85c'
            else:
                self.smart_status_label['text'] = 'CONNECTION:ERROR!'
                self.smart_status_label['fg'] = '#d9534f'
        except:
            self.smart_status_label['text'] = 'CONNECTION:ERROR!'
            self.smart_status_label['text'] = 'CONNECTION:ERROR!'
            self.smart_status_label['fg'] = '#d9534f'

    # def testPorts(self):
    #     server_port_list = [80, 8080, int(self.server_port_entry.get())]
    #     closed_server_ports = ''
    #     connect_server = True
    #
    #     try:
    #         for port in server_port_list:
    #             sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #             result = sock.connect_ex((socket.gethostbyname(self.server_ip_entry.get()), port))
    #             if result == 0:
    #                 print("Port: " + str(port) + " open")
    #             else:
    #                 closed_server_ports = str(port) + '\n'
    #             sock.close()
    #
    #     except socket.gaierror:
    #         connect_server = False
    #
    #     if closed_server_ports == '' and connect_server:
    #         self.server_ports_label['text'] = 'Server Ports:All Open'
    #     elif closed_server_ports != '' and connect_server:
    #         self.server_ports_label['text'] = 'Server Ports Closed:' + closed_server_ports
    #     else:
    #         self.server_ports_label['text'] = 'Server Ports:Unable to reach Server'
    #
    #     try:
    #         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #         result = sock.connect_ex((socket.gethostbyname('127.0.0.1'), int(self.agent_port)))
    #         if result == 0:
    #             self.agent_ports_label['text'] = 'Agent Port: Open'
    #         else:
    #             self.agent_ports_label['text'] = 'Agent Port(' + self.agent_port + '): Closed'
    #         sock.close()
    #
    #     except:
    #         print('error on agent side')

if __name__ == '__main__':
    akey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                          "SOFTWARE\\Wow6432Node\\TrendMicro\\PC-cillinNtCorp\\CurrentVersion")
    initial_server = str(winreg.QueryValueEx(akey, 'Server')[0])
    initial_port = str(winreg.QueryValueEx(akey, 'ServerSSLPort')[0])
    initial_agent_port = str(winreg.QueryValueEx(akey, 'LocalServerPort')[0])
    winreg.CloseKey(akey)

    root = tk.Tk()
    Window = Window(master=root, server_ip=initial_server, server_port=initial_port, agent_port=initial_agent_port)
    root.title("Agent Test Connection")
    root.geometry('400x600')
    root.mainloop()
