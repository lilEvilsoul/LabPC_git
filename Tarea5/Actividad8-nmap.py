import nmap
import csv

# definimos los rangos de puertos para
# el escaneo
begin = 78
end = 80

#asigna el objetivo a ser escaneado
target = input("Ingrese la dirección ip: ")

scanner = nmap.PortScanner()

array = []
count = 1
for x in target:
	if count <= 3:
		if x == '.':
			count += 1
			array.append(x)
		else:
			array.append(x)

ip = ''.join(array)

with open('results.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["PORT", "STATE", "OTHER"])

for x in range(100, 124):
	print('analizando esta ip: ', ip + str(x))
	try:
		new_ip = ip + str(x)		
		for i in range (begin, end+1):

			res = scanner.scan(new_ip, str(i))

			res = res['scan'][new_ip]['tcp'][i]['state']

			print(f'port {i} is {res}.')
			print(scanner.csv())
			with open('results.csv', 'a', newline='') as file:
    				writer = csv.writer(file)
    				writer.writerow([f'{i}', f'{res}', scanner.csv()])
		print('------------------------------------------------------\n')
	except KeyError:
		print('No se encontró ningun puerto abierto en:', new_ip)
		print('------------------------------------------------------\n')


