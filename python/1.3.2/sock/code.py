server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(False)
# set option reused
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_address = ('192.168.1.102', 10001)
server.bind(server_address)

server.listen(10)

# sockets from which we except to read
inputs = [server]
# sockets from which we expect to write
outputs = []

# Outgoing message queues (socket:Queue)
message_queues = {}

# A optional parameter for select is TIMEOUT
timeout = 20

while inputs:
    print "waiting for next event"
    readable, writable, exceptional = select.select(inputs, outputs, inputs, timeout)