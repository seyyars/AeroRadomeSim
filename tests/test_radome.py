import numpy as np
from aeroradomesim.radome_rf import layer, tmm_s21
def test_tmm_lossless_normal():
    f = np.linspace(2e9, 3e9, 5)
    stk = [layer(0.010, eps_r=2.5, tan_delta=0.0)]
    s21 = tmm_s21(f, stk, theta=0.0, pol="TE")
    assert (np.abs(s21) <= 1.0 + 1e-9).all()
