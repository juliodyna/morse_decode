'''
O Código Morse é um sistema de representação de letras, algarismos e sinais de pontuação através
de um sinal codificado enviado de modo intermitente. Foi desenvolvido por Samuel Morse em 1837, 
criador do telégrafo elétrico, dispositivo que utiliza correntes elétricas para controlar eletroímãs 
que atuam na emissão e na recepção de sinais. 
O script tem a finalidade de decifrar uma mensagem em código morse e salvá-la em texto claro.
'''

import os
import datetime
import sys
import pandas as pd
from config import dict_morse, file_path
import re

# from dotenv import load_dotenv # para variáveis de ambiente
# load_dotenv() # para carregar as variáveis de ambiente
# file_path = os.getenv("file_path")



def invert_dict(reverso):
    '''
    input: qualquer dicionário com chave e valor (neste caso de exemplo a chave é o código morse e o valor é o alfabeto)
    output: retorna o dicionario invertido
    '''
    return({v: k for k, v in reverso.items()}) #valor vira key e key vira valor


def adicionar_espaco_entre_letras(palavra):
    # Verifica se a palavra tem pelo menos duas letras
    if len(palavra) < 2:
        return palavra
    
    # Separa a última letra
    ultima_letra = palavra[-1]
    
    # Junta as letras com espaços, exceto a última
    letras_com_espaco = " ".join(palavra[:-1])
    
    # Adiciona a última letra sem espaço
    palavra_com_espaco = f"{letras_com_espaco} {ultima_letra}"
    
    return palavra_com_espaco

def code_morse_create(msg):
    '''
    input : mensagem alfa numerico com as letras e numeros separadas por espaços e palavras por Pipes
    output : palavra escrito em código morse A A | A .- .- | .-
    '''
    msg = msg.upper()
    msg = re.sub(r"\s+", "|", msg)
    msg = adicionar_espaco_entre_letras(msg)
    print(msg)
    msg_lst = msg.split(" ")
    msg_claro = [] 
    dict_reverso = invert_dict(dict_morse)
    for morse in msg_lst :
        if morse =="|":
            morse = ""
            msg_claro.append(morse)
        else:
            msg_claro.append(dict_reverso[morse])
        
    return " ".join(msg_claro)


def decode_morse(msg):
    '''
    input : mensagem em código morse com as letras separadas por espaços
    output : palavra escrito em letras e algarismos 
    '''
    print(msg)
    #msg = adicionar_espaco_entre_letras(msg)
    
    msg = msg.rstrip()
    msg = re.sub(r"\s\s+", " | ", msg)
    #print(msg)
    msg_lst = msg.split(" ")
    msg_claro = [] 
    for letter in msg_lst :
        if letter =="|":
            letter = " "
            msg_claro.append(letter)
        else:
            msg_claro.append(dict_morse[letter])
    return "".join(msg_claro)


def save_clear_msg_csv_hdr(msg):
    '''
    input : mensagem em código morse com as letras separadas por espaços
    output : palavra escrito em letras e algarismos, salva em arquivo csv
    '''
    now = datetime.datetime.now()
    msg_claro = decode_morse(msg)
    df = pd.DataFrame([[msg_claro, now,msg]], columns=["mensagem", "datetime", "morse"])
    hdr = not os.path.exists(file_path) # se o arquivo já existir, ele salva sem o cabeçalho, se não ele coloca
    df.to_csv(file_path, mode='a', index=False, header=hdr)
    ''' with open(file_path, 'a') as file:
        file.write(msg)'''


if __name__ == "__main__":
    
    frase = input("Digite uma frase: ")
    mensagem = code_morse_create(frase)
    save_clear_msg_csv_hdr(mensagem)
    #print(save_clear_msg_csv_hdr.__doc__)
    #print(pd.to_pickle.__doc__)
