import pymysql


def connect():
    s = "localhost"  # TODO: replace with env vars
    d = "alphagrep"
    u = "bill"
    p = "Stovepipe1!"
    conn = pymysql.connect(host=s, user=u, password=p, database=d)
    return conn
