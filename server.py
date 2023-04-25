import socketio
import eventlet

# 서버의 IP 주소와 포트를 설정합니다.
SERVER_IP = '127.0.0.1'
SERVER_PORT = 10000 # ~12000

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

# 클라이언트가 전송한 메시지를 다른 클라이언트에게 브로드캐스팅하는 이벤트 핸들러
@server.on('message')
def message(sid, data):
    print('Message received from player', sid, ':', data)
    server.emit('message', data)
    # 모든 연결된 플레이어에게 메시지를 브로드캐스팅
    # server.emit('message', {'player_id': sid, 'data': data})

# 클라이언트와의 연결이 끊겼을 때 호출되는 이벤트 핸들러
@server.on('disconnect')
def disconnect(sid):
    print('Player disconnected:', sid)
    # 플레이어가 연결을 끊었음을 알리는 메시지를 모든 연결된 플레이어에게 브로드캐스팅
    # server.emit('player_disconnect', {'player_id': sid})

# 서버를 시작하는 메인 함수
if __name__ == '__main__':
    app = socketio.WSGIApp(server)
    eventlet.wsgi.server(eventlet.listen((SERVER_IP, SERVER_PORT)), app)