#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 16:33:38 2023

@author: leegyeongrim
"""

import socketio

# 서버의 IP 주소와 포트를 설정합니다.
SERVER_IP = '127.0.0.1'
SERVER_PORT = 10000 # ~12000

# 서버 url 구성.
server_url = f'http://{SERVER_IP}:{SERVER_PORT}'

# 클라이언트 객체 생성.
client = socketio.Client()

# 서버로부터 이벤트를 수신하는 핸들러 함수입니다.
@client.on('message')
def handle_message(data):
    print('메시지를 수신했습니다:', data)
    
# 서버에 메시지를 전송하는 함수입니다.
def send_message(data):
    client.emit('message', data)

# 서버에 연결하는 함수입니다.
def connect_to_server():
    client.connect(server_url)
    print('서버에 연결되었습니다!')

# 서버와의 연결을 끊는 함수입니다.
def disconnect_from_server():
    client.disconnect()
    print('서버와의 연결이 끊어졌습니다.')
    
# 서버에 연결하는 메인 함수
if __name__ == '__main__':
    client.connect(server_url)