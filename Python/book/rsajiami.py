"""
注意：
api签名时：签名用私钥，验签用公钥
数据加密时：加密用公钥，解密用私钥
密钥和公钥保存的图片会在下边展示出来
"""
import rsa


# 对api的签名机制进行验证：签名用私钥，验签用公钥
class RsaEncrypt:
    def __init__(self, sign_str):
        self.sign_str = sign_str

    def rsa_generate(self):
        """
        生成私钥和公钥并保存
        :return:
        """
        # 生成公钥和私钥
        pubkey, privkey = rsa.newkeys(2048)
        pub = pubkey.save_pkcs1()
        # 公钥
        with open('public.pem', 'wb') as w_pub:
            w_pub.write(pub)
        # 私钥
        pri = privkey.save_pkcs1()
        with open('private.pem', 'wb') as w_pri:
            w_pri.write(pri)
        return "保存成功"

    @classmethod
    def read_rsa(self):
        """
        读取公钥和私钥
        :return:
        """
        with open('public.pem', 'rb') as publickfile:
            pub = publickfile.read()
            pubkey = rsa.PublicKey.load_pkcs1(pub)
        with open('private.pem', 'rb') as privatefile:
            priv = privatefile.read()
            # print(pub)
            privkey = rsa.PrivateKey.load_pkcs1(priv)
        return pubkey, privkey

    def str_sign(self):
        privkey = self.read_rsa()[1]
        # 先将要加密的数据转成二进制
        str_encode = self.sign_str.encode()
        # 用私钥进行加密，并设置加密算法
        signature = rsa.sign(str_encode, privkey, 'SHA-1')  # 签名加密算法可以更换比如：SHA-256
        # print(signature)
        return signature

    def sign_verify(self, signature):
        """
        验证签名是否正确，如果正确，则返回签名算法,否则返回验证失败
        :param signature:
        :return:
        """
        pubkey = self.read_rsa()[0]
        try:
            agl = rsa.verify(self.sign_str.encode(), signature, pubkey)
            print(type(agl))
            print(agl.encode("utf-8"))  # 返回加密算法代表验签成功
            return True
        except rsa.VerificationError:
            print("验证失败")
            return False


# 对数据进行加密:加密用公钥，解密用私钥
class DataEncrypt:
    def __init__(self, data_str):
        self.data_str = data_str
        self.secret_key = RsaEncrypt.read_rsa()  # 调用RsaEncrypt类的读取密钥对方法

    def data_encrypt(self):
        """
        用公钥对数据进行加密
        :return:
        """
        str_encrypt = rsa.encrypt(self.data_str.encode(), self.secret_key[0])
        print(str_encrypt)  # 加密后看着像二进制，但有不太像，看不懂
        return str_encrypt

    def data_decrypt(self, encrypt):
        str = rsa.decrypt(encrypt, self.secret_key[1]).decode()
        print(str)  # 返回加密前的数据
        return str


if __name__ == '__main__':
    # RsaEncrypt('a').rsa_generate()
    # 验证签名机制
    sing_test = RsaEncrypt('shichengtao1989')
    sing_test.sign_verify(sing_test.str_sign())
    # 验证加密解密机制
    data = DataEncrypt('dfad--fa/d.s$$$&{}()><?L::>')
    data.data_decrypt(data.data_encrypt())

    data.data_decrypt(sing_test)