# Client setup using UDP

import socket
import argparse
import sys
from select import select


def setup_client(server_ip, port_num, log_file, my_name):
    BUFFER_SIZE = 1024
    timeout = 10

    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print my_name + " connecting to the server: " + server_ip + " at port: " + str(port_num)

    client_file = open(log_file, 'w')
    client_file.write("connecting to the server " + socket.gethostbyname(socket.gethostname()) + " at port " +
                      str(port_num))
    client_file.write("\nsending register message " + my_name)
    address = (server_ip, port_num)
    sock.settimeout(5)
    try:
        sock.sendto("testing-" + my_name, address)
        (message, address) = sock.recvfrom(BUFFER_SIZE)
    except socket.error:
        print "Could not connect to server..."
    else:
        print "connected to server and registered"
        client_file.write("\nreceived welcome")
        print "waiting for messages..."
        #sock.settimeout(None)
        while True:
            #user_input = raw_input("your message: ")
            #print "Your message: ",
            rlist, _, _ = select([sys.stdin], [], [], timeout)
            if rlist:
                s = sys.stdin.readline()
                s = s.strip()
                if s == "exit":
                    break
                sock.sendto(s, address)
                #client_file.write("\n" + s)

            #else:
                #print "No input. Moving on..."
            # if user_input == "exit":
            #     break
            # sock.sendto(user_input, address)
            try:
                (message, address) = sock.recvfrom(BUFFER_SIZE)
                if message:
                    client_file.write("\n" + message)
                    server_response = "DEBUG -- Client: " + message + " --From server: " + str(address[0]) + ":" + str(address[1])
                    print server_response
            except socket.error:
                pass

    print "exit"
    client_file.write("\nterminating client...")
    client_file.close()
    sock.close()


def read_command_lines():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "-IP", help="server IP address", required=True)
    parser.add_argument("-p", "-port", type=int, help="port num", required=True)
    parser.add_argument("-l", "-log", help="log file", required=True)
    parser.add_argument("-n", "-name", help="client name", required=True)
    args = parser.parse_args()
    return (args.s, args.p, args.l, args.n)


(ip_address, port_number, log_name, client_name) = read_command_lines()
setup_client(ip_address, port_number, log_name, client_name)
