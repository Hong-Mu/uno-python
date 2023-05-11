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

# 서버에 연결하는 함수입니다.
def connect_to_server():
    client.connect(server_url)
    print('서버에 연결되었습니다!')

# 서버와의 연결을 끊는 함수입니다.
def disconnect_from_server():
    client.disconnect()
    print('서버와의 연결이 끊어졌습니다.')


#TODO 타이머, 플레이어수는 서버에서 클라이언트에 바로 정보 공유하는걸로 구현, test 못함

# 서버로부터 timer정보 받아서 처리
@client.on('timer')
def timer(data):
    print(data)

# 서버로부터 player수 받아서 처리
@client.on('playerNum')
def playetrNum(data):
    print(data)

# 서버에 해당 player의 카드 갯수 보내기
def send_cardNum(data):
    client.emit('cardNum', data)

# 서버에서 모든 클라이언트에게 전달한 cardNum 처리
@client.on('cardNum')
def handle_cardNum(data):
    print(data)

# client가 server에 draw 요청
def draw(data):
    client.emit('draw', data)

# server가 처리해준 draw, client가 처리
@client.on('draw')
def handle_draw(data):
    print("draw되었습니다.") #해당 client hands에 1장 추가

# client가 server에 animation 요청
def animation(data):
    client.emit('animation', data)

# server가 처리해준 animation, client가 처리
@client.on('animation')
def handle_animation(data):
    print("animate 되었습니다.")

# client가 카드를 내서 현재카드 바뀌는걸 요청
def currentCard(data):
    client.emit("pay", data)

# server가 바꾼 카드를 반영
@client.on('pay')
def handle_currentCard(data):
    print('현재카드 바뀜.')

# server가 바꾼 카드를 반영
@client.on('pay')
def handle_currentCard(data):
    print('현재카드 바뀜.')

# client가 바꾼 색상 전달
def currentColor(data):
    client.emit("color", data)

@client.on('color')
def handle_currentColor(data):
    print('현재색상 바뀜.')

# 서버에 연결하는 메인 함수
if __name__ == '__main__':
    client.connect(server_url)
    currentColor('blue')