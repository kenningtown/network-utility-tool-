import socket, threading
import subprocess
from  ftplib import FTP
import requests

#from dns_tool import server, udp_server, client, udp_client, process_dns, http_get, ftp_connect
#from network_trace import trcpath, trcrouting

import tkinter as tk
from tkinter import simpledialog, messagebox

import socket
import threading
#-------------------------------------------------------------------------


def process_dns(dom, dns_com):
    res = ""
    if dns_com == "nslookup" or  dns_com == "host" or dns_com == "dig":
        res = f"{dns_com} {dom}"

    if not res:
        print("Invalid input!")
    else:
        processing = subprocess.run(res, shell=True, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return processing.stdout



def http_get(link):
    info = requests.get(link)
    content = info.headers.get('Content-Type')
    response = f"Status: {info.status_code}\nType of content: {content}\n"

    if 'application/json' in content:

        json_cont = str(info.json())
        return response + "Response:\n" + json_cont
    else:
        return response + info.text[0:700]


def ftp_connect(serv, prt, usr, pswd):
    try:
        ftp = FTP()
        ftp.connect(serv, prt)
        ftp.login(usr, pswd)
        ftp.quit()
        return f"Successfully connected to {serv}!"
    except Exception as ex:
        return f"Failed to connect! {ex}"


def trcrouting(dm):
    res = ['traceroute', dm]
    try:
        process = subprocess.run(res, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        return process.stdout
    except Exception as ex:
        return f"Invalid response: {ex}"



def trcpath(domen):
    res = ['tracepath', domen]
    try:
        process = subprocess.run(res, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        return process.stdout
    except Exception as ex:
        return f"Invalid response: {ex}"


def server(prt):
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('localhost', prt))
        server_socket.listen()
        client_socket, addr = server_socket.accept()
        info = client_socket.recv(1024).decode()
        client_socket.sendall("message is received.".encode())
        client_socket.close()
        return f"Server: accepted connection from {addr}, received message '{info}'"
    except Exception as e:
        return f"Server error: {e}"


def client(prt, message):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', prt))
        client_socket.sendall(message.encode())
        info = client_socket.recv(1024).decode()
        client_socket.close()
        return f"Client received a response: {info}"
    except Exception as e:
        return f"Client error: {e}"

def udp_server(port):
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind(('localhost', port))
        info, addr = server_socket.recvfrom(1024).decode()
        server_socket.sendto("UDP message received.".encode(), addr)
        return f"UDP Server: received message '{info}' from {addr}"
    except Exception as e:
        return f"UDP Server error: {e}"


def udp_client(port, msg):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.sendto(msg.encode(), ('localhost', port))
        info_back, a = client_socket.recvfrom(1024).decode()
        return f"UDP Client received a response: {info_back}"
    except Exception as e:
        return f"UDP Client error: {e}"



#-----------------------------------------------------------------------------

class NetworkUtilityApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Network Utility")
        self.geometry("400x300")
        self.configure(bg='#87CEEB')
        self.create_widgets()

    def create_widgets(self):
        tk.Button(self, text="DNS Lookup", command=self.dns_lookup).pack(pady=10)
        tk.Button(self, text="Traceroute", command=self.traceroute).pack(pady=10)
        tk.Button(self, text="HTTP GET Request", command=self.http_get_request).pack(pady=10)
        tk.Button(self, text="FTP Connect", command=self.ftp_connect).pack(pady=10)
        tk.Button(self, text="TCP/UDP Socket Communication", command=self.socket_com).pack(pady=10)
        tk.Button(self, text="Exit", command=self.destroy).pack(pady=10)

    def dns_lookup(self):
        domain = simpledialog.askstring("DNS Lookup", "Enter domain:")
        command = simpledialog.askstring("DNS Lookup", "Choose command (nslookup, host, dig):")
        result = process_dns(domain, command)
        messagebox.showinfo("DNS Lookup Result", result)

    def http_get_request(self):
        url = simpledialog.askstring("HTTP GET Request", "Enter URL:")
        response = http_get(url)  
        messagebox.showinfo("HTTP GET Response", response)

    def ftp_connect(self):
        server = simpledialog.askstring("FTP Connect", "Server to connect:")
        port = simpledialog.askinteger("FTP Connect", "Port:")
        username = simpledialog.askstring("FTP Connect", "Username:")
        password = simpledialog.askstring("FTP Connect", "Password:")
        response = ftp_connect(server, port, username, password)  
        messagebox.showinfo("FTP Connect Response", response)

    def traceroute(self):
        domain = simpledialog.askstring("Traceroute", "Enter address to trace:")
        traceroute_result = trcrouting(domain) 
        tracepath_result = trcpath(domain)  
        combined_result = f"Traceroute Result:\n{traceroute_result}\n\nTracepath Result:\n{tracepath_result}"
        messagebox.showinfo("Network Trace Results", combined_result)
    

    def socket_com(self):
        msg = simpledialog.askstring("Socket Communication", "Enter message to send to the server:")
        port = simpledialog.askinteger("Socket Communication", "Enter the port number:")
        socket_type = simpledialog.askstring("Socket Communication", "Enter socket type (tcp/udp):").lower()
        responses = []

        def tcp_communication():
            responses.append(client(port, msg))

        def udp_communication():
            responses.append(udp_client(port, msg))

        if socket_type == 'tcp':
            s_thread = threading.Thread(target=server, args=(port,))
            s_thread.start()
            cl_thread = threading.Thread(target=tcp_communication)
            cl_thread.start()
            s_thread.join()
            cl_thread.join()
        elif socket_type == 'udp':
            udp_s_thread = threading.Thread(target=udp_server, args=(port,))
            udp_s_thread.start()
            udp_cl_thread = threading.Thread(target=udp_communication)
            udp_cl_thread.start()
            udp_s_thread.join()
            udp_cl_thread.join()
        else:
            messagebox.showerror("Error", "Invalid socket type selected. Please choose tcp or udp.")
            return


        response_message = "\n".join(responses)
        messagebox.showinfo("Response", response_message)


if __name__ == "__main__":
    app = NetworkUtilityApp()
    app.mainloop()
    