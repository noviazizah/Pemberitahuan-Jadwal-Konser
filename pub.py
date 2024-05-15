import random
import time
import datetime

from paho.mqtt import client as mqtt_client

# Configuration
broker = 'broker.emqx.io'
port = 1883
topic = ""
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'admin'
password = 'public'

def connect_mqtt():
	# Connect publisher to broker
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client):
    command = 1
    while (command != 0):
    	# Publisher Menu
            header()
            print(f"Welcome {topic}! Choose the menu:")
            print("\n 1 Publish Message \n\n 0 Exit \n")
            time.sleep(2)
            command = input("Choose: ")
            if command == str(0):
                # Exit
                header()
                print("Thank you for hyping with us <3")
                exit()
            if command == str(1):
                # Input Message
                header()
                concert_name = input("Enter Concert Name: ")
                date_input = input("Enter Date (YYYY/MM/DD): ")
                time_input = input("Enter Time (HH:MM): ")
                schedule_input = date_input + " - " + time_input
                schedule = datetime.datetime.strptime(schedule_input, "%Y/%m/%d - %H:%M")
                message = f"\n{concert_name}\n{schedule}"
                
                # Publish Message to Broker
                result = client.publish(topic, message)
                status = result[0]
                if status == 0:
                    print(f"\nMessage:{message}")
                    print(f"Message has been sent to {topic} subscriber!")
                else:
                    print(f"Failed to send message to topic {topic} subscriber")
                print ()

                client.loop_start()
                client.loop_stop()

def agency():
	# Start Menu
	global topic
	SM = "SMTOWN"
	YG = "YG Entertaiment"
	header()
	print("Welcome agency! Choose the agency:")
	print(f"\n 1 {SM} \n 2 {YG} \n")
	command = input("Choose: ")
	if command == str(1):
		topic = SM
	elif command == str(2):
		topic = YG

def run():
	global topic 
	agency()
	print (topic)
	client = connect_mqtt()
	client.loop_start()
	publish(client)

def header():
    print("\n===============================\n")
    print("      CONCERT HYPE TUNNEL      \n")
    print("===============================\n")

if __name__ == '__main__':
    run()