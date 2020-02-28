import socket
import threading
import json
import re

systems = [[{"sys_id": "sample system","project_name": "sample project", "gen_reached": 0, "max_wr": 24.4,
            "processor_usage": 76.12}, False]]
sys_id_lookup = {"sample_system": 0}


def send_and_print(message, comSocket):
   """
   :param message: string to both print to screen and send over a socket
   :param comSocket: socket for yeeting message down
   :return: 1 if execute correctly
   """
   print(message)
   message = message+"\n"
   comSocket.send(message.encode())
   return 1


def est_tcp_server(ipAddress="0.0.0.0", port=1337, threadFunction=None):
   """
   establishes a TCP listening server on the ipAddress and port passed in.
   When a connection is made, calls function passed in
       :param ipAddress: IP address to connect to as string. Default 0.0.0.0; this means listen on any.
       :param port: port to connect to as integer
       :param threadFunction: function to handle incoming connections in new thread sas function
   """

   TCP_socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   TCP_socket_server.bind((ipAddress, port))
   TCP_socket_server.listen(10)

   print("server online")
   while True:
       conn, addr = TCP_socket_server.accept()

       thread = threading.Thread(target=threadFunction, args=(conn, addr))
       thread.start()

   TCP_socket_server.close()
   return 0


def handler_v2(conn, addr):
   """
   Handles incoming connections. Should be started in new thread.
       :param conn: socket connection
       :param addr: socket address
       :return: 1 if executes successfully
   """

   print("handling inbound connection from %s" % str(addr))

   requestType = send_and_receive("connection approved; request type? \n", conn)

   if not requestType:
       return

   if re.match("^POST.*", requestType):
       recv_data(conn)
   elif re.match("^GET.*", requestType):
       get_handler(re.split("_", requestType)[-1], conn)       # passes on the section of the request after GET_
   else:
       send_and_print("1 - illegal connection type", conn)
       conn.close()
       return 0

   return 1


def handler(conn):
   """
   Handles incoming connections. Should be started in new thread.
       :param conn: socket connection
       :return: 1 if executes successfully
       """

   print("handling inbound connection")

   conn.send("connection approved \n".encode())
   conn.send("request type? \n".encode())
   requestType = conn.recv(1024)

   if requestType == "POST":
       recv_data(conn)
   elif requestType == "GET":
       GETtype = send_and_receive("GET_type?\n", conn)
       if GETtype == "sysids":
           send_sys_ids(conn)
       elif GETtype == "sysdata":
           send_sys_data(conn)
   else:
       conn.send("illegal connection type\n".encode())
       conn.close()

   return 0


def get_handler(type=None, conn=None):
   """
   :param type: the type of get request. Split off of initial request using REGEX
   :param conn: same as before; socket
   :return: 1 if execute successfully
   """

   if not conn and type:
       return

   type = str(type)

   if type == "sysids":
       send_sys_ids(conn)
   if type == "data":
       send_sys_data(conn)
   else:
       #print(type)
       #print(isinstance(type, str))
       send_and_print("2 - illegal connection type", conn)
       conn.close()
       return None

   return None


def send_sys_ids(conn=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)):
   """
   sends JSON list of all sys_ids currently stored on server
   :param conn: socket connection
   :return: 1 if executes successfully
   """

   sys_ids = []
   for system in systems:
       sys_ids.append(system[0]["sys_id"])

   data = json.dumps(sys_ids)
   conn.send(data)
   conn.close()


def send_sys_data(conn):
   """
   Sends JSON containing all data on given system
   :param conn: socket connection
   :return: 1 if executes successfully
   """
   sys_id = send_and_receive("sys_id?\n")
   if not sys_id:
       send_and_print("invalid sys_id entered", conn)
       conn.close()
   sys_index = get_index(sys_id)
   sys_data_raw = systems[sys_index]

   return 0


def send_and_receive(message="", comSocket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)):
   """
   sends a message to given socket and returns response
   :param message to send as string
   :param comSocket socket connection over which to communicate
   """
   comSocket.send(message.encode())
   comSocket.settimeout(8)
   try:
       data = comSocket.recv(2048)
   except socket.timeout:
       comSocket.send("Station took too long to reply \n".encode())
       return None
   return data.decode()


def get_json(message="", comSocket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)):
   """ sends a message to given socket and returns response
       :param message to send as string
       :param comSocket """
   comSocket.send(message.encode())
   comSocket.settimeout(8)
   try:
       data = comSocket.recv(1024)
   except socket.timeout:
       comSocket.send("Station took too long to reply \n".encode())
       comSocket.close()
       return -1

   try:
       json_data = json.loads(data)
   except StopIteration as err:
       comSocket.send("Station took too long to reply \n".encode())
       print("file received not JSON")
       return None

   return json_data


def recv_data(conn):
   """
   Receives data from incoming connection and passes to update_records function
   :param conn: socket connection
   :return: 1 if executes successfully
   """

   json_data = get_json("send JSON of sys_data \n", conn)
   if not json_data:
       print("No data sent. ")
       return

   try:
       new_data = json.loads(json_data)
   except ValueError:
       send_and_print("file sent not a JSON", conn)
       send_and_print("connection terminated", conn)
       conn.close()

   update_records(new_data)
   return


def get_index(sys_id):
   if sys_id in sys_id_lookup:
       index = sys_id_lookup[sys_id]
   else:
       try:
           index = max(sys_id_lookup.values())
       except IndexError:
           index = 0
       sys_id_lookup[sys_id] = index

   return index


def update_records(data):
   index = get_index(data["sys_id"])
   systems[index] = data

   return


if __name__ == "__main__":
   est_tcp_server("0.0.0.0", 1337, handler_v2)
