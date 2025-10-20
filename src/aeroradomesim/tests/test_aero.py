from aeroradomesim.aero import mach_sweep
def test_aero_basic():
    res = mach_sweep(h=1000.0, N=11)
    assert (res["q"] >= 0).all()
    assert res["M"].size == 11
