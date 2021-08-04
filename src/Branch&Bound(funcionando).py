import pulp
import math 
import random
import json
import time
# problema: o programa está repetindo restrições e não consegue sair desse loop
#--------------------------------------------------------------------------------
def asterisco():
    print('**************************************')
ix = []
iy = []
it = []
sinal = []
opcao = ''
st = pai =[]
p = 0
originalx = 0
originalz = 0
originaly = 0
#--------------------------------------------------------------------------------
while opcao != 'MIN' and opcao != 'MAX':
    opcao = str(input('Informe o obejtivo da FO [MAX/MIN]: ')).strip().upper()
if opcao == 'MIN':
    original = pulp.LpProblem('Problema', pulp.LpMinimize)
elif opcao == 'MAX':
    original = pulp.LpProblem('Problema', pulp.LpMaximize)
x = pulp.LpVariable("x", lowBound = 0)   
y = pulp.LpVariable("y", lowBound = 0) 
xp = float(input('Informe o coeficiente x da FO: '))
yp = float(input('Informe o coeficiente y da FO: '))
original += xp * x + yp * y 
ne = int(input('Informe o numero de restriçoes: '))
print('\n')
w = 0

for i in range(0,ne):
    print(f'{i+1}º RESTRIÇÃO-------') 
    ix.append(float(input('Informe o coeficiente de x: ')))
    iy.append(float(input('Informe o coeficiente de y: ')))     
    it.append(float(input('Informe o termo independente: ')))
    sinal.insert(i,str(input('Informe o sinal da restriçao [>= ou = ou <=]: ' )))
    print('\n')
inicio = time.time()
for j in range(0,ne):
    if sinal[j] == '>=':
        original += ix[j] * x + iy[j] * y >= it[j]
    elif sinal[j] == '=':
        original += ix[j] * x + iy[j] * y == it[j]
    elif sinal[j] == '<=':
        original += ix[j] * x + iy[j] * y <= it[j]

asterisco()
print(original)
status = original.solve()    
print(pulp.LpStatus[status])    
print(f'O valor de Z = {pulp.value(original.objective)}\nO valor de X = {pulp.value(x)}\nO valor de Y = {pulp.value(y)}')
if pulp.LpStatus[status] != 'Optimal':
    print('Resultado NÃO é ótimo')
if pulp.value(x).is_integer() == False or pulp.value(y).is_integer() == False:
    if pulp.LpStatus[status] == 'Optimal':
        pai.append(original)
originaly = pulp.value(y)
originalz = pulp.value(original.objective)
originalx = pulp.value(x)
print('\n')
#-----------------------------------------------------
incub = 0
incubx = 0 
incuby = 0
nix = 0
niy = 0
ex = 0
ey = 0
e = 0
p=1
contador = 0
tx = []
ty = []
mx = []
my = []
escolhax = 0
escolhay = 0
#-----------------------------------------------------
while pai:
    branch = pai[0]
    temp = branch.copy()
    temp.solve()
    pai.remove(branch)
    if pulp.value(x).is_integer() == False:
        nix = pulp.value(x)
        ex = 1
    if pulp.value(y).is_integer() == False: 
        niy = pulp.value(y)
        ey = 2
    escolhas = [ex,ey]
    if  pulp.value(y).is_integer() == False and pulp.value(x).is_integer() == False:
        e = random.choice(escolhas)
        if e == 1:
            if math.floor(nix) !=0:
                temp += 1 * x  <= math.floor(nix)
                escolhax = 1
        elif e==2:
            if  math.floor(niy) !=0:
                temp += 1 * y  <= math.floor(niy)
                escolhay = 1
    elif pulp.value(x).is_integer() == False:
        temp += 1 * x  <= math.floor(nix)
        escolhax = 1
    elif pulp.value(y).is_integer() == False:
        temp += 1 * y  <= math.floor(niy)
        escolhay = 1
    print(f'{p}º ITERAÇÃO------------------') 
    print(temp)
    status= temp.solve()    
    print(pulp.LpStatus[status])    
    print(f'O valor de Z = {pulp.value(temp.objective)}\nO valor de X = {pulp.value(x)}\nO valor de Y = {pulp.value(y)}')
    p+=1
    if pulp.value(x).is_integer() == True and pulp.value(y).is_integer() == True and pulp.LpStatus[status] == 'Optimal':
        if pulp.value(temp.objective) > incub:
            incub = pulp.value(temp.objective)
            incubx = pulp.value(x)
            incuby = pulp.value(y)
    if incub > pulp.value(temp.objective):
        continue
    elif incub < pulp.value(temp.objective) and incub > 0 and pulp.LpStatus[status] == 'Optimal':
        pai.append(temp)
    elif (pulp.value(x).is_integer() == False or pulp.value(y).is_integer() == False) and pulp.LpStatus[status] == 'Optimal':
        if escolhax == 1 and math.floor(nix) not in tx:
            pai.append(temp)
        elif escolhay == 1 and math.floor(niy) not in ty:
            pai.append(temp)
    tx.append(math.floor(nix))
    ty.append(math.floor(niy))
    escolhax = 0
    escolhay = 0
#-------------------------------------------------------------------------
    temp = branch.copy()
    temp.solve()
    if e > 0:
        if e == 1 and temp != 1 * x  >= math.ceil(nix):
            temp += 1 * x  >= math.ceil(nix)
            escolhax = 1
        elif e==2 and temp != 1 * y  >= math.ceil(niy):
            temp += 1 * y  >= math.ceil(niy)
            escolhay = 1
    elif pulp.value(x).is_integer() == False:
        temp += 1 * x  >= math.ceil(nix)
        escolhax = 1
    elif pulp.value(y).is_integer() == False:
        temp += 1 * y  >= math.ceil(niy)
        escolhay = 1
    asterisco()
    print(temp)
    status= temp.solve()    
    print(pulp.LpStatus[status])    
    print(f'O valor de Z = {pulp.value(temp.objective)}\nO valor de X = {pulp.value(x)}\nO valor de Y = {pulp.value(y)}')
    if pulp.value(x).is_integer() == True and pulp.value(y).is_integer() == True and pulp.LpStatus[status] == 'Optimal':
        if pulp.value(temp.objective) > incub:
            incub = pulp.value(temp.objective)
            incubx = pulp.value(x)
            incuby = pulp.value(y)
    if incub > pulp.value(temp.objective):
        continue
    elif incub < pulp.value(temp.objective) and incub > 0 and pulp.LpStatus[status] == 'Optimal':
        if math.ceil(nix) not in tx:
            pai.append(temp)
        elif math.ceil(niy) not in ty:
            pai.append(temp)
    elif (pulp.value(x).is_integer() == False or pulp.value(y).is_integer() == False) and pulp.LpStatus[status] == 'Optimal':
        if escolhax == 1 and math.ceil(nix) not in tx:
            pai.append(temp)
        elif escolhay == 1 and math.ceil(niy) not in ty:
            pai.append(temp)
    tx.append(math.ceil(nix))
    ty.append(math.ceil(niy))
    nix=0
    niy=0
    escolhax = 0
    escolhay = 0 
asterisco()
tempo =time.time()-inicio
if incub == 0:
    print(f'A solução ótima Z = {originalz}')
    print(f'X = {originalx}')
    print(f'Y = {originaly}')
    print('Tempo:',tempo,'s') 
else: 
    print(f'A solução ótima Z = {incub}')
    print(f'X = {incubx}')
    print(f'Y = {incuby}')
    print('Tempo:',tempo,'s')           


