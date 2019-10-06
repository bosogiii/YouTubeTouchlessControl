import requests
import json

class ServerRequester:
    def __init__(self, width, height):
        self.url = "http://localhost:3000/gesture"
        self.headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

        self.isPlayed = False
        self.triggered = None
        self.num_frame = 0
        self.width = width
        self.height = height

        self.fps = 10

    def getStatus(self, box, trigger):
        if trigger == 'garbage':
            return

        if trigger != self.triggered:
            self.triggered = trigger
            self.num_frame = 0
            return
        else:
            self.triggered = trigger

        self.num_frame += 1

        if self.num_frame == self.fps:
            self.requester(self.triggered)


    def requester(self, cmd):
        try:
            print("send " + cmd + " to webServer")
            data = {'msg': cmd}
            r = requests.post(self.url, data=json.dumps(data), headers=self.headers, timeout=1)
        except Exception as e:
            pass