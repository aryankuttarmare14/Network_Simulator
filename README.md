# Network Simulator

This project is a network simulator that implements the entire protocol stack, including functionalities for the Physical, Data Link, Network, Transport, and Application layers. Developed in Python, it provides a framework to simulate various networking functionalities, including device creation, packet transmission, routing, and application layer services.

## Functionalities Implemented

### Submission 1: Physical and Data Link Layer

**Physical Layer Functionalities:**
- Creating end devices and hubs.
- Creating connections between devices to form a topology.
- Sending and receiving data.

**Data Link Layer Functionalities:**
- Creating layer 2 devices: bridge and switch.
- Address learning in switches.
- Error control protocol (Parity Check).
- Access control protocol (CSMA/CD).
- Sliding window-based flow control protocol.

### Submission 2: Network Layer

**Network Layer Functionalities:**
- Creating and configuring a router.
- Assigning well-formatted classless IPv4 addresses to devices.
- Using ARP to find the MAC address of a host within a network.
- Performing static routing.
- Implementing RIP or OSPF protocols for dynamic routing.

### Submission 3: Transport and Application Layer

**Transport Layer Functionalities:**
- Assigning port numbers to various processes.
- Implementing sliding window flow control protocol (Go-Back-N or Selective Repeat).

**Application Layer Functionalities:**
- Telnet service.
- FTP service.

## File Structure

- **physical_layer.py:** Implementation of physical layer functionalities.
- **data_link_layer.py:** Implementation of data link layer functionalities.
- **network_layer.py:** Implementation of network layer functionalities.
- **transport_application_layer.py:** Implementation of transport and application layer functionalities.
- **README.md:** This file providing an overview of the project.

## Usage

1. Clone the repository:

```sh
git clone https://github.com/aryankuttarmare14/Network_Simulator
