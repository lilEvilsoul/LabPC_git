from selenium import webdriver
import time
import os
from openpyxl import Workbook
from bs4 import BeautifulSoup as bs
import requests
import re
from openpyxl.styles import Font

def OpenChrome(nombre):
    PATH = "C:/WebDriver/chromedriver.exe"

    driver = webdriver.Chrome(PATH)
    driver.get("https://www.google.com")

    time.sleep(2)

    srch_tag = driver.find_element_by_name("q")
    srch_tag.send_keys(nombre)
    srch_btn = driver.find_element_by_name("btnK")
    srch_btn.submit()

    time.sleep(2)

    with open("Recursos/Urls.txt", "a") as file:
        for elemnt in driver.find_elements_by_xpath('//div[@class="tF2Cxc"]'):
            link = elemnt.find_element_by_xpath('.//div[@class="yuRUbf"]/a').get_attribute('href')
            file.write(link + "\n")
    
    time.sleep(2)

    srch_tag2 = driver.find_element_by_name("q")
    srch_tag2.clear()
    srch_tag2.send_keys(nombre + " wegow")
    srch_tag2.submit()

    with open("Recursos/Urls.txt", "a") as file2:
        cont = 0
        for elemnt2 in driver.find_elements_by_xpath('//div[@class="tF2Cxc"]'):
            if cont >= 3:
                pass
            else:
                link = elemnt2.find_element_by_xpath('.//div[@class="yuRUbf"]/a').get_attribute('href')
                file2.write(link + "\n")
            cont += 1

    time.sleep(2)

    srch_tag3 = driver.find_element_by_name("q")
    srch_tag3.clear()
    srch_tag3.send_keys(nombre + " noticias")
    srch_tag3.submit()
    
    with open("Recursos/Noticias.txt", "w", encoding="utf-8") as news:
        for elemnt3 in driver.find_elements_by_xpath('//div[@class="tF2Cxc"]'):
            title = elemnt3.find_element_by_xpath('.//h3').text
            link_news = elemnt3.find_element_by_xpath('.//div[@class="yuRUbf"]/a').get_attribute('href')
            detail = elemnt3.find_element_by_xpath('.//span[@class="aCOpRe"]').text
            news.write(title + " | " + link_news + " | " + detail + "\n")
    
    time.sleep(2)
    driver.quit()

def concert_info(sheet, book, nombre):
    for file_name in os.walk("Recursos"):
            for name in file_name[2]:
                if ".txt" in name and name != "Urls.txt":
                    with open("Recursos/" + name, "r", encoding='UTF-8') as page_html:
                        soup = bs(page_html, "html.parser")

                        #Nombre
                        name = []
                        for nm in soup.find_all('a', class_="event-title"):
                            event = []
                            for i in str(nm.get('title')):
                                if i == "\n":
                                    pass
                                else:
                                    event.append(i)
                            name.append(str.join('', event))

                        #Fechas
                        datetime = []
                        for dt in soup.find_all('time', class_="event-start-time"):
                            dates = []
                            for i in str(dt.text):
                                if i == "\n" or i.isspace():
                                    pass
                                else:
                                    dates.append(i)
                            datetime.append(str.join('', dates))

                        #Lugares
                        place = []
                        for lg in soup.find_all('a', class_="venue-name"):
                            lugar = []
                            for i in str(lg.text):
                                if i == "\n" or i.isspace():
                                    pass
                                else:
                                    lugar.append(i)
                            place.append(str.join('', lugar))

                        #Precios
                        price = []
                        for p in soup.find_all('p', class_="event-price" ):
                            precio = []
                            for i in str(p.text):
                                if i == "\n" or i.isspace() or i.isalpha():
                                    pass
                                else:
                                    precio.append(i)
                            price.append(str.join('', precio))

                        #Hora
                        hour = []
                        for hr in soup.find_all('time', class_="time"):
                            time = []
                            for i in str(hr.text):
                                if i == "\n" or i.isspace():
                                    pass
                                else:
                                    time.append(i)
                            hour.append(str.join('', time))

                        if not datetime and not place and not price:
                            pass
                        else:
                            u = 3
                            for m in name:
                                sheet[f'F{u}'] = str(m)
                                u += 1

                            i = 3
                            for x in place:
                                sheet[f'G{i}'] = str(x)
                                i += 1
                            
                            o = 3
                            for y in datetime:
                                sheet[f'H{o}'] = str(y)
                                o += 1

                            t = 3
                            for n in hour:
                                sheet[f'I{t}'] = str(n)
                                t += 1

                            p = 3
                            for z in price:
                                sheet[f'J{p}'] = str(z)
                                p += 1

                            book.save(nombre + '.xlsx')

def social_info(sheet, book, nombre):
    redes = []
    with open("Recursos/Urls.txt", "r") as file:
        for line in file:
            social = re.compile(r'https://(www.)?(facebook)?(twitter)?(instagram)?(youtube)?(music.apple)?(open.spotify)?.com/')
            if social.search(line):
                redes.append(line)
            else:
                pass
            
    x = 2
    for y in redes:
        sheet[f'A{x}'] = str(y)
        x += 1
    book.save(nombre + '.xlsx')

    notice = []
    with open("Recursos/Noticias.txt", "r", encoding='UTF-8') as file2:
        for line2 in file2:
            notice.append(line2)
    
    u = 2
    for z in notice:
        sheet[f'L{u}'] = str(z)
        u += 1
    book.save(nombre + '.xlsx')

def request_estructure():
    name_link = []
    link_request = []

    with open("Recursos/Urls.txt") as file:
        for link in file:
            if link != "- - - - - - - - - - Urls Disponibles - - - - - - - - - -" + "\n":
                for x in link:
                    if x == "/" or x == "\n" or x == ":" or x == "." or x == "?" or x == "*" or x == "|" or x == '"':
                        pass
                    else:
                        name_link.append(x)

                if not os.path.isfile("Recursos/" + str.join('', name_link) + ".txt"):
                    for y in link:
                        if y == "\n":
                            pass
                        else:
                            link_request.append(y)

                    not_request = re.compile(r'https://(www.)?(facebook)?(twitter)?(instagram)?(youtube)?(music.apple)?(open.spotify)?.com/')
                    if not_request.search(str.join('', link_request)):
                        pass
                    else:
                        page = requests.get(str.join('', link_request))
                        time.sleep(5)
                        if page.status_code == 200:
                            content = bs(page.content, "html.parser")
                            with open("Recursos/" + str.join('', name_link) + ".txt", "w", encoding='UTF-8') as file:
                                file.write(content.prettify())
                        else:
                            pass
                else:
                    pass
            else:
                pass
            name_link.clear()
            link_request.clear()

book = Workbook()
sheet = book.active

def Doc_Excel(sheet, book, nombre):
    sheet['A1'] = "Redes Sociales"
    sheet['A1'].font = Font(bold=True)

    sheet.merge_cells('F1:J1')
    sheet['F1'] = "Conciertos de " + nombre
    sheet['F1'].font = Font(bold=True)

    sheet['F2'] = "Nombre"
    sheet['F2'].font = Font(italic=True)
    sheet['G2'] = "Lugar"
    sheet['G2'].font = Font(italic=True)
    sheet['H2'] = "Fecha"
    sheet['H2'].font = Font(italic=True)
    sheet['I2'] = "Hora"
    sheet['I2'].font = Font(italic=True)
    sheet['J2'] = "Precio"
    sheet['J2'].font = Font(italic=True)

    sheet['L1'] = "Noticias"
    sheet['L1'].font = Font(bold=True)

    book.save(nombre + '.xlsx')

def WebScraping(nombre):
    print("\nCreando documento de excel...")
    Doc_Excel(sheet, book, nombre)
    print("Hecho!")

    print("\nObteniendo codigo fuente de las paginas...")
    request_estructure()
    print("Hecho!")

    print("\nObteniendo informacion personal y social...")
    social_info(sheet, book, nombre)
    print("Hecho!")

    print("\nObteniendo informacion de proximos conciertos...")
    concert_info(sheet, book, nombre)
    print("Hecho!")

    print("\n\nSe ha termiando el proceso de busqueda!, se ha creado un archvio de excel (" + nombre + ".xlsx)")
    input("presione 'enter' para continuar...")

def new_srch():
    with open("Recursos/Urls.txt", "w") as file:
        file.write("- - - - - - - - - - Urls Disponibles - - - - - - - - - -\n")

    if os.path.isdir("Recursos"):
        for file_name in os.walk("Recursos"):
            if file_name[2][0] == "Urls.txt":
                pass
            else:
                for file in file_name[2]:
                    if ".txt" in file and file != "Urls.txt":
                        os.remove("Recursos/" + file)

def menu(nombre):
    while True:
        os.system('cls')
        print("Busqueda automatizada\n")
        op = input("[1] Iniciar con la busqueda [2] Salir \nElija su opcion: ")

        if op == "1":
            print("Buscando links relacionados...")
            OpenChrome(nombre)
            print("Hecho!")
            WebScraping(nombre)
        elif op == "2":
            exit()
        else:
            input("Esta opcion es invalida, presione 'enter' para continuar...")


if __name__ == '__main__':
    new_srch()
    nombre = input("Ingrese el nombre de la persona famosa: ")
    menu(nombre)
