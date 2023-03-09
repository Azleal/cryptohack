#!/usr/bin/env python3
import base64
import codecs
import json
import socket

from Crypto.Util.number import long_to_bytes

HOST = 'socket.cryptohack.org'
PORT = 13377


def hack(data):
    data = json.loads(data)
    encoded = data['encoded']
    encoding = data['type']
    decoded = ''
    if encoding == "base64":
        decoded = base64.b64decode(encoded).decode()
    elif encoding == "hex":
        decoded = bytes.fromhex(encoded).decode()
    elif encoding == "rot13":
        decoded = codecs.decode(encoded, 'rot_13')
    elif encoding == "bigint":
        decoded = long_to_bytes(int(encoded, 16)).decode()
    elif encoding == "utf-8":
        decoded = ''.join([chr(b) for b in encoded])
    json_data = json.dumps({"decoded": decoded}, ensure_ascii=False).replace("'", '"')
    print(json_data)
    return json_data


def try_hack():
    # Connect to the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print('Connected to', HOST)

        count = 1
        while True:
            # Receive the welcome message
            data = s.recv(1024)
            print("接受响应:", data.decode())
            # Send a message to the server
            message = hack(data)
            print("解码内容:", message)
            # time.sleep(2)
            s.sendall(message.encode())
            print("发送解码内容完毕", count)
            count += 1


def manual_hack():
    while True:
        data = input()
        print("输入data", data)
        hack(data)


try_hack()
# manual_hack()
