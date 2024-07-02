import requests
import time
import datetime
import logi

#Program wyświetla pogodę w mieście
#git https://github.com/Sabephi/Weather-API

#dekorator liczący czas funkcji
def dek_czasu(funkcja):
    def opakowanie(*args, **kwargs):
        start = time.time()
        wynik = funkcja(*args, **kwargs)
        koniec= time.time()
        print(f"\n{'>'*9} Czas wykonania {'<'*9} \n{koniec - start} sekund\n")
        return wynik
    return opakowanie

#klasa pobierająca podstawowe dane ze strony
class main:
    def __init__(self, city, api="1e13ef3d961f7822a0ba6a9357c087a1"):
        self.city = city
        self.api = api
    @dek_czasu
    def wyswietl_temp(self):
        request = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={self.api}")
        json = request.json()
        temp = round(int(json['main']['temp']) - 273.15)
        temp_min = round(int(json['main']['temp_min']) - 273.15)
        temp_max = round(int(json['main']['temp_max']) - 273.15)
        niebo = json['weather'][0]['description']
        wilgotnosc = json['main']['humidity']

        return temp, temp_min, temp_max, niebo, wilgotnosc
    
    @dek_czasu
    def wyswietl_wiatr(self):
        request = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={self.api}")
        json = request.json()
        wiatr_kierunek = json['wind']['deg']
        wiatr_kierunek = int(wiatr_kierunek)
        if wiatr_kierunek > 23 and wiatr_kierunek <= 67:
            wiatr_kier = 'NE'
        elif wiatr_kierunek > 67 and wiatr_kierunek <= 112:
            wiatr_kier = 'N'
        elif wiatr_kierunek > 112 and wiatr_kierunek <= 157:
            wiatr_kier = 'NW'
        elif wiatr_kierunek > 157 and wiatr_kierunek <= 202:
            wiatr_kier = 'W'
        elif wiatr_kierunek > 202 and wiatr_kierunek <= 247:
            wiatr_kier = 'SW'
        elif wiatr_kierunek > 247 and wiatr_kierunek <= 292:
            wiatr_kier = 'S'
        elif wiatr_kierunek > 292 and wiatr_kierunek <= 337:
            wiatr_kier = 'SE'
        elif (wiatr_kierunek > 337 and wiatr_kierunek <= 360) or (wiatr_kierunek >=0 and wiatr_kierunek <= 23):
            wiatr_kier = 'E'


        wiatr_predkosc = round(int(json['wind']['speed']) * 3.6)
        return wiatr_kier, wiatr_predkosc

    @dek_czasu
    def wyswietl_sys(self):
        request = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={self.api}")
        json = request.json()
        wschod = time.strftime("%H:%M:%S", time.gmtime(json['sys']['sunrise']+(json['timezone']) ))
        zachod = time.strftime("%H:%M:%S", time.gmtime(json['sys']['sunset']+(json['timezone'])))

        godz = time.strftime("%H:%M:%S", time.gmtime(json['dt']+(json['timezone'])))
        return wschod, zachod, godz
     
    @dek_czasu
    def wyswietl_koordynaty(self):
        request = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={self.api}")
        json = request.json()
        kier_y = json['coord']['lat']
        kier_x = json['coord']['lon']

        return kier_y, kier_x
    
    @dek_czasu
    def wyswietl_prognoza(self):
        json = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={self.api}").json()
        kier_y = json['coord']['lat']
        kier_x = json['coord']['lon']
        json = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?lat={kier_y}&lon={kier_x}&appid={self.api}").json()
        zbior = [json['list'][x] for x in range(0,40,8)]
        return zbior

# Nieskończona pętla będąca menu

while True:
    print(f'''
{">"*14} MENU {"<"*14}          
1. Temperatura
2. Wiatr
3. Godzina, Wschód/Zachód
4. Lokalizacja
5. Prognoza 5-dniowa
6. Test
7. Pokaz logi
8. Wyjdź 
''')
    
    wybor_menu = input("Wybierz opcję: ")
    wybor_menu = int(wybor_menu)
    print("\033c")
    if wybor_menu in range (1,6):
        miasto = input('Podaj miasto (ang): \n')
    else:
        pass

#temperatura
    if wybor_menu == 1:
        try:
            temp, temp_min, temp_max, niebo, wilgotnosc = main(miasto).wyswietl_temp()
            print('*' * 8, 'Temperatura', '*' * 8)
            print(f"""
Obecnie w mieście jest {temp}°C
Najmniej spadnie do {temp_min}°C
Maksymalnie {temp_max}°C
Niebo: {niebo}
Wilgotnośc wynosi {wilgotnosc}%
                """)
            logi.fun_logi('temperatura',miasto)
        except:
            logi.fun_blad('temperatura')
            print('błędne miasto')
#wiatr
    if wybor_menu == 2:
        try:
            wiatr_kierunek, wiatr_predkosc = main(miasto).wyswietl_wiatr()
            print('*' * 13, 'Wiatr', '*' * 13)
            print(f"""
Prędkość wiatru wynosi {wiatr_predkosc} km/h
Kierunek wiatru: {wiatr_kierunek}
                """)
            logi.fun_logi('wiatr',miasto)
        except:
            logi.fun_blad('wiatr')
            print('błędne miasto')
#długość dnia            
    if wybor_menu == 3:
        try:
            wschod, zachod, godz = main(miasto).wyswietl_sys()
            print('*' * 9, 'Godziny', '*' * 9)
            print(f"""
Obecna godzina w mieście {godz} 
Wschód o godzinie: {wschod}
Zachód o godzinie: {zachod}
                """)
            logi.fun_logi('godzinowa',miasto)
        except:
            logi.fun_blad('godzinowej')
            print('błędne miasto')
#lokalizcja
    if wybor_menu == 4:
        try:
            kier_y, kier_x = main(miasto).wyswietl_koordynaty()
            print('*' * 11, 'Koordynaty', '*' * 11)
            print(f"""
Szerokość geograficzna: {kier_y}
Długość geograficzna: {kier_x}
                """)
            logi.fun_logi('koordynaty',miasto)
        except:
            logi.fun_blad('lokalizacja')
            print('błędne miasto')
#prognoza
    
    if wybor_menu == 5:
        try:
            zbior = main(miasto).wyswietl_prognoza()
            print('*' * 12, 'Prognoza', '*' * 12)
            h=0
            for i in range(5):
                
                rok = int(zbior[i]['dt_txt'].split('-',3)[0])
                msc = int(zbior[i]['dt_txt'].split('-',3)[1])
                dzn = int(zbior[i]['dt_txt'].split('-',3)[2].split()[0])

                dzien_tyg_nr = datetime.date(rok, msc, dzn).weekday()
                dni_tygodnia = ["poniedziałek", "wtorek", "środa", "czwartek", "piątek", "sobota", "niedziela"]
            
                print(f"""
        >>>{dni_tygodnia[dzien_tyg_nr].upper()}({h}h)<<<
        Temperatura:  {round(int(zbior[i]['main']['temp']) - 273.15)}°C
        Wilgotność: {zbior[i]['main']['humidity']}%
        Niebo: {zbior[i]['weather'][0]['description']}
        Prędkość wiatru: {round(int(zbior[i]['wind']['speed']) * 3.6)} km/h
        """)
                h+=24
            logi.fun_logi('prognozy',miasto)
        except:
            logi.fun_blad('prognozy')
            print('błędne miasto')
#test
    if wybor_menu == 6:
        try:
            miasto_temp = "wroclaw"
            print("TEST-START")
            print(f"Testowane miasto: {miasto_temp}")
#test1
            temp, temp_min, temp_max, niebo, wilgotnosc = main(miasto_temp).wyswietl_temp()
            print('*' * 8, 'Temperatura', '*' * 8)
            print(f"""
Obecnie w mieście jest {temp}°C
Najmniej spadnie do {temp_min}°C
Maksymalnie {temp_max}°C
Niebo: {niebo}
Wilgotnośc wynosi {wilgotnosc}%
                """)
#test2
            wiatr_kierunek, wiatr_predkosc = main(miasto_temp).wyswietl_wiatr()
            print('*' * 13, 'Wiatr', '*' * 13)
            print(f"""
Prędkość wiatru wynosi {wiatr_predkosc} km/h
Kierunek wiatru: {wiatr_kierunek}
                """)
#test3
            wschod, zachod, godz = main(miasto_temp).wyswietl_sys()
            print('*' * 9, 'Godziny', '*' * 9)
            print(f"""
Obecna godzina w mieście {godz} 
Wschód o godzinie: {wschod}
Zachód o godzinie: {zachod}

                """)
#test 4
            kier_y, kier_x = main(miasto_temp).wyswietl_koordynaty()
            print('*' * 10, 'Koordynaty', '*' * 10)
            print(f"""
Szerokość geograficzna: {kier_y}
Długość geograficzna: {kier_x}
                """)
#test 5
            zbior = main(miasto_temp).wyswietl_prognoza()
            print('*' * 12, 'Prognoza', '*' * 12)
            h=0
            for i in range(5):
                
                rok = int(zbior[i]['dt_txt'].split('-',3)[0])
                msc = int(zbior[i]['dt_txt'].split('-',3)[1])
                dzn = int(zbior[i]['dt_txt'].split('-',3)[2].split()[0])

                dzien_tyg_nr = datetime.date(rok, msc, dzn).weekday()
                dni_tygodnia = ["poniedziałek", "wtorek", "środa", "czwartek", "piątek", "sobota", "niedziela"]
            
                print(f"""
        >>>{dni_tygodnia[dzien_tyg_nr].upper()}({h}h)<<<
        Temperatura:  {round(int(zbior[i]['main']['temp']) - 273.15)}°C
        Wilgotność: {zbior[i]['main']['humidity']}%
        Niebo: {zbior[i]['weather'][0]['description']}
        Prędkość wiatru: {round(int(zbior[i]['wind']['speed']) * 3.6)} km/h
        """)
                h+=24

#test koniec               
            print("TEST-END")
            logi.fun_logi('test',f'testowego {miasto_temp}')
        except:
            logi.fun_blad('testu')
            print('TEST-BŁĄD')

#logi
    if wybor_menu == 7:
        try:
            print(logi.fun_show())
        except:
            print('bład')       
#OFF            
    if wybor_menu == 8:
        print("wyłaczanie")
        break
