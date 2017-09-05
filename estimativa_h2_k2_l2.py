#!/home/j/anaconda2/bin/python

"""
    Created on 09/2017
    
    Descricao: Estimativa dos indices de Miller para o experimento de Debye Scherrer, permitindo o calculo do parametro alfa.
    
    @autor:  Janderson <joliveira@lna.br>

    
    Simple usage example:
    
    ./estimativa_h2_k2_l2.py --medidas_de_S1=medidas_de_S1.txt --listathetas=lista_thetas1.txt
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

parser.add_option("-m", "--medidas_de_S1", dest="medidas_de_S1", help='Entre com o arquivo contendo os dados de S1 de cada amostra',type='string',default="")
parser.add_option("-f", "--listathetas", dest="listathetas", help='Entre com o arquivo contendo os valores dos angulos thetas',type='string',default="")
parser.add_option("-v", action="store_true", dest="verbose", help="verbose",default=0)


try:
    options,args = parser.parse_args(sys.argv[1:])
except:
    print "Erro: checar a forma de usar calcalfa.py -h ";sys.exit(1);

if options.verbose:
    print ': Arquivo contendo os dados de S1 de cada amostra', options.medidas_de_S1

    print ': Arquivo contendo os valores do angulo theta', options.listathetas




#ler arquivo que contem os valores de S1
s1_amostra1, s1_amostra2, s1_amostra3 = np.loadtxt(options.medidas_de_S1, unpack=True)

###########################################################################
################## funcao que converte S1 em theta (graus) ################
###########################################################################
def cal_theta(s1_amostra1, s1_amostra2, s1_amostra3):

    s1, s2, s3 = [],[],[]    
    for i in range(len(s1_amostra1)):
        
        s1.append(s1_amostra1[i])
        s2.append(s1_amostra2[i])
        s3.append(s1_amostra3[i])        
    
    saida_valores_theta1 = '#theta em graus' +  '\n'
    saida_valores_theta2 = '#theta em graus' +  '\n'
    saida_valores_theta3 = '#theta em graus' +  '\n'
    for amostra in range(len(s1)):
         
        c = (3.14/360.00)*57.30
        
        saida_valores_theta1 += str(round(c*s1[amostra],3)) + '\n'
        saida_valores_theta2 += str(round(c*s2[amostra],3)) + '\n'
        saida_valores_theta3 += str(round(c*s3[amostra],3)) + '\n'
            

    if saida_valores_theta1:
        outfile = open('lista_thetas1.txt', 'w')
        outfile.write(saida_valores_theta1)
        outfile.close()

        outfile = open('lista_thetas2.txt', 'w')
        outfile.write(saida_valores_theta2)
        outfile.close()

        outfile = open('lista_thetas3.txt', 'w')
        outfile.write(saida_valores_theta3)
        outfile.close()
    else :
	    print saida_valores_theta


    return saida_valores_theta1, saida_valores_theta2, saida_valores_theta3

###########################################################################
###########################################################################


thetas = cal_theta(s1_amostra1, s1_amostra2, s1_amostra3)
#print thetas 



## ler arquivo que contem os valores de theta calculados anteriormente
listathetas = np.loadtxt(options.listathetas, unpack=True)


###########################################################################
######### esta funcao calcula o quadrado do seno de angulo theta ##########
###########################################################################
def Rad(numero): 
    rad = (numero/180)*math.pi
    return rad

lista_sen2 = []
for theta in listathetas:
    sen2 = round(math.sin(Rad(theta))**2,2)
    lista_sen2.append(sen2)
    print "sen2:",sen2

#print lista_sen2   
############################################################################
############################################################################


# definimos valores maximos possiveis para os indices de Miller, o que 
# vai permitir criar um lisa com todos os possiveis valores para a soma
# dos quadrados dos indices de Miller

h = 6
k = 6
l = 6

###########################################################################
########## calcula a Soma dos Quadrados dos Indices (s_q_i) ###############
###########################################################################
def calc_s_q_i(h,k,l): 
    
    soma = h**2 + k**2 + l**2
    
    lista_soma_quadrados_indices = range(soma)
    return lista_soma_quadrados_indices

#lista_indices = calcular_constante(hkl)

##########################################################################
##########################################################################
 
lista_soma_quadrados_indices = calc_s_q_i(h,k,l)

##########################################################################
########### esta funcao efetua o produto entre SEN^2 e k #################
##########################################################################

def calcular_constantes(lista_sen2, lista_soma_quadrados_indices):

    
    constante = []
    
    for hkl in lista_soma_quadrados_indices:

        for i in range(len(lista_sen2)):
            cont = hkl/lista_sen2[i]
            constante.append(cont)
    return constante


##########################################################################
##########################################################################



##########################################################################
############ reorganizar os valores de hkl e salvar em .txt ##############
##########################################################################
calc_constante = calcular_constantes(lista_sen2, lista_soma_quadrados_indices)
 

calc_constante = np.array(calc_constante)
mask = np.argsort(calc_constante)

lista_h2_k2_l2 = calc_constante[mask]


salvar_lista_h2_k2_l2 = ''
for hkl in (lista_h2_k2_l2):


    salvar_lista_h2_k2_l2 += str(round(hkl,3))
    salvar_lista_h2_k2_l2 += '\n'
    
#print outfilecontents

nome_lista_h2_k2_l2= 'lista_h2_k2_l2'+options.listathetas
if salvar_lista_h2_k2_l2 :
	outfile = open(nome_lista_h2_k2_l2, 'w')
	outfile.write(salvar_lista_h2_k2_l2)
	outfile.close()
else :
	print salvar_lista_h2_k2_l2


###########################################################################
###########################################################################



# abrir uma nova lista contendo os valores de 

lista_h2_k2_l2 = np.loadtxt(nome_lista_h2_k2_l2, unpack=True)


##########################################################################
################ Calcular SEN^2 X Const. = Produto #######################
##########################################################################

listaproduto = '#SEN^2 X Const. = Produto' +  '\n'
for i in lista_h2_k2_l2:
    
    for sen in range(len(lista_sen2)):
        produto = i*lista_sen2[sen]
    
        #print produto


        listaproduto+= str(round(lista_sen2[sen],2)) + ' '+ ' X '+ ' ' + str(round(i,2)) + ' '+ ' = '+ ' ' + str(round(produto,2))
        listaproduto += '\n' 
    
    

saida_produto =  'calculo_SEN_x_Const_'+options.listathetas
if saida_produto :
	outfile = open(saida_produto, 'w')
	outfile.write(listaproduto)
	outfile.close()
else :
	print saida_produto

###########################################################################
###########################################################################




###########################################################################
### Encontrar os valores para as somas de h2 k2 l2 e o parametrso alfa ####
###########################################################################

lamb2 = (2.37*(10.00**(-20.))) # o quadrado do comprimento de onda

#print lamb2


# entrar com o valor encontrado pelo calculo de SEN_x_Const    
melhor_constante = raw_input("Digite o valor encontrado para a melhor estimativa para a constante: ") 

    

print melhor_constante

hkl = float(melhor_constante)
lista_alfa = []
for sen in range(len(lista_sen2)):
    
    c = []
    
    for s in range(len(lista_sen2)):
        
        int_c = round(hkl*lista_sen2[s],2)
        c.append(int(int_c))
  

    alfa = math.sqrt((lamb2*int(c[sen]))/(4.0*lista_sen2[sen]))

    a = alfa*(10.00**(10.))
    lista_alfa.append(a)
    print 'sen',lista_sen2[sen], 'alfa', round(a,2) 
    
print c
###########################################################################
###########################################################################



##########################################################################
################## Arquivo contendo os resultados  #######################
##########################################################################

lista_resultados = '# theta SEN^2  Const*SEN^2 (h2+k2+l2) alfa' +  '\n'
for s in range(len(lista_sen2)):
    

    lista_resultados+= str(round(listathetas[s],1)) +'	'+ str(round(lista_sen2[s],2)) + '	'+str(hkl*+lista_sen2[s])+ '		 ' + str(c[s]) + '	'+ str(round(lista_alfa[s],2))
    lista_resultados += '\n' 
    
    

saida_resultado =  'saida_resultado_'+options.listathetas
if lista_resultados :
	outfile = open(saida_resultado, 'w')
	outfile.write(lista_resultados)
	outfile.close()
else :
	print saida_produto


###########################################################################
############################### FIM #######################################
###########################################################################





