import tornado.ioloop
import tornado.web
from tornado.httpclient import HTTPClient, HTTPRequest
import sys
import json
import importlib
import os
import threading
import traceback
from time import sleep

import player
from game import GameState

running = True

def monitor_changes(port):
    last_write_time = os.path.getmtime('player.py')

    while running:
        current_write_time = os.path.getmtime('player.py')
        if last_write_time != current_write_time:
            last_write_time = current_write_time
            print ('Change detected')
            importlib.reload(player)
            register_player(port)

        sleep(1)

    print('Stopping')

class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.handle_method('GET')

    def post(self):
        self.handle_method('POST')

    def get_payload(self):
        
        payload_len = int(self.request.headers.get('content-length', 0))
        if payload_len == 0:
            return None
        return tornado.escape.json_decode(self.request.body)

    def handle_method(self, method):
        try:
            if method == 'GET':
                self.set_status(200)
                self.write('Please send POST with game data\n'.encode())
            else:
                payload = self.get_payload()
                response = ''
                if self.request.path == '/end':
                    player.game_end()
                else:    
                    actions = player.get_actions(GameState(payload))
                    response = json.dumps(list(map(lambda a : a.__dict__, actions)), sort_keys=True, indent=2).encode()
                self.set_status(200)
                self.set_header('Content-Type', 'application/json')
                self.write(response)
                self.finish()

        except Exception as e:
            print(e)
            print(traceback.format_exc())
            self.set_status(500)
            self.write('An error occured')


poll_interval = 0.1

def make_app():
    return tornado.web.Application([
        (r"/.*", MainHandler),
    ])


def start_server(port):
    print('Starting HTTP server at port %d' % port)
    app = make_app()
    app.listen(port, address="0.0.0.0")  # explicit: listen on all interfaces
    try:
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        pass



def register_player(port):
    info = player.get_player_info()

    # Where EvG is reachable FROM WINDOWS (this script runs on Windows)
    evg_base = os.environ.get("EVG_SERVER", "http://127.0.0.1:5000")
    evg_url = evg_base.rstrip("/") + "/api/players"

    # The callback address EvG should use to reach THIS bot.
    # Set this to an IP that the EvG container can reach.
    public_host = os.environ.get("PLAYER_HOST", "10.255.255.254")
    info["address"] = f"http://{public_host}:{port}"

    http_client = HTTPClient()
    http_client.fetch(
        HTTPRequest(
            evg_url,
            method="POST",
            headers={'Content-Type': 'application/json'},
            body=json.dumps(info, sort_keys=True, indent=2).encode()
        )
    )

def safe_register(port):
    try:
        register_player(port)
        print("Registered player OK")
    except Exception as e:
        print(f"register_player failed (continuing): {e}")

def monitor_changes(port):
    last_write_time = os.path.getmtime('player.py')
    while running:
        current_write_time = os.path.getmtime('player.py')
        if last_write_time != current_write_time:
            last_write_time = current_write_time
            print('Change detected')
            importlib.reload(player)
            #safe_register(port)
        sleep(1)
    print('Stopping')

if __name__ == '__main__':
    port = 9080
    #safe_register(port)  # <— no longer fatal
    monitor = threading.Thread(target=monitor_changes, args=(port,))
    monitor.start()
    start_server(port)
    running = False
    monitor.join()

