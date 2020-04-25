

'''

old boy 17

'''


name = 'Joker'
#
# def change_name():
#     global  name
#     name = "dick"
#     print(name)
#
#     def foo():
#         name = "wu"
#         nonlocal  name
#         name="fuck"
#         print(name)
#     foo()
# change_name()



def test():
    print("in the test")
def test1():
    print("in the test1") 
    return test


def filter_test(array):
    ret = []
    for p in array:
        if not p.startswith('sb'): ret.append(p)
    return ret
mov = ['sb_alex','joker','linhaifeng']
# res = filter_test(mov)
# print(res)
# rest = test()
# print(rest())


def sb_show(n):
    return n.startswith("sb")

def filer_test(func,array,init=None):
    ret = []
    for p in array:
        if not func(p):
            ret.append(p)
    return ret

rest = filer_test(sb_show,mov)
print(rest)