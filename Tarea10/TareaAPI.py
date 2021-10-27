from pyhunter import PyHunter
import getpass


def Search_domain(organizacion):
    res = hunter.domain_search(company=organizacion, limit=1, emails_type='personal')
    return res
    
masterkey = getpass.getpass("Ingresa tu APIkey: ")
ht = PyHunter(masterkey)
domain = input("Dominio a investigar: ")
info = Search_domain(domain)

if info is None:
    print("\nNo se ha encontrado nada relacionado a su busqueda")
    exit()
else:
    print(info)
