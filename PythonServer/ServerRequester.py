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

        self.p1 = None
        self.p2 = None

        self.fps = 6

    def setStatus(self, box, trigger, fps):

        if self.triggered is None:
            self.triggered = trigger
            self.num_frame = 0
            self.p1 = box[0]
            self.p2 = box[1]

        self.num_frame += 1

        if self.num_frame > self.fps/2:
            if self.triggered == 'play':
                self.requester(self.triggered)
            elif self.triggered == 'pause':
                self.requester(self.triggered)
            elif self.triggered == 'next' and trigger == 'previous':
                self.requester('next')
            elif self.triggered == 'previous' and trigger == 'next':
                self.requester('previous')
            elif self.triggered == 'mute':
                if self.p1[0] - box[0][0] > self.width/3:
                    self.requester('unmute')
                elif box[0][0] - self.p1[0] > self.width/3:
                    self.requester('mute')

        if self.num_frame == self.fps:
            self.triggered = None
            self.num_frame = 0


    def requester(self, cmd):
        self.triggered = None
        self.num_frame = 0

        try:
            print("send " + cmd + " to webServer")
            data = {'msg': cmd}
            r = requests.post(self.url, data=json.dumps(data), headers=self.headers, timeout=0.1)
            print(r)
        except Exception as e:
            pass