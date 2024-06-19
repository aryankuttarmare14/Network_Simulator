import uuid
from physical_l import *
from datalink_l import *

class Router(Device):
    def __init__(self, device_id):
        super().__init__(device_id, "router")
        self.routing_table = {}
        self.arp_table = {}

    def add_route(self, destination_network, subnet_mask, next_hop):
        self.routing_table[(destination_network, subnet_mask)] = next_hop

    def arp_request(self, ip_address):
        if ip_address in self.arp_table:
            return self.arp_table[ip_address]
        else:
            mac_address = str(uuid.uuid4())  # Simulating ARP request/response
            self.arp_table[ip_address] = mac_address
            return mac_address

    def forward_packet(self, packet):
        dest_ip = packet.destination_ip
        for (network, mask), next_hop in sorted(self.routing_table.items(), key=lambda x: -x[1].count('1')):
            if self.ip_in_subnet(dest_ip, network, mask):
                next_hop_mac = self.arp_request(next_hop)
                # Forward packet to next hop (simulated)
                print(f"Forwarding packet to next hop {next_hop} with MAC {next_hop_mac}")
                break

    def ip_in_subnet(self, ip, network, mask):
        ip_bin = self.ip_to_bin(ip)
        network_bin = self.ip_to_bin(network)
        mask_bin = self.ip_to_bin(mask)
        return ip_bin & mask_bin == network_bin & mask_bin

    def ip_to_bin(self, ip):
        return int(''.join(f'{int(octet):08b}' for octet in ip.split('.')), 2)

class Packet:
    def __init__(self, source_ip, destination_ip, data):
        self.source_ip = source_ip
        self.destination_ip = destination_ip
        self.data = data

class ARPEntry:
    def __init__(self, ip_address, mac_address):
        self.ip_address = ip_address
        self.mac_address = mac_address

def create_ip_address(network, host_id):
    octets = network.split('.')
    octets[-1] = str(host_id)
    return '.'.join(octets)

def test_network_layer():
    # Create devices and router
    simulator = NetworkSimulator()
    devices = [simulator.create_device("end_device") for _ in range(4)]
    router = Router(str(uuid.uuid4()))

    # Assign IP addresses
    device_ips = ["192.168.1.1", "192.168.1.2", "192.168.2.1", "192.168.2.2"]
    subnet_masks = ["255.255.255.0", "255.255.255.0"]

    # Configure router with static routes
    router.add_route("192.168.1.0", "255.255.255.0", "192.168.1.1")
    router.add_route("192.168.2.0", "255.255.255.0", "192.168.2.1")

    # Test ARP
    mac_address = router.arp_request("192.168.1.1")
    print(f"MAC address for 192.168.1.1 is {mac_address}")

    # Create and forward packet
    packet = Packet("192.168.1.1", "192.168.2.2", "Hello, World!")
    router.forward_packet(packet)

def test_rip_protocol():
    # This is a simplified version of RIP for educational purposes.
    class RIPRouter(Router):
        def __init__(self, device_id):
            super().__init__(device_id)
            self.neighbors = []

        def add_neighbor(self, router):
            self.neighbors.append(router)

        def share_routing_table(self):
            for neighbor in self.neighbors:
                for (network, mask), next_hop in self.routing_table.items():
                    neighbor.add_route(network, mask, next_hop)

    router1 = RIPRouter(str(uuid.uuid4()))
    router2 = RIPRouter(str(uuid.uuid4()))

    router1.add_neighbor(router2)
    router2.add_neighbor(router1)

    router1.add_route("192.168.1.0", "255.255.255.0", "192.168.1.1")
    router2.add_route("192.168.2.0", "255.255.255.0", "192.168.2.1")

    print("Router 1 Routing Table Before RIP:")
    print(router1.routing_table)

    print("Router 2 Routing Table Before RIP:")
    print(router2.routing_table)

    # Share routing tables (simulating RIP)
    router1.share_routing_table()
    router2.share_routing_table()

    print("Router 1 Routing Table After RIP:")
    print(router1.routing_table)

    print("Router 2 Routing Table After RIP:")
    print(router2.routing_table)

if __name__ == "__main__":
    test_network_l()
    test_rip_protocol()
