class GameServer:
    import socketio


import eventlet

# 서버의 IP 주소와 포트를 설정합니다.
SERVER_IP = '127.0.0.1'
SERVER_PORT = 10000  # ~12000

# 서버 객체 생성.
server = socketio.Server()

# 연결된 플레이어들의 정보를 저장할 변수.
players = {}


# 클라이언트(sid)가 연결되었을 때 호출되는 이벤트 핸들러
@server.on('connect')
def connect(sid, environ):
    print('Player connected:', sid)
    # 새로운 플레이어가 연결됨을 알리는 메시지를 모든 연결된 플레이어에게 브로드캐스팅
    # server.emit('player_connect', {'player_id': sid})


# 클라이언트와의 연결이 끊겼을 때 호출되는 이벤트 핸들러
@server.on('disconnect')
def disconnect(sid):
    print('Player disconnected:', sid)
    # 플레이어가 연결을 끊었음을 알리는 메시지를 모든 연결된 플레이어에게 브로드캐스팅
    # server.emit('disconnect', {'player_id': sid})


# 클라이언트에게 timer 넘겨줌
def timer(data):
    server.emit('timer', data)


# player수 모든 클라이언트에게 넘겨줌
def playerNum(data):
    server.emit('num', data)


# 클라이언트한테 받은 cardNum 모든 클라이언트에게 전달
@server.on('cardNum')
def cardNum(sid, data):
    print(sid, ':', data)
    server.emit('cardNum', {'player_id': sid, 'data': data})


# draw를 요청한 해당 클라이언트한테만 event 처리
@server.on('draw')
def handle_draw(sid, data):
    # deck에서 pop 하기
    server.emit('draw', data, room=sid)  # 해당 결과 요청한 client에게 전달


# client가 요청한 animation 처리
@server.on('animation')
def handle_animation(sid, data):  # 해당 sid를 가진 client가 요청
    # 요청한 동작에 대한 animation 처리
    server.emit('animation', data)  # 그 결과 모든 client에게 전달


# client가 요청한 현재카드 바꾸기
@server.on('pay')
def handle_currentCard(sid, data):  # 해당 sid를 가진 client가 요청
    # currentCard가 바꾸는 동작
    server.emit('pay', data)  # 바꾼 카드 모든 client에게 전달


@server.on('color')
def handle_currentColor(sid, data):
    # currentColor가 바꾸는 동작
    server.emit('color', data)  # 바꾼 색상 모든 client에게 전달


# 서버를 시작하는 메인 함수
if __name__ == '__main__':
    app = socketio.WSGIApp(server)
    eventlet.wsgi.server(eventlet.listen((SERVER_IP, SERVER_PORT)), app)

