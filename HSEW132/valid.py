
def zn_number_sml(value):
    ali="{v0:{s0}{a0}{b0}}{dot}{v1:{s1}{a1}{b1}}"
    pf=False
    l0,l1=2,5
    
    if '%' in value:
        pf=True
        value=value.rstrip('%')
        ali+='<>|'
        l1-=3
        
    try:

        if '.' in value:
            V0,V1=[int(x) for x in value.split('.')]            
            if V0==0:
                return ' -'+ali.format(v0='',s0='',a0='',b0='',dot='.',v1=str(V1),s1='.',b1=l1,a1='')
            elif V0<20 and V0>0:
                return ali.format(v0=str(V0),s0='',a0='>',b0=l0,dot='.',v1=str(V1),a1='<',s1='0',b1=l1)
            else:
                return None
            
        else:            
            v=int(value)
            if pf:
                if v in range(-99,0):
                    return ' -'+ali.format(v0='',s0='',a0='',b0='',dot=' ',v1=str(v)[1:],s1='.',b1=l1,a1='>')
                elif v in range(0,2000):
                    return  ali.format(v0='',s0='',a0='',b0='',dot=' ',v1=str(v),s1='0',b1=l1,a1='<')
                else:
                    return None
            else:
                if v in range(-9999,0):
                    return' -'+ali.format(v0='',s0='',a0='',b0='',dot=' ',v1=str(v)[1:],s1='.',b1=l1,a1='>')
                elif v in range(0,200000):
                    V=str(v)
                    return  ali.format(v0=V[:2],s0='',a0='',b0='',dot=' ',v1=V[2:],s1='0',b1=l1,a1='<')
                else:
                    return None
                
    except Exception,e:
        return None
    return None

def zn_number_big(value):
    ali="{v:{s}{a}{b}}"
    pf=False
    length=5

    if '.' in value:
        return None

    if '%' in value:
        pf=True
        value=value.rstrip('%')
        ali+='<>|'
        length-=3

    try:
        num=int(value)
        if num<0:
            ali=' -'+ali
            length-=2
    except Exception,e:
        return None

    if not pf:
        if not (num in range(-999,20000)):
            return None
    else:
        if num<0:
            if not (num in range(-9,0)):
                return None
        else:
            if not (num in range(0,200)):
                return None

    return ali.format(v=str(abs(num)),s='',a='>',b=length)

def zn_mark_state(value):
    for x in value:
        if x not in 'ldxscLDXSC ':
            return None
    return value
    
def zn_mark_curren(value):
    for x in value:
        if x not in '1234 ':
            return None
    return value

def zn_mark_arrow(value):
    for x in value:
        if x not in 'aduADU ':
            return None
    return value

def zn_mark_promo(value):
    for x in value:
        if x not in 'aduADU ':
            return None
    return value
   
def zn_mark_bar(value):
    for x in value:
        if x not in '1234ABCDabcd':
            return None
    return value
    
def zn_mark_unit(value):
    for x in value:
        if x not in 'GLKUglku ':
            return None
    return value


def zn_alpha(value):
    mid='{0: ^6}'

    for x in value:
        if x not in '123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0-_*<>.':
            return None    
    
    
    if value.count('.') >0:
        st=value.split('.')
    else:
        return mid.format(value)+'   '
    
    length=len(st)

    if length==2:
        ali="{0[0]:{1}{2}{3}}{0[1]:{1}{2}{4}}"
        if len(st[0])>len(st[1]):
            v0,v1=4,2
            ali+='  .'
        elif len(st[0])<len(st[1]):
            v0,v1=2,4
            ali+='.  '
        else:
            v0,v1=3,3
            ali+=' . '
        return ali.format(st,'0','>',v0,v1)
    elif length==3:
        ali="{0[0]:{1}{2}{3}}{0[1]:{1}{2}{4}}{0[2]:{1}{2}{5}}"
        if len(st[1])>2 or len(st[1])==0:
            return None
        elif len(st[0])==len(st[2]):
            v0,v1,v2=2,2,2
            ali+='. .'    
        elif len(st[0])>len(st[2]):
            v0,v1,v2=3,1,2
            ali+=' ..'    
        elif len(st[0])<len(st[2]):
            v0,v1,v2=2,1,3
            ali+='.. '    
        return ali.format(st,'0','>',v0,v1,v2)
    elif length==4:
        ali='{0[0]:{1}{2}{3}}{0[1]:{1}{2}{4}}{0[2]:{1}{2}{5}}{0[3]:{1}{2}{6}}'+'...'
        if len(st[1])>1 or len(st[2])>1:
            return None
        else:
            v0,v1,v2,v3=2,1,1,2
            return ali.format(st,'0','>',v0,v1,v2,v3)
    else:
        return None
