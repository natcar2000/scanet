# Programa: scanet v1.0
# Descrição: Pequeno scanner de redes locais
# Desenvolvedor: Natanael Rodrigues
# Email: natanrod965@gmail.com
# Github: https://github.com/natcar2000


import socket
import threading
import sys
import time


PARAMS = ['-e', '-m', '-p']
threads = []
hosts_ativos = []
portas_abertas = []


# Função principal do programa, que realiza ações conforme os parâmetros passados pelo usuário
def main(alvo):
    if sys.argv[1] == PARAMS[0]:
        print(f"+ Escaneando a rede {alvo}... +\n")
        time.sleep(3)
        pega_hosts_ativos(alvo)
        hosts_ativos.sort()
        print(hosts_ativos)
        time.sleep(3)
        print("+ Rede escaneada com sucesso... +")
    elif sys.argv[1] == PARAMS[1]:
        if sys.argv[3] == PARAMS[2]:
            print(f"+ Escaneando o host {alvo}... +")
            time.sleep(3)
            pega_portas_abertas(alvo)
            portas_abertas.sort()
            for porta_aberta in portas_abertas:
                protocolo = resolve_servico(porta_aberta)
                if protocolo == None:
                    print(f"Porta {porta_aberta}/TCP: Aberta")
                else:
                    print(f"Porta {porta_aberta} ({protocolo})/TCP: Aberta")
            time.sleep(3)
            print("+ Host escaneado com sucesso ... +")
    portas_abertas.clear()
    hosts_ativos.clear()
    return True


# Função que retorna em uma lista todos os hosts ativos em uma rede
def conecta_aos_hosts(rede, host):
    ipv4 = f'{rede}.{host}'
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ipv4, 65535))
    except TimeoutError as erro:
        pass
    except ConnectionRefusedError as erro:
        hosts_ativos.append(ipv4)
    finally:
        s.close()
    return True


# Função responsável por tentar estabelecer uma conexão TCP com cada porta especificada pelo usuário
def conecta_a_portas_tcp(ipv4, porta):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if s.connect_ex((ipv4, porta)) == 0:
        portas_abertas.append(porta)
    s.close()
    return True


# Função responsável por tentar identificar o serviço de uma porta especificada pelo usuário
def resolve_servico(porta):
    protocolo = None
    try:
        servico = socket.getservbyport(porta)
        protocolo = servico
    except:
        pass
    finally:
        return protocolo


# Função que implementa o escaneamento de hosts
def pega_hosts_ativos(rede):
    for i in range(1, 255):
        t = threading.Thread(target=conecta_aos_hosts, args=(rede, i,))
        t.start()
        threads.append(t)
    for thread in threads:
        thread.join()
    threads.clear()
    return True


# Função que implementa o mapeamento de portas
def pega_portas_abertas(ipv4):
    lista_de_portas = sys.argv[4].split(',')
    for porta in lista_de_portas:
        t = threading.Thread(target=conecta_a_portas_tcp, args=(ipv4, int(porta),))
        t.start()
        threads.append(t)
    for thread in threads:
        thread.join()
    threads.clear()
    return True


main(sys.argv[2])
