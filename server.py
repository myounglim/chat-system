# Server setup using UDP sockets/TCP

import socket
import argparse


def server_run(sock, server_file):
    BUFFER_SIZE = 1024
    # host = ''
    #
    # # Create UDP socket
    # sock = socket.socket(socket.AF_INET,
    #                      socket.SOCK_DGRAM)
    #
    # sock.bind((host, port_num))
    # print "server started on " + socket.gethostbyname(socket.gethostname()) + " at port " + str(port_num) + "..."
    # server_file = open(log_file, 'w')
    # server_file.write("server started on " + socket.gethostbyname(socket.gethostname()) + " at port " +
    #                   str(port_num) + "...")

    client_dictionary = {}
    try:
        while True:
            (message, address) = sock.recvfrom(BUFFER_SIZE)
            if message == "exit":
                break
            if "testing-" in message:
                print message[8:] + " registered from host " + str(address[0]) + " port " + str(address[1])
                server_file.write("\nclient connection from host " + str(address[0]) + " port " + str(address[1]))
                server_file.write("\nreceived register " + message[8:] + " from host " + str(address[0]) +
                                  " port " + str(address[1]))
                sock.sendto(message, address)
                client_dictionary[message[8:]] = address
                continue
            if "sendto" in message:
                split_on_space = message.split()
                found_sender = False
                #print "Iterating over dictionary..."
                client_name = ""
                for key in client_dictionary:
                    client_port = client_dictionary[key][1]
                    #print "Client port is: " + str(client_port)
                    if client_port == address[1]:
                        client_name = key
                        #print "Client name is: " + client_name
                        server_file.write("\n" + message + " from " + client_name)
                        break

                for key in client_dictionary:
                    #print key, 'corresponds to', client_dictionary[key]
                    #if key in message:
                    if key == split_on_space[1]:
                        #print "Key: " + key + " in that key is stored: " + str(client_dictionary[key][0]) + ", " \
                              #+ str(client_dictionary[key][1])
                        sock.sendto("recvfrom " + client_name + " " + message[7 + len(key):], client_dictionary[key])
                        server_file.write("\nrecvfrom " + client_name + " " + message[7 + len(key):] + " to " + key)
                        found_sender = True
                if not found_sender:
                    server_file.write("\n" + split_on_space[1] + " not registered with server")

            client_response = "DEBUG -- Server: " + message + " From client: " + str(address[0]) + ":" + str(address[1])
            print client_response
            sock.sendto(message, address)

    except KeyboardInterrupt:
        print "terminating server..."
        server_file.write("\nterminating server...")
        server_file.close()
        sock.close()


def read_command_lines():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "-port", type=int, help="input port num", required=True)
    parser.add_argument("-l", "-log", help="log file name", required=True)
    args = parser.parse_args()
    return (args.p, args.l)


def server_setup(port_num, log_file):
    # Create UDP socket
    sock = socket.socket(socket.AF_INET,
                         socket.SOCK_DGRAM)

    sock.bind(('', port_num))
    print "server started on " + socket.gethostbyname(socket.gethostname()) + " at port " + str(port_num) + "..."
    server_file = open(log_file, 'w')
    server_file.write("server started on " + socket.gethostbyname(socket.gethostname()) + " at port " +
                      str(port_num) + "...")

    return sock, server_file


(port_number, log_name) = read_command_lines()
server_socket, server_file_name = server_setup(port_number, log_name)
server_run(server_socket, server_file_name)

