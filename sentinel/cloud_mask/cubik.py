#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.interpolate import interp1d

# calculate 5 natural cubic spline polynomials for 6 points
# (x,y) = (0,12) (1,14) (2,22) (3,39) (4,58) (5,77)
x = np.array([0, 13, 20, 40,53,	63, 83,	85,	90,	98,	100,	103,	105,	108,	110,	113,	118,	135,	138,	140,	145,	148,	150,	173,	175,	178,	203])
y = np.array([0.538148480950998,0.754584663096723,	0.735769074384378,	0.746693651265003,0.780442943631995,0.643364823947639, 0.189254864080764,	0.173197031903253,	0.18253182657897,	0.188146451981418,	0.177265684561636,	0.183513603615882,	0.187256661906394,	0.176390687873623,	0.174791691117031,	0.17672111321259,	0.186876515189589,	0.116507590507189,	0.118271142848379,	0.13439899385651,	0.154239064450529,	0.213714299548289,	0.193403089513723,	0.108986611448488,	0.14142954193976,	0.145392120433177,	0.080757903203055])

x1 = np.array([0, 13, 20, 40,53,	63, 83,	85,	90,	98,	100,	103,	105,	108,	110,	113,	118,	135,	138,	140,	145,	148,	150,	173,	175,	178,	203])
y1 = np.array([0.638148480950998,0.854584663096723,	0.835769074384378,	0.846693651265003,0.880442943631995,0.743364823947639, 0.289254864080764,	0.273197031903253,	0.28253182657897,	0.288146451981418,	0.277265684561636,	0.283513603615882,	0.287256661906394,	0.276390687873623,	0.274791691117031,	0.27672111321259,	0.286876515189589,	0.216507590507189,	0.218271142848379,	0.23439899385651,	0.254239064450529,	0.213714299548289,	0.193403089513723,	0.108986611448488,	0.14142954193976,	0.145392120433177,	0.080757903203055])


#x = np.array([103,183,199,215,247,263])
#y = np.array([0.092924924,0.6973349676,0.591438389,0.3648472544,0.1842870447,0.2033718735]) ------- 2015

# x = np.array([202,218,234,250,298])
# y = np.array([0.7145816883,0.7877757606,0.7173789292,0.6582763842,0.2095308463]) ------------------ 2016


# x = np.array([117,137,157,170,180,192,202,207,215,217,220,222,225,227,230,235,252,255,257,262,265,267,290,292,320])
# y = np.array([0.11715954784902,0.258859531316896,0.620692835454185,0.722128682889928,0.674575087919654,0.605901657839146,0.418340253583404,0.242824619018595,0.195003763345711,0.181382943481083,0.184990341624159,0.169906129424399,0.153060686203508,0.149583156716902,0.147293766834139,0.158694937704404,0.066207336191915,0.099016403364609,0.100874580754954,0.092815102583713,0.113097415409369,0.109564836802331,0.104706220609199,0.14963853055789,0.189578584889643])
# ------------- 2017

# calculate natural cubic spline polynomials
cs = CubicSpline(x,y,bc_type='natural')
cs1 = CubicSpline(x,y,bc_type='not-a-knot')
cs2 = CubicSpline(x,y,bc_type='clamped')

linear = interp1d(x, y)
cubik = interp1d(x, y,'cubic')
cubik1 = interp1d(x1, y1,'cubic')


linear1 = interp1d(x, y,'linear')
slinear1 = interp1d(x, y,'slinear')
quadrat = interp1d(x, y,'quadratic')
# print (linear(144))
# show values of interpolation function at x=1.25
# print('S(144.25) = ', cs(144), ' ',cs(10))


different=x[-1]-x[0]
# s=np.arange(0,different)
s3=[] #for cubik spline
s30=[] #for cubik1 spline



s31=[] #for cubik spline
s32=[] #for cubik splin

s1=[] #for linear interpolation
s2=[] #for cubic interpolation
l1=[] #for linear interpolation new
sl1=[] #for slinear interpolation
qu=[] #for quadratic interpolation
xnew=[]
xnew1=[]
for i in range(different):

    data=x[0]+i+1
    data1 = x1[0] + i + 1
    xnew.append(data)
    xnew1.append(data1)

    # print(cs(data))
    s1.append(linear(data))
    s2.append(cubik(data))
    s3.append(cs(data)) # index massive s - i = 1 (i=100, s[i]=99)
    s30.append(cubik1(data1))  # index massive s - i = 1 (i=100, s[i]=99)


    s31.append(cs1(data)) # different cubic bc_type
    s32.append(cs2(data)) # different cubic bc_type

    l1.append(linear1(data))
    sl1.append(slinear1(data))
    qu.append(quadrat(data))
    # s3[i]=cs(data)
    # print(s3[i])

#plt.set_label('fo')

plt.plot(x, y, 'o', xnew, s3, '-',label='sine')

plt.plot(x1, y1, 'o', xnew1, s30, '-',label='sine1')
plt.legend()
plt.show()
# Cubic spline interpolation calculus example
    #  https://www.youtube.com/watch?v=gT7F3TWihvk

