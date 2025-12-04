from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

# پوشه‌ی خروجی برای شکل‌ها (نسبت به همین فایل)
OUT = Path(__file__).parent / "figures"
OUT.mkdir(exist_ok=True)

# -----------------------
# 1) دما روی دیواره vs Mach
# -----------------------
gamma = 1.4          # نسبت گرمای ویژه هوا
T_inf = 288.0        # دمای آزاد [K]
r = 0.9              # ضریب ریکاوری

M = np.linspace(0.0, 3.0, 200)
T0 = T_inf * (1.0 + (gamma - 1.0) / 2.0 * M**2)
Tw = T_inf + r * (T0 - T_inf)   # دمای معادل دیواره

plt.figure()
plt.plot(M, Tw)
plt.xlabel("Mach number")
plt.ylabel(r"Wall temperature $T_w$ [K]")
plt.title("Wall temperature vs Mach number")
plt.grid(True)
plt.tight_layout()
plt.savefig(OUT / "temperature_vs_mach.pdf")
plt.close()

# -----------------------
# 2) تلفات عبور RF vs Mach
# -----------------------

# مدل ساده وابستگی دی‌الکتریک به دما
eps0 = 4.0           # epsilon' در دمای مرجع
tan_delta0 = 0.002   # loss tangent در دمای مرجع
T_ref = 300.0        # دمای مرجع [K]
a_eps = 2e-3         # حساسیت تقریبی epsilon' نسبت به دما
a_tan = 1e-5         # حساسیت تقریبی loss tangent نسبت به دما

eps_real = eps0 + a_eps * (Tw - T_ref)
tan_delta = tan_delta0 + a_tan * (Tw - T_ref)
eps_imag = eps_real * tan_delta
eps_r = eps_real - 1j * eps_imag

# پارامترهای RF
c0 = 299_792_458.0   # سرعت نور [m/s]
f = 10e9             # فرکانس 10 GHz
k0 = 2.0 * np.pi * f / c0
d = 0.01             # ضخامت رادوم [m]

n1 = 1.0             # ضریب شکست هوا
n3 = 1.0             # هوا
n2 = np.sqrt(eps_r)  # ضریب شکست ماده رادوم

phi = k0 * n2 * d    # فاز داخل لایه

# ضرایب فرنل برای تابش عمود
r12 = (n1 - n2) / (n1 + n2)
r23 = (n2 - n3) / (n2 + n3)
t12 = 2.0 * n1 / (n1 + n2)
t23 = 2.0 * n2 / (n2 + n3)

T_amp = t12 * t23 * np.exp(1j * phi) / (1.0 + r12 * r23 * np.exp(2j * phi))
T_power = np.abs(T_amp) ** 2
loss_dB = -10.0 * np.log10(T_power)  # تلفات بر حسب dB

plt.figure()
plt.plot(M, loss_dB)
plt.xlabel("Mach number")
plt.ylabel("Transmission loss [dB]")
plt.title("Radome RF transmission loss vs Mach number")
plt.grid(True)
plt.tight_layout()
plt.savefig(OUT / "transmission_loss_vs_mach.pdf")
plt.close()
