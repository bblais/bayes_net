def replace(mylist,val1,val2):
    newlist=[]
    for val in mylist:
        if val==val1:
            newlist.append(val2)
        else:
            newlist.append(val)
            
    return newlist


def flatten(L):
    
    y=[]
    for val in L:
        if isinstance(val,list):
            y.extend(flatten(val))
        else:
            y.append(val)

    return y

def combinations(items):

    if not items:
        yield []
    else:
        for item in items[0]:
            for c in combinations(items[1:]):
                y=[item]
                y.extend(c)
                yield y

def time2str(t):

    minutes=60
    hours=60*minutes
    days=24*hours
    years=365*days
    
    yr=int(t/years)
    t-=yr*years

    dy=int(t/days)
    t-=dy*days
    
    hr=int(t/hours)
    t-=hr*hours

    mn=int(t/minutes)
    t-=mn*minutes

    sec=t

    s=""
    if yr>0:
        s+=str(yr)+" years "
    if dy>0:
        s+=str(dy)+" days "
    if hr>0:
        s+=str(hr)+" hours "
    if mn>0:
        s+=str(mn)+" minutes "        
        
    s+=str(sec)+" seconds "


    return s

