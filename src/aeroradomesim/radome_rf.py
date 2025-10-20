import numpy as np

def layer(thickness, eps_r, tan_delta=0.0):
    return {"d": float(thickness), "eps": complex(eps_r*(1-1j*tan_delta))}

def _snell(theta0, n0, n1):
    s=np.sin(theta0)*(n0/n1); s=np.clip(s,-1.0,1.0); return np.arcsin(s)

def _Z(pol, n, theta):
    return (np.cos(theta)/n) if pol.upper()=="TE" else (1.0/(n*np.cos(theta)))

def _M(k0, n, d, theta, pol):
    Z=_Z(pol,n,theta); beta=k0*n*np.cos(theta); c=np.cos(beta*d); s=1j*np.sin(beta*d)
    return np.array([[c,1j*Z*s],[1j*s/Z,c]],dtype=complex)

def tmm_s21(f, stack, theta=0.0, pol="TE", n0=1.0, nL=1.0):
    f=np.atleast_1d(f); c0=299792458.0; k0=2*np.pi*f/c0; pol=pol.upper()
    thetas=[float(theta)]; ns=[n0]
    for L in stack:
        ns.append(np.sqrt(L["eps"])); thetas.append(_snell(thetas[-1], ns[-2], ns[-1]))
    ns.append(nL); thetas.append(_snell(thetas[-1], ns[-2], ns[-1]))
    S21=np.zeros_like(f,dtype=complex)
    for i,k in enumerate(k0):
        Mtot=np.eye(2,dtype=complex)
        for j,L in enumerate(stack, start=1):
            Mtot = Mtot @ _M(k, ns[j], L["d"], thetas[j], pol)
        Z0=_Z(pol,ns[0],thetas[0]); ZL=_Z(pol,ns[-1],thetas[-1])
        A,B,C,D=Mtot.ravel(); S21[i]=2.0/(A+B/ZL+C*Z0+D*Z0/ZL)
    return S21
