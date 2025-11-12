


import os
verbos = True


class RenameFile:
    def __init__(self,path_src,path_dest):
        self.src ,self.dest = path_src,path_dest

    def execute(self):
        if verbos:
            print("[renaming '{}']".format(self.src,self.dest))
        os.rename(self.src,self.dest)

    def undo(self):
        if verbos:
            print("[renaming '{}' back to '{}']".format(self.dest,self.src))
        os.rename(self.dest,self.src)

class CreateFile:
    def __init__(self,path,txt='hello world \n'):
        self.path ,self.txt = path,txt
    def execute(self):
        if verbos:
            print("[creating file '{}']".format(self.path))
        with open(self.path,mode='w',encoding='utf-8') as out_file:
            out_file.write(self.txt)
    def undo(self):
        delete_file(self.path)


class ReadFile:
    def __init__(self,path):
        self.path = path

    def execute(self):
        if verbos:
            print("[reading file '{}']".format(self.path))
        with open(self.path,mode='r',encoding='utf-8') as in_file:
            print(in_file.read(),)
def delete_file(path):
    if verbos:
        print("deleting file '{}'".format(path))
    os.remove(path)

def main():
    orig_name,new_name = 'file1','file2'
    commands = []
    for cmd in CreateFile(orig_name),ReadFile(orig_name),RenameFile(orig_name,new_name):
        commands.append(cmd)
    [c.execute() for c in commands]
    answer = input('reverse the executed commands [Y/N]')
    if answer not in 'Y':
        print('The result is {}'.format(new_name))
        exit()
    for c in reversed(commands):
        try:
            c.undo()
        except AttributeError as e:
            pass
if __name__ == '__main__':
    main()