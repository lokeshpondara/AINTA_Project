from scapy.all import rdpcap

def analyze_pcap(file):

    packets = rdpcap(file)

    print("Total packets:",len(packets))

    protocols = {}

    for pkt in packets:

        proto = pkt.lastlaer().name

        protocols[proto] = protocols.get(proto,0) + 1

    print("\nProtocol distribution:")

    for p,c in protocols.items():
        print(p,c)