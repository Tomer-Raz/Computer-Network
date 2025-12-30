# TCP/IP Traffic Analysis & Socket Application

This project explores the fundamental principles of TCP/IP networking through two main phases: simulating the encapsulation process and building a distributed multi-client chat application using raw sockets.

## Project Components

### 1. Data Encapsulation & Packet Capture

This phase shows how application-layer data is prepared and wrapped into transport and internet layer headers for network transmission.

- **Input Data**: Users create a CSV file containing application-layer messages with the following fields:  
  `msg_id`, `app_protocol`, `src_app`, `dst_app`, `message`, `timestamp`.

- **Encapsulation Simulation**: Using a Jupyter Notebook, the project simulates the creation of IPv4 and TCP headers. This includes manual checksum calculations and building packet structures with Python `struct` and `socket` modules.

- **Traffic Generation**: The crafted packets are sent over the network using Raw Sockets (Linux or macOS) or the Scapy library with Npcap (Windows).

- **Packet Analysis**: Traffic is captured with Wireshark, filtered (for example `tcp port 12345`), and analyzed to verify header and payload integrity.

### 2. Distributed Chat System

This phase focuses on designing and implementing a real-time, two-way communication system.

- **Protocol**: Built entirely on TCP for reliable communication.
- **Server Logic**: A central server acts as a mediator, allowing clients to find and chat using unique usernames.
- **Concurrency**: The server supports at least 5 simultaneous client connections.
- **Low-Level Implementation**: Developed using standard socket libraries only. High-level frameworks like Spring are not allowed.
- **Error Handling**: Includes mechanisms to handle network issues such as unexpected client disconnections.

## Technical Requirements

- **Language**: Python (recommended for compatibility with the provided notebook examples).
- **Libraries**:  
  - `pandas` for data processing  
  - `scapy` for packet injection on Windows
- **Tools**: Wireshark (with Npcap for Windows loopback support).
- **Permissions**: Administrative or root privileges are required to access raw sockets.

## Installation & Setup

### Part 1: Running the Simulation

1. Prepare a CSV file named `groupXX_<application>_input.csv`.
2. Open the provided Jupyter Notebook and load the CSV file.
3. Run the cells to build the IP and TCP headers and transmit the data.
4. Monitor the traffic in Wireshark using filters like `ip.addr == 127.0.0.1`.

### Part 2: Operating the Chat App

1. Run the server script to start listening for TCP connections.
2. Launch multiple client instances and assign unique usernames.
3. Request a chat session by entering the name of another connected user.
4. Capture the session in Wireshark and save it as a `.pcap` file for network-layer analysis.

## Deliverables

- **Summary Report**: Detailed explanation of the encapsulation process and traffic analysis.
- **Codebase**: Full server and client source code.
- **Simulation Data**: Input CSV file and the executed Jupyter Notebook.
- **Captures**: Wireshark `.pcap` files showing the analyzed traffic.

## Analogy for Understanding

Think of the encapsulation process like sending a letter:  
- The CSV message is the letter itself.  
- The TCP header is the inner envelope with a room number (port).  
- The IP header is the outer envelope with the building address (IP).

The chat application works like a switchboard operator (server) that connects different callers (clients) so messages reach the correct room.
