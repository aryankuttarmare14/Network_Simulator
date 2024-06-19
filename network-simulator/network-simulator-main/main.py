from physical_l import *
from datalink_l import *
from network_l import *
from transport_application_l import *

def transport_application_l():
    # Define your test cases for the application layer here
    pass

if __name__ == "__main__":
    # Run tests for physical and data link layers
    simulator = NetworkSimulator()
    simulator.test_case_1()
    simulator.test_case_2()
    simulator.test_case_3()

    # Run tests for network layer
    test_network_layer()
    test_rip_protocol()

    # Run tests for application layer
    transport_application_l()
