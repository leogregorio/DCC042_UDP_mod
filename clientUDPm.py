from socket import *
import numpy as np
import time

# funções

def getResposta():
    msgResposta = clientSocket.recvfrom(M)
    print ("Resposta do Server: %s" % msgResposta[0])
    return msgResposta[0]

def getProxBit(packet):
    packetSplit = packet.split(b',')
    return int(packetSplit[0].decode())

def getWindowSize(packet):
    packetSplit = packet.split(b',')
    return int(packetSplit[2].decode())
    
def createPacket(numSeq, msg):
    packet  = ''
    packet += str(numSeq) 
    packet += ',' 
    packet += str(msg)
    return packet

def createSegment(fileSize, packetSize):       
    if(fileSize%packetSize == 0):
        tamanho = fileSize/packetSize
    else:
        tamanho = fileSize/packetSize + 1
    segment = np.empty(int(tamanho), dtype = tuple)# acked, first B
    for i in range(0,len(segment)):
        segment[i] = [False, packetSize*i]
    return segment


#variáveis globais

serverName = "localhost"
serverPort = 12000
fileSize   = 15*1024*1024 #arquivo de 15kB
M = 1024 #tamanho do pacote
buffer = [] #buffer com janela deslizante
N = 10 # tamanho do buffer
clientSocket = socket(AF_INET,SOCK_DGRAM)
numSeqAtual = 0
buffer = [ 0 , N-1] # inicio , fim
segment = createSegment(fileSize, M)
windowSizeRcvr = N 
clientSocket = socket(AF_INET,SOCK_DGRAM)


while numSeqAtual <= len(segment):    

    maxEnvio = N
    if( (buffer[1] - buffer[0] + 1) > windowSizeRcvr):
        maxEnvio = buffer[0] + windowSizeRcvr + 1
    else:
        maxEnvio = buffer[1] + 1

    for i in range(buffer[0], maxEnvio):
        packetToSend = createPacket(numSeqAtual, segment[i][1])
        clientSocket.sendto(packetToSend.encode(),(serverName,serverPort))
        numSeqAtual += 1

    resposta = getResposta()
    proxBit = getProxBit(resposta) 
    #dados da resposta
    windowSizeRcvr = getWindowSize(resposta)
    primeiroBit = buffer[0]*M
    acked = int((proxBit - primeiroBit)/M) # quantos pacotes foram ACKed
    ultimoACK = (proxBit / M) # 2048, ACK

    #desliza o lado esquerdo da janela
    for i in range(acked):
        segment[buffer[0]][0] = True
        if(buffer[0] < len(segment) - 1 ):
            buffer[0] += 1
        
    #desliza o lado direito da janela    
    if(buffer[1] + acked > len(segment) - 1):
        buffer[1] = len(segment) - 1
    else:
        buffer[1] += acked  

    ultimo = segment[len(segment) - 1]
    if(bool(ultimo[0]) == True):
        clientSocket.close()
        print ('Fechando socket do client...')
        break
    
    
