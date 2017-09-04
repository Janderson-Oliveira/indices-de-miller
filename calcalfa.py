#!/home/j/anaconda2/bin/python

"""
    Created on 09/2017
    
    Descricao: Calculo do parametro alfa.
    
    @autor:  Janderson <joliveira@lna.br>
    
    ################ ATENÇÃO ##################
    >> Este código ainda não esta finalizado <<
    ###########################################
     
    Simple usage example:
    
    ./calcalfa.py --amostras=amostras.txt --datafile=theta.txt --outputfile=melhorestimativa.txt
    """

__version__ = "1.0"

__copyright__ = """
    Copyright (c) ...  All rights reserved.
    """

import sys

from optparse import OptionParser

import numpy as np
import math


parser = OptionParser()

parser.add_option("-t", "--amostras", dest="amostras", help='Entre com o arquivo contendo os dados de cada amostra',type='string',default="")
parser.add_option("-i", "--datafile", dest="datafile", help='Entre com o arquivo contendo os dados experimentais',type='string',default="")
parser.add_option("-o", "--outputfile", dest="outputfile", help='Saida contendo as melhores estimativas',type='string',default="")
parser.add_option("-s", "--hkl", dest="hkl", help='Indices de Miller',type='string',default="777")
parser.add_option("-v", action="store_true", dest="verbose", help="verbose",default=0)


try:
    options,args = parser.parse_args(sys.argv[1:])
except:
    print "Erro: checar a forma de usar calcalfa.py -h ";sys.exit(1);

if options.verbose:
    print ': Entre com o arquivo contendo os dados experimentais', options.datafile
    print ': Saida contendo as melhores estimativas', options.outputfile
    print ': Indices de Miller', options.hkl



hkl = options.hkl
listathetas = np.loadtxt(options.datafile, unpack=True)
s1, s2, s3 = np.loadtxt(options.amostras, unpack=True)

saida=options.outputfile
#print listathetas


def cal_theta(amostra1 = s1, amostra2 = s2, amostra3 = s3):

    s1, s2, s3 = [],[],[]    
    for i in range(len(amostra1)):
        
        s1.append(amostra1[i])
        s2.append(amostra2[i])
        s3.append(amostra3[i])        
    
    saida_valores_theta = '#theta em graus' +  '\n'
    for amostra in range(len(s1)):
         
        k = (3.14/360.00)*57.30
        
        saida_valores_theta += str(round(k*s1[amostra],3)) +' '+ str(round(k*s2[amostra],3)) +' '+str(round(k*s3[amostra],3)) +  '\n'
        

    return saida_valores_theta

thetas = cal_theta(amostra1 = s1, amostra2 = s2, amostra3 = s3)
print thetas 

exit()

def Rad(numero): #esta funcao converte para radiano os valores de theta
    rad = (numero/180)*math.pi
    return rad

lista_sen2 = []
for theta in listathetas:
    sen2 = math.sin(Rad(theta))**2
    lista_sen2.append(sen2)
    #print sen2

#print lista_sen2   
h = 7
k = 7
l = 7


def calc_s_q_i(h,k,l): # calcula a soma dos quadrados dos indices
    
    soma = h**2 + k**2 + l**2
    
    lista_soma_quadrados_indices = range(soma)
    return lista_soma_quadrados_indices
#lista_indices = calcular_constante(hkl)
 
calc_k = calc_s_q_i(h,k,l)



def calcular_constantes(lista_sen2, calc_k):

    lista_k = calc_k
    resultado = []
    
    for k in lista_k:

        for i in range(len(lista_sen2)):
            s = k/lista_sen2[i]
            resultado.append(s)
    return resultado


k = calcular_constantes(lista_sen2, calc_k)
 

k = np.array(k)
mask = np.argsort(k)

lista_k = k[mask]



#for i in lista_k:
#    print i

outfilecontents = ''
for k in (lista_k):


    outfilecontents+= str(k)
    outfilecontents += '\n'
    
#print outfilecontents

outputfile =  options.outputfile

if outputfile :
	outfile = open(outputfile, 'w')
	outfile.write(outfilecontents )
	outfile.close()
else :
	print outfilecontents

##lambda = 1.54*10**(-8)

listak = np.loadtxt('/home/j/ic/quantica/k.txt', unpack=True)

listaproduto = '#SEN^2 X Const. = Produto' +  '\n'
for i in listak:
    
    for sen in range(len(lista_sen2)):
        produto = i*lista_sen2[sen]
    
        print produto


        listaproduto+= str(lista_sen2[sen]) + ' '+ ' X '+ ' ' + str(i) + ' '+ ' = '+ ' ' + str(produto)
        listaproduto += '\n' 
    
    



saida_produto =  "options.outputfile_produto.txt"

if outputfile :
	outfile = open(saida_produto, 'w')
	outfile.write(listaproduto)
	outfile.close()
else :
	print outfilecontents








