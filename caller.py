import random
import threading
from torpy.http.requests import TorRequests
import requests

url = "http://20.79.211.11/hash/"


def tor():
    randomValue = random.randrange(2354232343, 235235235423523234)

    with TorRequests() as tor_requests:
        try:
            with tor_requests.get_session() as sess:

                response = sess.get(url+str(randomValue))
                print(response.text)
        except:
            print("Tor error")


i = 0
while i < 1000:
    # x = threading.Thread(target=withoutTor, args=())
    # x.start()

    tor()
    i = i+1

tor()
