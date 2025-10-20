import numpy as np
g0=9.80665; R=287.05287; gamma=1.4; Pr=0.71
_mu_ref=1.716e-5; _T_ref=273.15; _Suth=110.4

def isa_atm(h: float):
    if h<=11000.0:
        T0=288.15; p0=101325.0; L=-0.0065
        T=T0+L*h; p=p0*(T/T0)**(-g0/(L*R))
    else:
        T11=216.65; p11=22632.06
        T=T11; p=p11*np.exp(-g0*(h-11000.0)/(R*T11))
    rho=p/(R*T); a=np.sqrt(gamma*R*T); return T,p,rho,a

def mu_air(T: float):
    return _mu_ref*(T/_T_ref)**1.5*(_T_ref+_Suth)/(T+_Suth)

def adiabatic_wall_temperature(T: float, M):
    r=Pr**(1/3); M=np.asarray(M); return T*(1.0+r*0.5*(gamma-1.0)*M*M)

def Cf_lam_avg(Re):  return 1.328/np.sqrt(np.maximum(Re,1e-12))
def Cf_turb_avg(Re): return 0.074/np.power(np.maximum(Re,1.0),0.2)
def Cf_blend(Re, Re_tr=5e5):
    Re=np.asarray(Re); w=1.0/(1.0+(Re/np.maximum(Re_tr,1.0))**2)
    return w*Cf_lam_avg(Re)+(1-w)*Cf_turb_avg(Re)

def mach_sweep(h=1000.0,M_min=0.0,M_max=3.0,N=201,L=1.2,Rb=0.2):
    T,p,rho,a=isa_atm(h); mu=mu_air(T); M=np.linspace(M_min,M_max,N)
    V=a*M; q=0.5*rho*V*V
    T0=T*(1+0.5*(gamma-1.0)*M*M)
    Taw=adiabatic_wall_temperature(T,M)
    Re_L=rho*V*L/np.maximum(mu,1e-12)
    Cf=Cf_blend(Re_L)/(1.0+0.12*M*M)  # تصحیح تراکم‌پذیری ملایم
    return {"M":M,"V":V,"q":q,"T0":T0,"Taw":Taw,"Re_L":Re_L,"Cf":Cf,"rho":rho,"a":a}
