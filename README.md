# AeroRadomeSim
Numerical simulation of Mach-0–3 aerothermodynamics and temperature-dependent radome RF transmission (Python).

## Install (dev)
pip install -e . pytest

## Quickstart
```python
from aeroradomesim.aero import mach_sweep
from aeroradomesim.radome_rf import layer, tmm_s21
res = mach_sweep(h=1000.0, N=51)
print(res["q"][:3])
s21 = tmm_s21([2.4e9], [layer(0.010, eps_r=3.0, tan_delta=0.0)], theta=0.0, pol="TE")
print(abs(s21[0]))
![](docs/img/q_vs_mach.png)  ![](docs/img/radome_s21.png)
