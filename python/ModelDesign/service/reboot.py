import paramiko


def reboot():
    #传输文件到ap上,根据文件名选择命令
    ssh_ = paramiko.SSHClient()
    ssh_.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh_.connect(ip='101.201.81.174', port=22, username='root', password='7ujm^YHN~', timeout=30)
    except(Exception,):
        raise Exception(f"登录失败")
    try:
        stdin, stdout, stderr = ssh_.exec_command( f'cd /home/root;reboot')
        print("reboot succ")
    except:
        print("reboot failed")
