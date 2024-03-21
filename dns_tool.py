import subprocess
from  ftplib import FTP
import requests
import socket
import threading
#https://vk.com/im

def server(prt):                   #TCP server function

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', prt))
    server_socket.listen()
    print(f"Server: listening ....")

    client_socket, addr = server_socket.accept()
    print(f"Server: accepted connection from {addr}")

    info = client_socket.recv(1024)
    print(f"Server: received client message  '{info.decode()}' ")

    client_socket.sendall("message is received.".encode())
    client_socket.close()


def client(prt, message):                #TCP client function

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', prt))

    client_socket.sendall(message.encode())

    info = client_socket.recv(1024)
    print(f"Client received a response:  {info.decode()}")

    client_socket.close()

    
def udp_server(port):                      #UDP server function
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('localhost', port))
    print(f"UDP Server: listening ....")

    info, addr = server_socket.recvfrom(1024)
    print(f"UDP Server: received message '{info.decode()}' from {addr}")

    server_socket.sendto("UDP message received.".encode(), addr)


 
def udp_client(port, msg):                      #UDP client function
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.sendto(msg.encode(), ('localhost', port))

    info_back, a = client_socket.recvfrom(1024)
    print(f"UDP Client received a response: {info_back.decode()}")

#-----------------------------------------------------------------------------------


def http_get(link):                                          #http GET request
    info = requests.get(link)                              #get method
    content = info.headers.get('Content-Type')
    print("Status: ", info.status_code)                     #status if the method worked succesfully
    print("Type of content: ", content)                    #checking whether the type is in json format, html or etc.

    if 'application/json' in content:
        print("Response:\n", info.json())
    else:
        print(info.text[0:700])                          #printing first 700 characters only if not json format


def ftp_connect(serv, prt, usr, pswd):                   #establishing connections with ftp servers
    try:
        ftp = FTP()
        ftp.connect(serv, prt)
        ftp.login(usr, pswd)                              #logging in with credentials
        print(f"Succesfully connected to {serv}!")
        ftp.quit()
    except Exception:
        print("Failed to connect!")

#-------------------------------------------------------------------------
        
def process_dns(dom, dns_com):
    res = ""
    if dns_com == "nslookup" or  dns_com == "host" or dns_com == "dig":                  #checking if the command is valid
        res = f"{dns_com} {dom}"

    if not res:
        print("Invalid input!")
    else:
        processing = subprocess.run(res, shell=True, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(processing.stdout) #printing the contents





if __name__ == "__main__":          #I decided to include them in main because It would be good to have a systemized menu
                                     #Here I am asking for the basic inputs to proceed with requests.
    print("1. DNS Lookup")
    print("2. HTTP GET Request")
    print("3. FTP Connect")
    print("4. TCP/UDP Socket Communication")
    choice = input("Choose an option: ")

    if choice == '1':
        domain = input("Enter domain: ")
        command = input("Choose command (nslookup, host, dig): ")
        process_dns(domain, command)

    elif choice == '2':
        url = input("Enter the URL: ")
        http_get(url)

    elif choice == '3':
        server = input("Which server to connect: ")
        port = int(input("Type the port: "))
        username = input("Your username: ")
        password = input("Enter the password: ")
        ftp_connect(server, port, username, password)
        
    elif choice == '4': #Here, I used threading to make socket work in one script, also here is the choice to do it in UCP or TCP.
        msg = input("Enter message to send to the server: ")
        port = 12345
        type = input("Which socket type do you choose: (tcp/udp)? ").lower()
        print("-----")

        if type == 'tcp':
            s_thread = threading.Thread(target=server, args=(port,))
            s_thread.start()

            cl_thread = threading.Thread(target=client, args=(port, msg))
            cl_thread.start()
            
            s_thread.join()
            cl_thread.join()

        elif type == 'udp':
            udp_s_thread = threading.Thread(target=udp_server, args=(port,))
            udp_s_thread.start()

            udp_cl_thread = threading.Thread(target=udp_client, args=(port, msg))
            udp_cl_thread.start()

            udp_s_thread.join()
            udp_cl_thread.join()