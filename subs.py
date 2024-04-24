import random
import time
from paho.mqtt import client as mqtt_client

### CONFIG ###
broker = 'broker.emqx.io'
port = 1883
topic = "SMTOWN"
client_id = ""
username = 'admin'
password = 'public'
subs = []

def connect_mqtt(client: mqtt_client):
    ### CONNECT SUBSCRIBER TO BROKER ###
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!\n")
        else:
            print("Failed to connect, return code %d\n", rc)

    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)

def on_message(client, userdata, msg):
    ### GET MESSAGE FROM PUBLISHER ###
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

def subscribe_menu(client):
    ###  CHOSE TO SUBSCRIBE/UNSUBSCRIBE TOPIC ###
    SM = "SMTOWN"
    YG = "YG Entertaiment"
    print(f"sekarang sedang subscribe {subs}")
    print(f"subscribe/unsubscribe : \n 1 {SM} \n 2 {YG}")
    command = input()
    if command == str(1):
        #Jika sedang subscribe SM, jadi unsubscribe SM. Begitupun sebaliknya
        if SM in subs: 
            subs.pop(subs.index(SM))
            client.unsubscribe(SM)
        else:
            subs.append(SM)
            client.subscribe(SM)
    elif command == str(2):
        #Jika sedang subscribe YG, jadi unsubscribe YG. Begitupun sebaliknya
        if YG in subs:
            subs.pop(subs.index(YG))
            client.unsubscribe(YG)
        else:
            subs.append(YG)
            client.subscribe(YG)
    print(f"sekarang jadi subscribe {subs}")
    print()
    print()

def run():
    global client_id
    client_id = input("USERNAME : ")

    #Make Client
    client = mqtt_client.Client(client_id)

    #Connect client to broker
    connect_mqtt(client)

    #Start loop client
    client.loop_start()
    time.sleep(1)

    subscribe_menu(client)

    while True:
        client.on_message = on_message    
        inputs = input()
        if (inputs == "menu"):
            subscribe_menu(client)
        time.sleep(1)

    client.loop_stop()

if __name__ == '__main__':
    run()