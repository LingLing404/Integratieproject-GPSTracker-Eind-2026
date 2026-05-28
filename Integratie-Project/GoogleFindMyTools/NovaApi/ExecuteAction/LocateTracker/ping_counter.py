
pingcount = 0

def ping():
    global pingcount
    pingcount =+ 1
    return pingcount

def get():
    return pingcount