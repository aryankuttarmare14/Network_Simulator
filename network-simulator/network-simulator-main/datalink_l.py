import random
import time
import uuid

class EndDevice:
    def __init__(self, name):
        self.name = name

    def send(self, message, connection):
        print(f"{self.name} is sending the message: {message}")
        connection.transmit(self, message)

    def receive(self, message):
        print(f"{self.name} received the message: {message}")

class Hub:
    def __init__(self, name):
        self.name = name
        self.connections = []

    def connect(self, connection):
        self.connections.append(connection)

    def broadcast(self, sender, message):
        print(f"{self.name} received the message from {sender.name}: {message}")
        for connection in self.connections:
            if connection.device == sender:
                continue
            if isinstance(connection.device, Switch):
                print(f"{self.name} is forwarding the message to {connection.device.name}")
                connection.device.forward(sender, message, connection)
            else:
                print(f"{self.name} is broadcasting the message to {connection.device.name}")
                connection.device.receive(message)

class Switch:
    def __init__(self, name):
        self.name = name
        self.mac_table = {}
        self.connections = []

    def connect(self, connection):
        self.connections.append(connection)

    def learn_mac(self, sender, connection):
        self.mac_table[sender] = connection

    def forward(self, sender, message, connection):
        self.learn_mac(sender.name, connection)

        dest = message.split(":")[0].strip()
        if dest in self.mac_table:
            target_connection = self.mac_table[dest]
            if target_connection != connection:
                print(f"{self.name} is forwarding the message from {sender.name} to {dest}")
                target_connection.device.receive(message)
        else:
            print(f"{self.name} received the message from {sender.name}: {message}")
            for conn in self.connections:
                if conn != connection:
                    if isinstance(conn.device, Hub):
                        print(f"{self.name} is forwarding the message to {conn.device.name}")
                        conn.device.broadcast(sender, message)
                    else:
                        print(f"{self.name} is broadcasting the message to {conn.device.name}")
                        conn.device.receive(message)

    def csma_cd(self, sender, message, connection):
        collision_detected = random.choice([True, False])
        backoff_attempts = 0
        max_backoff_attempts = 10

        while collision_detected and backoff_attempts < max_backoff_attempts:
            print(f"{sender} detects collision. Attempt {backoff_attempts + 1} with exponential backoff.")
            backoff_time = random.uniform(0, (2 ** backoff_attempts) * 0.001)
            time.sleep(backoff_time)
            backoff_attempts += 1
            collision_detected = random.choice([True, False])

        if not collision_detected:
            print(f"{sender} successfully sends the message after {backoff_attempts} attempts.")
            self.forward(sender, message, connection)
        else:
            print(f"{sender} failed to send the message after {max_backoff_attempts} attempts due to continuous collisions.")

    def go_back_n_arq(self, sender, message, connection):
        seq_num = 0
        window_size = 5
        messages = [f"{message} (Sequence #{seq_num + i})" for i in range(window_size)]

        for msg in messages:
            print(f"{sender} sends message with Go-Back-N ARQ: {msg}")
            self.forward(sender, msg, connection)
            time.sleep(0.5)

        for i in range(window_size):
            ack = random.choice([True, False])
            if ack:
                print(f"{sender} received ACK for Sequence #{seq_num + i}")
            else:
                print(f"{sender} did not receive ACK for Sequence #{seq_num + i}. Resending from Sequence #{seq_num + i}...")
                self.go_back_n_arq(sender, message, connection)
                break

    def selective_repeat(self, sender, message, connection):
        seq_num = 0
        window_size = 5
        messages = [f"{message} (Sequence #{seq_num + i})" for i in range(window_size)]

        for msg in messages:
            print(f"{sender} sends message with Selective Repeat: {msg}")
            self.forward(sender, msg, connection)
            time.sleep(0.5)

        for i in range(window_size):
            ack = random.choice([True, False])
            if ack:
                print(f"{sender} received ACK for Sequence #{seq_num + i}")
            else:
                print(f"{sender} did not receive ACK for Sequence #{seq_num + i}. Resending Sequence #{seq_num + i}...")
                msg = messages[i]
                print(f"{sender} sends message with Selective Repeat: {msg}")
                self.forward(sender, msg, connection)

    def stop_and_wait_arq(self, sender, message, connection):
        print(f"{sender} sends message with Stop-and-Wait ARQ: {message}")
        ack_received = False

        while not ack_received:
            self.forward(sender, message, connection)
            time.sleep(0.5)

            ack = random.choice([True, False])
            if ack:
                print(f"{sender} received ACK for the message.")
                ack_received = True
            else:
                print(f"{sender} did not receive ACK. Resending the message...")

class Connection:
    def __init__(self, device, hub):
        self.device = device
        self.hub = hub

    def transmit(self, sender, message):
        if isinstance(sender, EndDevice):
            if isinstance(self.hub, Switch):
                self.hub.learn_mac(sender.name, self)
                self.hub.csma_cd(sender.name, message, self)
            else:
                self.hub.broadcast(sender, message)
        elif isinstance(sender, Hub):
            self.device.receive(message)

class NetworkSimulator:
    def create_device(self, device_type):
        if device_type == "end_device":
            return EndDevice(str(uuid.uuid4()))
        elif device_type == "hub":
            return Hub(str(uuid.uuid4()))
        elif device_type == "switch":
            return Switch(str(uuid.uuid4()))

    @staticmethod
    def test_case_1():
        print("Test Case 1: Dedicated connection between two end devices")
        device1 = EndDevice("Device 1")
        device2 = EndDevice("Device 2")
        hub = Hub("Hub 1")
        connection1 = Connection(device1, hub)
        connection2 = Connection(device2, hub)
        hub.connect(connection1)
        hub.connect(connection2)
        message = input("Enter the message to send from Device 1 to Device 2: ")
        device1.send(message, connection1)

    @staticmethod
    def test_case_2():
        print("\nTest Case 2: Star topology with five end devices connected to a hub")
        hub = Hub("Hub 1")
        devices = [EndDevice(f"Device {i}") for i in range(1, 6)]
        connections = [Connection(device, hub) for device in devices]
        for connection in connections:
            hub.connect(connection)

        sender = random.choice(devices)
        message = input(f"Enter the message to send from {sender.name}: ")
        sender.send(message, connections[devices.index(sender)])

    @staticmethod
    def test_case_3():
        print("\nTest Case 3: Data Link Layer - Switch with five end devices, CSMA/CD, Go-Back-N ARQ, and Selective Repeat")
        switch = Switch("Switch 1")
        devices = [EndDevice(f"Device {i}") for i in range(1, 6)]
        connections = [Connection(device, switch) for device in devices]
        for connection in connections:
            switch.connect(connection)

        def choose_devices():
            print("Available devices: ", [device.name for device in devices])
            sender_index = int(input("Choose the sender device (1-5): "))
            while sender_index < 1 or sender_index > 5:
                print("Invalid choice. Please choose a valid number.")
                sender_index = int(input("Choose the sender device (1-5): "))
            sender_name = f"Device {sender_index}"

            receiver_index = int(input("Choose the receiver device (1-5): "))
            while receiver_index < 1 or receiver_index > 5 or sender_index == receiver_index:
                if sender_index == receiver_index:
                    print("Sender and receiver cannot be the same. Please choose a different device.")
                else:
                    print("Invalid choice. Please choose a valid number.")
                receiver_index = int(input("Choose the receiver device (1-5): "))
            receiver_name = f"Device {receiver_index}"

            return sender_name, receiver_name

        sender_name, receiver_name = choose_devices()
        message = input(f"Enter the message to send from {sender_name} to {receiver_name}: ")
        message = f"{receiver_name}: {message}"
        sender = next(device for device in devices if device.name == sender_name)
        connection = connections[devices.index(sender)]

        print("\nChoose the protocol to use:")
        print("1. CSMA/CD")
        print("2. Go-Back-N ARQ")
        print("3. Selective Repeat")
        print("4. Stop-and-Wait ARQ")
        protocol_choice = int(input("Enter the number of the chosen protocol: "))

        if protocol_choice == 1:
            switch.csma_cd(sender.name, message, connection)
        elif protocol_choice == 2:
            switch.go_back_n_arq(sender.name, message, connection)
        elif protocol_choice == 3:
            switch.selective_repeat(sender.name, message, connection)
        elif protocol_choice == 4:
            switch.stop_and_wait_arq(sender.name, message, connection)
        else:
            print("Invalid choice. Please choose a valid protocol number.")
