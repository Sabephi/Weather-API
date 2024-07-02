def fun_logi(funkcja,miasto):
    import datetime
    f = open("log.txt",mode='a')
    czas_teraz = datetime.datetime.now()
    f.write(f"{czas_teraz.strftime("%x, %X")} - wyswietlono funkcje {funkcja} dla miasta {miasto} \n")

def fun_blad(blad):
    import datetime
    f = open("log.txt",mode='a')
    czas_teraz = datetime.datetime.now()
    f.write(f"{czas_teraz.strftime("%x, %X")} - blad w czesci {blad} \n")

def fun_show():
    f = open("log.txt",mode='r')
    return f.read()