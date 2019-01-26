import math
pai= math.pi
A= 0.040380
dA= 0.000021
g= ((4*pai**2))/A
dg= ((4*pai**2)*dA)/(A**2)
print(g, dg)



pai= math.pi
sqart= math.sqrt
g_list=[977.67, 971.3, 977.67]
gtheo= 981
dgtheo= 10
dg_list=[0.51, 1.5, 0.73]

for x in range(0, len(g_list)):
    Nsigma= (g_list[x] - gtheo)/(sqart(dg_list[x]**2+dgtheo**2))
    print('Nsigma for', x, 'is', Nsigma)
    print('dg/g*100%=', (dg_list[x]/g_list[x])*100)