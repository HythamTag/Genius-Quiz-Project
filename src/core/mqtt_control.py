import time
import threading
from paho.mqtt import client as mqtt_client

class MqttServer:
    def __init__(self, client_id, topic, broker='localhost', port=1883, username=None, password=None):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.client_id = client_id
        self.username = username
        self.password = password
        self.client = None
        self.connected = False

    def connect_mqtt(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                self.connected = True
                print(f"✅ [{self.client_id}] Connected to MQTT Broker at {self.broker}:{self.port}")
            else:
                print(f"❌ [{self.client_id}] Connection failed with code {rc}")
                self.connected = False

        client = mqtt_client.Client(self.client_id)

        if self.username and self.password:
            client.username_pw_set(self.username, self.password)

        client.on_connect = on_connect

        try:
            print(f"Attempting to connect to {self.broker}:{self.port}")
            client.connect(self.broker, self.port, 60)  # Timeout of 60 seconds
            client.loop_start()  # Run the MQTT loop in a separate thread
            print("Started MQTT loop.")
        except Exception as e:
            print(f"⚠️ MQTT connection failed for [{self.client_id}]: {e}")

    def publish(self, message: str):
        if self.client is None or not self.connected:
            print(f"⚠️ Skipped publish: MQTT not connected for [{self.client_id}]")
            return

        time.sleep(0.1)
        result = self.client.publish(self.topic, message)
        status = result[0]
        if status == 0:
            print(f"📤 Published `{message}` to `{self.topic}`")
        else:
            print(f"❌ Failed to publish to `{self.topic}`")

    def run(self):
        # Run MQTT connection in a separate thread to not block the app
        threading.Thread(target=self.connect_mqtt, daemon=True).start()

# Optional test usage
if __name__ == '__main__':
    # Initialize the server with correct details
    server_R = MqttServer(client_id='Team-R1', topic='Red/R1', broker='localhost', port=1883)
    server_R.run()

    # Try publishing a test message (even if not connected)
    server_R.publish("Hello, even if not connected!")

    # Your application can continue running without waiting for MQTT connection
    # Continue with your PyQt6 application or any other functionality
    print("The application is running, MQTT connection is asynchronous.")
