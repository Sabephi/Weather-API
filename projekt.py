import requests
import time
import datetime

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
        wschod = time.strftime("%I:%M:%S", time.gmtime(json['sys']['sunrise']+(json['timezone']*1000) ))
        zachod = time.strftime("%I:%M:%S", time.gmtime(json['sys']['sunset']+(json['timezone']*1000)))

        godz = time.gmtime(json['dt'])
        return wschod, zachod, godz
     
    @dek_czasu
    def wyswietl_koordynaty(self):
        request = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={self.api}")
        json = request.json()
        kier_y = json['coord']['lat']
        kier_x = json['coord']['lon']
        return kier_y, kier_x
    
    def wyswietl_prognoza(self):
        json = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={self.api}").json()
        kier_y = json['coord']['lat']
        kier_x = json['coord']['lon']
        json = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?lat={kier_y}&lon={kier_x}&appid={self.api}").json()
        dzien = [json['list'][x] for x in range(0,40,8)]
        return dzien

# Nieskończona pętla będąca menu

while True:
    print(f'''
{">"*14} MENU {"<"*14}          
1. Temperatura
2. Wiatr
3. Długość dnia
4. Lokalizacja
5. Prognoza 5-dniowa
6. Test
7. Wyjdź 
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
            print('*' * 8, 'temperatura', '*' * 8)
            print(f"""
Obecnie w mieście jest {temp}°C
Najmniej spadnie do {temp_min}°C
Maksymalnie {temp_max}°C
Niebo: {niebo}
Wilgotnośc wynosi {wilgotnosc}%
                """)
        except:
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
        except:
            print('błędne miasto')
#długość dnia            
    if wybor_menu == 3:
        try:
            wschod, zachod, godz = main(miasto).wyswietl_sys()
            print('*' * 9, 'Wschód/Zachód', '*' * 9)
            print(f"""
Wschód o godzinie: {wschod}
Zachód o godzinie: {zachod}
{godz}
                """)
            
        except:
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
        except:
            print('błędne miasto')
#prognoza
    if wybor_menu == 5:
        dzien = main(miasto).wyswietl_prognoza()
        print('*' * 12, 'Prognoza', '*' * 12)
        print(f"""
{dzien[0]['dt_txt'].split("-",3)[0]}

        # numer_dnia_tygodnia = dzien[0]['dt_txt'].split()[0].weekday()
        # dni_tygodnia = ["poniedziałek", "wtorek", "środa", "czwartek", "piątek", "sobota", "niedziela"]
        # print(dni_tygodnia[numer_dnia_tygodnia])
""")

#test
    if wybor_menu == 6:
        try:
            miasto_temp = "wroclaw"
            print("TEST-START")
#test1
            temp, temp_min, temp_max, niebo, wilgotnosc = main(miasto_temp).wyswietl_temp()
            print('*' * 8, 'temperatura', '*' * 8)
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
            print('*' * 9, 'Wschód/Zachód', '*' * 9)
            print(f"""
Wschód o godzinie: {wschod}
Zachód o godzinie: {zachod}
{godz}
                """)
#test 4
            kier_y, kier_x = main(miasto_temp).wyswietl_koordynaty()
            print('*' * 10, 'Koordynaty', '*' * 10)
            print(f"""
Szerokość geograficzna: {kier_y}
Długość geograficzna: {kier_x}
                """)
            print("TEST-END")
        except:
            print('TEST-BŁĄD')
#OFF            
    if wybor_menu == 7:
        print("wyłaczanie")
        break
