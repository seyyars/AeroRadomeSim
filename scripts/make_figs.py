import numpy as np, matplotlib.pyplot as plt
from aeroradomesim.aero import mach_sweep
from aeroradomesim.radome_rf import layer, tmm_s21

# Fig 1: q vs Mach
res = mach_sweep(h=1000.0, N=201)
M, q = res["M"], res["q"]
plt.figure(); plt.plot(M, q); plt.grid(True)
plt.xlabel("Mach"); plt.ylabel("q (Pa)")
plt.title("Dynamic pressure vs Mach @ 1 km")
plt.savefig("docs/img/q_vs_mach.png", dpi=160, bbox_inches="tight")

# Fig 2: |S21|(f,T) heatmap (نمونهٔ دو دما)
f = np.linspace(1.5e9, 3.5e9, 350)
def eps_r(T): return 3.8 + 1.5e-3*(T-300.0)
def tan_d(T): return 2e-3 + 2e-5*(T-300.0)
Ts = [300.0, 420.0]
plt.figure()
for T in Ts:
    stk = [layer(0.010, eps_r=eps_r(T), tan_delta=tan_d(T))]
    s21 = tmm_s21(f, stk, theta=0.0, pol="TE")
    plt.plot(f*1e-9, 20*np.log10(np.abs(s21)), label=f"T={T:.0f}K")
plt.xlabel("Frequency (GHz)"); plt.ylabel("|S21| (dB)"); plt.grid(True); plt.legend()
plt.title("Radome transmission vs frequency (two temperatures)")
plt.savefig("docs/img/radome_s21.png", dpi=160, bbox_inches="tight")
