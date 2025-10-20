import numpy as np
from aeroradomesim.radome_rf import layer, tmm_s21

def test_tmm_lossless_normal_power_le_1():
    f = np.linspace(2e9, 3e9, 7)
    stk = [layer(0.010, eps_r=2.5, tan_delta=0.0)]
    t = tmm_s21(f, stk, theta=0.0, pol="TE", n0=1.0, nL=1.0)

    # در نرمال اینسیدنس هوا→هوا: q0 = qL = 1 (نسبتاً)، پس T = |t|^2
    T = np.abs(t)**2
    assert (T <= 1.0 + 1e-9).all()
    assert (T >= -1e-12).all()
