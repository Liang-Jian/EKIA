
import rsa,mysql.connector
import base64


def wpub():
    (pubkey, privkey) = rsa.newkeys(2048)

    pub = pubkey.save_pkcs1()
    pubfile = open('public.pem', 'wb')
    pubfile.write(pub)
    pubfile.close()

    pri = privkey.save_pkcs1()
    prifile = open('private.pem', 'wb')
    prifile.write(pri)
    prifile.close()

def rpub():
    with open('public.pem', 'rb') as publicfile:
        p = publicfile.read()
        pubkey = rsa.PublicKey.load_pkcs1(p)
        print(pubkey)
    with open('private.pem', 'rb') as private:
        p = private.read()
        privkey = rsa.PrivateKey.load_pkcs1(p)
        print(privkey)

    return (pubkey,privkey)


def en_msg(password):
    encrypted_message = rsa.encrypt(password.encode('utf-8'), rpub()[0])
    print(base64.b64encode(encrypted_message))
    print('=====')
    print(base64.b64encode(encrypted_message).decode('utf-8'))
    return (base64.b64encode(encrypted_message).decode('utf-8'))

def de_msg(msg):
    msg_ = base64.b64decode(msg).decode('iso8859-1')
    decrypted_message = rsa.decrypt(msg_.encode('iso8859-1'), rpub()[1])
    print(decrypted_message.decode('iso8859-1'))
    
class MsqService(object):

    def __init__(self):
        self.conn = mysql.connector.connect(host='127.0.0.1', user='root', password='root',
                                            database='jleague',use_unicode=True)
        self.cursor = self.conn.cursor()
    def search(self, sql):

        self.cursor.execute(sql)
        select_data = self.cursor.fetchall()
        print("sql result:={}".format(select_data))
        return select_data

    def update(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()

    def close(self):
        if self.conn != None:
            self.conn.close()

        if self.cursor !=None:
            self.cursor.close()
    def __del__ (self):
        try:
            self.conn.close()
        except :
            pass

def main(id,pword):

    # mysql_command = "update event_tmp set password='%s' where id=%d" % (en_msg(pword),id)
    # MsqService().update(mysql_command)
    server = MsqService().search("select password from event_tmp where id={}".format(id))[0][0]
    de_msg(server)
# pw =
main(2,"s")