# scripts/make_figs.py
import numpy as np, matplotlib.pyplot as plt
from pathlib import Path
from aeroradomesim.aero import mach_sweep
from aeroradomesim.radome_rf import layer, tmm_s21

out = Path("docs/img"); out.mkdir(parents=True, exist_ok=True)

# شکل 1: q بر حسب Mach
res = mach_sweep(h=1000.0, N=201)
M, q = res["M"], res["q"]
plt.figure(); plt.plot(M, q); plt.grid(True)
plt.xlabel("Mach"); plt.ylabel("q (Pa)")
plt.title("Dynamic pressure vs Mach @ 1 km")
plt.savefig(out/"q_vs_mach.png", dpi=160, bbox_inches="tight")

# شکل 2: |S21|(f) برای دو دما
f = np.linspace(1.5e9, 3.5e9, 350)
eps_r = lambda T: 3.8 + 1.5e-3*(T-300.0)
tan_d = lambda T: 2e-3 + 2e-5*(T-300.0)
for T in (300.0, 420.0):
    s21 = tmm_s21(f, [layer(0.010, eps_r(T), tan_d(T))], theta=0.0, pol="TE")
    plt.figure(); plt.plot(f*1e-9, 20*np.log10(np.abs(s21))); plt.grid(True)
    plt.xlabel("Frequency (GHz)"); plt.ylabel("|S21| (dB)")
    plt.title(f"Radome transmission vs frequency (T={T:.0f} K)")
    plt.savefig(out/f"radome_s21_T{int(T)}K.png", dpi=160, bbox_inches="tight")

print("Saved figures to:", out.resolve())
