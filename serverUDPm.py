from socket import *
import time 


# funções

def getResposta():
    msgResposta = serverSocket.recvfrom(M)
    print ("Resposta do Client: %s" % msgResposta[0])
    return msgResposta[0]

def getNumSeq(packet):
    packetSplit = packet.split(',')
    return packetSplit[0]
    
def createPacket(numSeq, msg, bufferFill):
    packet  = ''
    packet += str(numSeq) 
    packet += ',' 
    packet += str(msg)
    packet += ',' 
    packet += str(bufferFill)
    return packet

#variáveis globais

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverPort = 12000
serverSocket.bind(('', serverPort))
M = 1024 #tamanho do pacote
buffer = [] #buffer com janela deslizante
N = 10 # tamanho do buffer
numSeqAtual = 0
timeoutCount = 0
primeiraExecucao = True

while True:
    try:
        if(primeiraExecucao):
            print ('Pronto para receber')
            primeiraExecucao = False
        proximoBit = 0
        message, clientAddress = serverSocket.recvfrom(M)
        result = message.decode()
        #print('Mensagem client: '+ result)
        numSeqAtual = int(getNumSeq(result))
        response = createPacket(-1,"NULL", -1)
    
        if(len(buffer) < N ):
            if(len(buffer) > 0 and buffer[len(buffer)-1] + 1 != numSeqAtual): # caso nao venha na ordem
                proximoBit = (buffer[len(buffer)-1] + 1)*M  
                response = createPacket(proximoBit,'ACK', N - len(buffer))
                serverSocket.sendto(response.encode(),clientAddress)           
            else: 
                buffer.append(numSeqAtual)
                proximoBit = (buffer[len(buffer)-1] + 1)*M   
                response = createPacket(proximoBit,'ACK', N - len(buffer))         
        

        if(len(buffer) == N ):
            buffer.clear()
            response = createPacket(proximoBit,'ACK', N - len(buffer))
            serverSocket.sendto(response.encode(),clientAddress)
    except: 
        timeoutCount += 1        
        print('Timeout ' + str(timeoutCount))
        if(timeoutCount >= 3):
            break
        serverSocket.sendto(response.encode(),clientAddress) 
    serverSocket.settimeout(10)
print ('Fechando socket do server...')
serverSocket.close()



