import Adafruit_DHT
import time
from cryptography.fernet import Fernet

import jpysocket
import socket

DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4

s = socket.socket()
print("Socket successfully created")

port = 4501

s.bind(('', port))
print("socket binded to %s" % (port))

s.listen(5)
print("socket is listening")

c, addr = s.accept()

print("Got connection from", addr)

msgsend = jpysocket.jpyencode("Thank You For Connecting.")
c.send(msgsend)

key = Fernet.generate_key()  # store in a secure location
print("Key:", key.decode())
f = Fernet(key)


while True:

    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)

    if humidity is not None and temperature is not None:
        ourString = (str(temperature) + "C").encode('utf_8')
        encrypted_data = f.encrypt(ourString)
        decrypted_data = f.decrypt(encrypted_data)
        # tmp = jpysocket.jpyencode(encrypted_data)
        tmp = encrypted_data
        tmpD = decrypted_data
        print(tmp)
        print(tmpD)
        # c.send(tmp)
        # hum = jpysocket.jpyencode("% s" % humidity + "%")
        # c.send(Fernet.encrypt(hum))
        # c.send(jpysocket.jpyencode("-----------"))
        time.sleep(0.5)

    else:
        c.send(jpysocket.jpyencode("Sensor failure"))
        time.sleep(0.5)