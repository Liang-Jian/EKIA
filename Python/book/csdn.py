import rsa
import base64
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA

#密钥一定要经过解码，否则无法直接使用，即bytes转str
pubkey = '''
        MIGJAoGBAIPTnV/W3oamUGE4gx/Hy4anOrcDve+rHvqjEnXgxE5Opy6dq0MTOZEs
        +AQtYO5+u3we/RlDcZgLeDg7OWTS6SFZVAVoVu03K7geGfMSedngVAB6uMYKxtJo
        +0k0+rUOCqXVFCIgLS5IS5i+8VyQjt7IfqE6m+rJIK1cpF1F2dDRAgMBAAE=
        '''
privkey = '''
        MIICYAIBAAKBgQCD051f1t6GplBhOIMfx8uGpzq3A73vqx76oxJ14MROTqcunatD
        EzmRLPgELWDufrt8Hv0ZQ3GYC3g4Ozlk0ukhWVQFaFbtNyu4HhnzEnnZ4FQAerjG
        CsbSaPtJNPq1Dgql1RQiIC0uSEuYvvFckI7eyH6hOpvqySCtXKRdRdnQ0QIDAQAB
        AoGAAIXiZfLwRxB52SjkPEgKoqofLYKySjUfllb3R8hwfu8I8sJlX4q/+7d19G5J
        qCiQjdmBn4wI81V4UKDLhMeYzsKoaWzLUaURCFkv7nH7p4nv0nU/fIdx2KymzBYt
        iOz/mQ1NPLc4vZ0PJ0ncPQrVbCavYs2H4d/8o5cDvrI8eAECRQC0dsNc875HK8y4
        acebaOjwHGX4Ap+bLYKL5P8zfgHLLV+putVcx5N4AnRyrLNjfzYS0FZHXhAFgCOz
        QmR/KkorcXNIoQI9ALsBOQgiZiWO3GEnMQqnM6qhmZg9727rWLd+/AvhxFs7Yy4Q
        e1Tpa4U66R4FljYBOcuCfGIDNvIcL86qMQJECKTDmLkn/PqxFIgkgmIU/iMuEyH1
        CRa18QNn4cyAQ34J3fRP8eCxRIdBkpiJAxP9wArwhvyPYeQQUa61Z43b/ZaygeEC
        PECUI4XTm0LNGv3R8vWi2AzM0aXpfY3oaDK1/4R66rw2vgFiX7TrBt5zgZ2EgGMV
        +Ud2QE34njjt0vSjgQJFAI3XEB2gqY/g4LbgCQpbaWlaNA/w8EPvNEe2SFlsKJBU
        uWe6l78I/sbvdRLfJ12XIN4I3Jnl8C3gwMI9iLaUz2MxuiUe
        '''

def public_long_encrypt(data, charset='utf-8'):
    global pubkey
    # base64.b64decode()解码一个字符串
    pub_key = RSA.importKey(base64.b64decode(pubkey))# 导入公钥
    pub_key_obj = Cipher_pkcs1_v1_5.new(pub_key)
    data = data.encode(charset) #将数据进行编码
    length = len(data)
    default_length = 117
    res = []
    for i in range(0, length, default_length):
        res.append(pub_key_obj.encrypt(data[i:i + default_length]))
    byte_data = b''.join(res)
    return base64.b64encode(byte_data)

def private_long_decrypt(data, sentinel=b'decrypt error'):
    global privkey
    pri_key = RSA.importKey(base64.b64decode(privkey))
    pri_key_obj = Cipher_pkcs1_v1_5.new(pri_key)
    data = base64.b64decode(data) # 将数据进行解码
    length = len(data)
    default_length = 128
    res = []
    for i in range(0, length, default_length):
        res.append(pri_key_obj.decrypt(data[i:i + default_length], sentinel))
    return str(b''.join(res), encoding = "utf-8")

data = 'little girl, I love you very much!'*100

cryto_info = public_long_encrypt(data)
print('加密信息：\n{}'.format(cryto_info))

decrypt_info = private_long_decrypt(cryto_info)
print('解密信息：\n{}'.format(decrypt_info))
