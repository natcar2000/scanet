import socket
import threading
import sys
import time


PARAMS = ['-e', '-m', '-p']
threads = []
hosts_ativos = []
portas_abertas = []


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
            time.sleep(3)
            print("+ Host escaneado com sucesso ... +")
    portas_abertas.clear()
    hosts_ativos.clear()
    return True


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


def conecta_a_portas_tcp(ipv4, porta):
    protocolo = resolve_servico(porta)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if s.connect_ex((ipv4, porta)) == 0:
        portas_abertas.append(porta)
        if protocolo == None:
            print(f"Porta {porta}/TCP: Aberta")
        else:
            print(f"Porta {porta}/TCP ({protocolo}): Aberta")
    s.close()
    return True


def resolve_servico(porta):
    protocolo = None
    try:
        servico = socket.getservbyport(porta)
        protocolo = servico
    except:
        pass
    finally:
        return protocolo


def pega_hosts_ativos(rede):
    for i in range(1, 255):
        t = threading.Thread(target=conecta_aos_hosts, args=(rede, i,))
        t.start()
        threads.append(t)
    for thread in threads:
        thread.join()
    threads.clear()
    return True


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
