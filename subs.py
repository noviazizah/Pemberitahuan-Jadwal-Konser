import time
from paho.mqtt import client as mqtt_client

# Configuration
broker = 'broker.emqx.io'
port = 1883
topic = "SMTOWN"
client_id = ""
username = 'admin'
password = 'public'
subs = []

def connect_mqtt(client: mqtt_client):
    # Connect Subscriber to Broker
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!\n")
        else:
            print("Failed to connect, return code %d\n", rc)

    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)

def on_message(client, userdata, message):
    #Receive Message from Publisher
        print(f"You got a message from {message.topic}\n{message.payload.decode()}")
        print("NOTE: Type `Menu` to show Menu\n")

def subscribe_menu(client):
    # Subscriber Menu
    SM = "SMTOWN"
    YG = "YG Entertaiment"
    header()
    print(f"Hi, {client_id}!")
    print(f"Now subscribed {subs}\n")
    print(f"Subscribe / Unsubscribe your favorite agency: \n 1 {SM} \n 2 {YG} \n\n 0 Exit \n")
    time.sleep(2)
    command = input("Choose: ")
    if command == str(1):
        # When subscribe SM, then unsubscribe SM
        if SM in subs: 
            subs.pop(subs.index(SM))
            client.unsubscribe(SM)
            print(f"Unsubscribe to {SM} successful!")
        # When not subscribe SM, then subscribe SM
        else:
            subs.append(SM)
            client.subscribe(SM)
            print(f"Subscribe to {SM} successful!")
    elif command == str(2):
        # When subscribe YG, then unsubscribe YG
        if YG in subs:
            subs.pop(subs.index(YG))
            client.unsubscribe(YG)
            print(f"Unsubscribe to {YG} successful!")
        # When not subscribe YG, then subscribe YG
        else:
            subs.append(YG)
            client.subscribe(YG)
            print(f"Subscribe to {YG} successful!")
    elif command == str(0):
        # Exit
        header()
        print("Thank you for hyping with us <3")
        exit()
    print(f"Now subscribed {subs}")
    print("NOTE: Type `menu` to show Menu\n")

def run():
    global client_id
    header()
    print("Hi, K-POP fan!\n")
    client_id = input("Please enter username: ")
    client = mqtt_client.Client(client_id)
    connect_mqtt(client)
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

def header():
    print("\n===============================\n")
    print("      CONCERT HYPE TUNNEL      \n")
    print("===============================\n")

if __name__ == '__main__':
    run()