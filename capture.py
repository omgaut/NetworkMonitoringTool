import pyshark
import argparse
import time
import csv

parser = argparse.ArgumentParser(prog='PysharkRead', description='Read packets.')
parser.add_argument('--interface', nargs='?', type=str, help='PysharkRead scripts files')
parser.add_argument('--timeout', nargs='?', type=str, default='10', help='Timeout for sniffing')
parser.add_argument('--packets', nargs='?', type=str, default='5', help='Packet count to sniff')
args = parser.parse_args()

capture = pyshark.LiveCapture(interface=args.interface)
# capture.sniff(timeout=int(args.timeout))
cnt = 1
print("src_addr,src_port,dst_addr,dst_port,protocol,packet_len")

src_addr = []
src_port = []
dst_addr = []
dst_port = []
protocol = []
packet_len = []

for packet in capture.sniff_continuously(packet_count=int(args.packets)):
    # print('Just arrived:', packet)
    try:
        cnt = cnt + 1
        localtime = time.asctime(time.localtime(time.time()))

        protocol = packet.transport_layer  # protocol type
        if packet.ip:
            src_addr = packet.ip.src  # source address
            dst_addr = packet.ip.dst  # destination address
        src_port = packet[protocol].srcport  # source port
        dst_port = packet[protocol].dstport  # destination port
        packet_len = packet.length

        # output packet info
        print("%s,%s,%s,%s,%s,%s" % (src_addr, src_port, dst_addr, dst_port, protocol, packet_len))

    except AttributeError as e:
    # ignore packets other than TCP, UDP and IPv4
        print(e)
        print('Just arrived:', packet)
        pass

print("Counts ", cnt)


data = [src_addr, src_port, dst_addr, dst_port, protocol, packet_len]

with open("data2.csv", "w") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerows(data)