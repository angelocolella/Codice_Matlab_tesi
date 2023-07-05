from numpy import * #Per alcune funzioni matematiche
from matplotlib.pyplot import * #Per grafici
import CoolProp.CoolProp as CP
import numpy


#Ciclo base R245fa

#Dati ingresso
fluido = 'R245fa'
Tcrit = 273.15+154  #K
Tcritcentigradi = 154   #°C
eta_t = 0.9
eta_c = 0.7

#Parametri termodinamici in SI

#Pt 1 uscita condensatore
T1 = 303
P1 = CP.PropsSI('P', 'T', T1, 'Q', 0, fluido)
s1 = CP.PropsSI('S', 'T', T1, 'Q', 0, fluido)

#Pt 2 uscita pompa
Tmax = 273.15+153
P2 = CP.PropsSI('P', 'T', Tmax, 'Q', 1, fluido)
s2 = 1138.916056813427
T2 = CP.PropsSI('T', 'P', P2, 'S', s2, fluido)

#Pt 2e (uscita prima parte caldaia, uscita vaporizzatore ingresso economizzatore), ovvero il punto di liquido satura a Tmax e Pmax
P2e = P2
T2e = Tmax
s2e = CP.PropsSI('S', 'P', P2e, 'Q', 0, fluido)

#Pt 3 (uscita caldaia, punto vapore saturo secco)
P3 = P2
T3 = Tmax
s3 = CP.PropsSI('S', 'P', P3, 'Q', 1, fluido)
h3 = CP.PropsSI('H', 'P', P3, 'Q', 1, fluido)

#Pt 4 (uscita turbina)
P4 = P1
s4 = 1789.804970637252
T4 = CP.PropsSI('T', 'P', P4, 'S', s4, fluido)



#Definizione curve saturazione piano T-s

#Curva liquido saturo

Tls = []
sls = []
Tls0 = 273.15  #K, temperatura partenza grafico
    
for i in range (Tcritcentigradi):
    Ti = Tls0 + i
    Tls.append(Ti-273.15)
    sls.append(CP.PropsSI ('S', 'T', Ti, 'Q', 0, fluido)/1000)

 
    
#Curva vapore saturo secco

Tvss = []
svss = []
Tvss0 = 273.15  #K, temperatura partenza grafico
    
for k in range (Tcritcentigradi):
    Tk = Tvss0 + k
    Tvss.append(Tk-273.15)
    svss.append(CP.PropsSI ('S', 'T', Tk, 'Q', 1, fluido)/1000)



#Trasformazione nella pompa 1-2, adiabatica
#Se le trasformazione fossero reversibili

h1 = 2.394056868884908*100000
s2is = s1

s12 = []
T12 = []

P12 = linspace(P1, P2, 100)


for i12 in range(len(P12)):
    h2is = CP.PropsSI('H', 'P', P12[i12], 'S', s2is, fluido)  

    #Sfrutto il rendimento eta_c = (h_2is-h_1)/(h_2-h_1) per determinare l'entalpia del punto 4 
    h2 = h1 + ((h2is-h1)/eta_c)       
    s12.append(CP.PropsSI('S', 'P', P12[i12], 'H', h2, fluido)/1000)  
    T12.append((CP.PropsSI('T', 'P', P12[i12], 'H', h2, fluido))-273.15)


#Trasformazione nella caldaia 2-2e-3
#Tradormazioni isobare

#2-2e

T2evs = CP.PropsSI('T', 'P', P2, 'Q', 0, fluido)
s2evs = CP.PropsSI('S', 'P', P2, 'Q', 0, fluido)
T22e_prov = linspace(T2, T2evs-0.1, 100)

T22e = []
s22e = []

for i22e in range(len(T22e_prov)):
    s22e.append(CP.PropsSI('S', 'P', P2, 'T', T22e_prov[i22e], fluido)/1000)
    T22e.append((T22e_prov[i22e])-273.15)
    if i22e == len(T22e_prov):
        s22e.append(s2evs/1000)
        T22e.append(T2evs-273.15)



#2e-3, da liquido saturo secco a vapore saturo secco a P2
T2e3 = [T2e-273.15, T3-273.15]
s2e3 = [s2e/1000, s3/1000]     


#Trasformazione turbina
#3-4
h4 = 4.374239146024928*100000

s34 = []
T34 = []



P34 = linspace(P3, P4, 500)


for i34 in range(len(P34)):
    s4is = s3
    h4is = CP.PropsSI('H', 'P', P34[i34], 'S', s4is, fluido)    

    #Sfrutto il rendimento di turbina eta_t=(h_3-h_4)/(h_3-h_4is) per determinare l'entalpia del punto 4 
    h4 = h3 - eta_t * (h3-h4is)        
    s34.append(CP.PropsSI('S', 'P', P34[i34], 'H', h4, fluido)/1000)  
    T34.append((CP.PropsSI('T', 'P', P34[i34], 'H', h4, fluido))-273.15)



#Trasformazione nel condensatore 4-1
#Tradormazione isobara P4 = P1
#4-1

T4ls = CP.PropsSI('T', 'P', P4, 'Q', 1, fluido)
s4ls = CP.PropsSI('S', 'P', P4, 'Q', 1, fluido)
T41_prov = linspace(T4ls+0.1, T4, 500)

s41 = []
T41 = []

for i41 in range(len(T41_prov)):
    s41.append(CP.PropsSI('S', 'P', P4, 'T', T41_prov[i41], fluido)/1000)
    T41.append((T41_prov[i41])-273.15)
    if i41 == len(T41_prov):
        s41.append(s4ls/1000)
        T41.append(T4ls-273.15)


T4ls1 = [T4ls-273.15 ,T1-273.15]
s4ls1 = [s4ls/1000, s1/1000]


coloreiso = '#0b1fa1'
colore = '#077a39'

font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 15}


matplotlib.rc('font', **font)
 
plot(sls, Tls, color = coloreiso)
plot(svss, Tvss, color = coloreiso)
plot(s12, T12, color = colore)
plot(s22e, T22e, color = colore)
plot(s2e3, T2e3, color = colore)
plot(s34, T34, color = colore)
plot(s41, T41, color = colore)
plot(s4ls1, T4ls1, color = colore)
title('Piano T-s ciclo base R245fa', fontdict=None, loc='center', pad=None)
xlabel('s [kJ/KgK]', fontsize = 18)
ylabel('T [C]', fontsize = 18)
grid(color='#808080', linestyle='--', linewidth=0.5)


pause(1e4) #Metto in pausa il programma così da poter vedere il grafico
