# this module will be imported in the into your flowgraph
import numpy as np
import math

def filtroNyquist(Sps,ntaps):
    k=np.linspace(-ntaps/2,ntaps/2-1,ntaps)
    h=np.sinc(k/Sps)
    return h

#######################################################
##               Forma Coseno Alzado                 ##
#######################################################                       
def rcos(Sps,ntaps,beta):
    if beta==0:
        h=nyq(Sps,ntaps)
    else:
        h=ntaps*[0,]
        for n in range(ntaps):
            k=n-ntaps/2. # esto es para que h[n] quede centrada en la mitad del vector
            if abs(k)==Sps/(2.*beta):
                h[n]=np.sinc(1./(2.*beta))*math.pi/4.
            else:
                h[n]=np.sinc(k/Sps)*math.cos(beta*k*math.pi/Sps)/(1.-(2.*beta*k/Sps)**2)                
    Amp=np.amax(h)
    return h/Amp
