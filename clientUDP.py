from socket import *
import time 
serverPort = 12000
M = 1024 #tamanho do pacote
buffer = [] #buffer com janela deslizante
N = 10 # tamanho do buffer


print ('Ready to receive')

# funções

def getResposta():
    msgResposta = serverSocket.recvfrom(M)
    print ("Server response: %s" % msgResposta[0])
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

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
numSeqAtual = 0
while True:
    print ('Waiting...⏳️')
    
    
    message, clientAddress = serverSocket.recvfrom(M)
    result = message.decode()
    print('Server message: '+ result)
    numSeqAtual = int(getNumSeq(result))
    response = createPacket(-1,"NULL", -1)

    if(len(buffer) < N ):
        if(len(buffer) > 0 and buffer[len(buffer)-1] + 1 != numSeqAtual): # caso nao venha na ordem
            proximoBit = (buffer[len(buffer)-1] + 1)*M             
        else: 
            buffer.append(numSeqAtual)
            proximoBit = (buffer[len(buffer)-1] + 1)*M            

    if(len(buffer) == N ):
        buffer.clear()
        response = createPacket(proximoBit,'ACK',len(buffer))
        serverSocket.sendto(response.encode(),clientAddress)
    time.sleep(0.2)
    # serverSocket.close()

print ('Closing socket...')
serverSocket.close()


