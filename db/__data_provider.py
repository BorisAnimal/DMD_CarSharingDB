import itertools


def get_locations():
    stt = ["Chuvashia", "Tatarstan", "Kalmikia", "Bashkiria"]
    ct = ["Kazan", "Innopolis", "Cheboksary"]
    str = ["Sportivnaya", "Baumana", "Lenina", "Gogolya"]
    hs = ["19", "1", "15", "12", "10", "2"]
    zp = ["420500", "452250", "124525", "151521", "422188"]
    gpsx = ["10.210", "21.80", "17.21", "15.1561", "213.112"]
    gpsy = ["10.210", "21.80", "17.21", "15.1561", "213.112"]
    return list(itertools.product(stt, ct, str, hs, zp, gpsx, gpsy))


def get_customers():
    nm = ["John", "Snowy", "Snoop"]
    dt = ["29.01.1992", "30.01.2000", "31.01.1987", "01.02.1991", "02.02.2002"]
    pn = ["5445555455", "646465465", "6465446464", "66651515", "46566515"]
    fn = ["Lock Dogg", "Matt Daymon", "Kate Gogo", "Lina Tiger"]
    return list(itertools.product(nm, dt, pn, fn))

def get_cars():
    st = ["good", "bad"]
    cl = [10, 90]
    tf = [70, 80]
    ml = ["Volvo", "lada"]
    col = ["red", "green", "Brown"]
    pl = ["e777kx", "h123bm"]
    return list(itertools.product(st, cl, tf, ml, col, pl))