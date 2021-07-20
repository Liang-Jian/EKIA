#-*- coding:utf-8 -*-


import socket,sys,argparse

host ='localhost'
# data_payload = 2048
# backlog =5
#
# def echo_server(port):
#     s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#     s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
def echo_client():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_address = (host,port)e
    print "connecting to %s  port %s" % server_address
    s.connect(server_address)
    try:
        message = 'test message '
        print 'sending %s' % message
        s.sendall(message)
        amount_recv = 0
        amount_expe = len(message)
        while amount_recv < amount_expe:
            s.recv(16)
            amount_recv += len(data)
            print "received : %s" % data
    except socket.errno,e:
        print 'socket error: %s' % str(e)
    except Exception,e:
        print "Other exception: %s" %str(e)
    finally:
        print 'close connect to servier'
        s.close()
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Socket Server Example')
    parser.add_argument('--port', action="store", dest="port", type=int,  required=True)
    given_args = parser.parse_args()
    port = given_args.port
    echo_client(port)