import urllib.parse


def tostr(any):
    if isinstance(any,int): any = str(any)

    print(any)
    print(type(any))
    return any

def strtourlencode(_string):
    url_code_name = urllib.parse.quote(_string)
    print(url_code_name)
    return (url_code_name)


def get_string(dict1):
    string_dict = ""
    if dict1 != {}:
        sorted_list = sorted(dict1.items(), key=lambda d: d[0])
        for i in iter(sorted_list):
            str1 = i[0] + "=" + tostr(i[1]) + "&"
            string_dict += str1
        # print(string_dict)
        print(string_dict[0:-1])

    return string_dict[0:-1]

d = {"a":"3","b":3}
get_string(d)


li = [{"quoteStatus": 0,"conflictTotal": 0,"classCourseId": None}]

tostr(32)
#
# k  = ",".join(li)
# print(k)




from string import Template
s = Template("{'name':'${name}','age':${age}}")
k = (s.substitute({'name':'sd','age':32}))
print(k)
