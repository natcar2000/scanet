# Importa bibliotecas necessárias 
from sys import argv  
from scapy.all import srp, Ether, ARP
from scapy.all import IP, TCP, sr

# Usuário escolhe a opção de varredura e o alvo (rede/host)
scan_option = argv[1]
alvo = argv[2]

# Função para descoberta de hosts, recebe a rede a ser mapeada como argumento e retorna todos os hosts encontrados
def enumera_hosts(rede):
    hosts = []
    arp = ARP()
    arp.pdst = rede
 
    ether = Ether()
    ether.dst = 'ff:ff:ff:ff:ff:ff'
    
    pck = ether / arp
    ips = srp(pck, timeout=10, verbose=1)[0]
    for ip in ips:
        hosts.append(ip[1].psrc)

    return hosts

# Função para escaneamento de portas, recebe o host a ser mapeado
def mapeia_portas(host, portas):
    multiplas_portas = []
    ip = IP()
    ip.dst = host

    tcp = TCP() 

    if '-' in portas:
        ports_list = portas.split('-') 
        multiplas_portas.append(int(ports_list[0]))
        multiplas_portas.append(int(ports_list[1]))
        tcp.dport = (multiplas_portas[0], multiplas_portas[1])

    elif ',' in portas:
        ports_list = portas.split(',')
        for i in range(len(ports_list)):
            multiplas_portas.append(int(ports_list[i]))
        tcp.dport = multiplas_portas

    else:
        tcp.dport = int(portas)
        
    tcp.flags = 'S'

    pck = ip / tcp
    response1, response2 = sr(pck, timeout=200, verbose=1)
    print('Host: {}\n'.format(host))
    for r1, r2 in response1:
        status = r2[TCP].flags
        porta = r1[TCP].dport
        if status == 'SA':
            print('{0}/TCP: Open'.format(porta))
        else:
            print('{0}/TCP: Closed'.format(porta))

    if len(multiplas_portas) > 0:
        multiplas_portas.clear()

    return '\nScan de portas concluído com sucesso!\n'
           
# Procedimento principal, executa as funções de descoberta de hosts/escaneamento de portas
def main():
    if scan_option == '-e':
        hosts = enumera_hosts(alvo)
        for host in hosts:
            print(host) 
    
    elif scan_option == '-m':
        if argv[3] == '-p':
            port_scan = mapeia_portas(alvo, argv[4])
            print(port_scan)
        else:
            print('Não foi possível escanear as portas.')

    else:
        print('Opção de escaneamento inválida.')

main()
