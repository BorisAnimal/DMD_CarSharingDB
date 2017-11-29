import itertools
from random import shuffle

def get_locations():
    gpsx = ["10.210", "21.80", "17.21", "15.1561", "213.112", "10.210", "21.80", "17.21", "15.1561", "213.112"]
    gpsy = ["15.1561", "213.112", "10.210", "10.210", "21.80", "17.21", "21.80", "17.21", "15.1561", "213.112"]
    tmp = list(itertools.product(gpsx, gpsy))
    shuffle(tmp)
    return tmp


def get_addresses():
    stt = ["Chuvashia", "Tatarstan", "Kalmikia", "Bashkiria"]
    ct = ["Kazan", "Innopolis", "Cheboksary"]
    str = ["Sportivnaya", "Baumana", "Lenina", "Gogolya"]
    hs = ["19", "1", "15", "12", "10", "2"]
    zp = ["420500", "452250", "124525", "151521", "422188"]
    tmp = list(itertools.product(stt, ct, str, hs, zp))
    shuffle(tmp)
    return tmp


def get_customers():
    nm = ["John", "Snowy", "Snoop"]
    dt = ["29.01.1992", "30.01.2000", "31.01.1987", "01.02.1991", "02.02.2002"]
    pn = ["5445555455", "646465465", "6465446464", "66651515", "46566515"]
    fn = ["Lock", "Matt", "Kate", "Lina"]
    ln = ["Dogg", "Daymon", "Gogo", "Tiger"]
    tmp = list(itertools.product(nm, dt, pn, fn, ln))
    shuffle(tmp)
    return tmp


def get_cars():
    st = ["good", "bad"]
    cl = [10, 90]
    tf = [70, 80]
    ml = ["Volvo", "lada"]
    col = ["red", "green"]
    pl = ["e777kx", "h123bm"]
    tmp = list(itertools.product(st, cl, tf, ml, col, pl))
    shuffle(tmp)
    return tmp
