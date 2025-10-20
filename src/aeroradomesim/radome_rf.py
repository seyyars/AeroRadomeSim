import numpy as np

def layer(thickness, eps_r, tan_delta=0.0):
    """یک لایهٔ دی‌الکتریک ایزوتروپ؛ eps = eps_r*(1 - i tanδ)"""
    eps_c = eps_r * (1.0 - 1j * tan_delta)
    return {"d": float(thickness), "eps": complex(eps_c)}

def _snell(theta0, n0, n1):
    # شکست اسنل با n های ممکن‌اً مختلط (برای tanδ>0 زاویه را از نسبت استفاده می‌کنیم)
    s = np.sin(theta0) * (n0 / n1)
    # برای مقادیر مختلط، clip بی‌معناست؛ در حالت نرمال‌اینسی‌دنس مشکلی نیست.
    return np.arcsin(s)

def _q(pol, n, theta):
    # ادمیتانس اپتیکی لایه (بدون μ≠1):  q_s (TE) = n cosθ ،  q_p (TM) = n / cosθ
    pol = pol.upper()
    c = np.cos(theta)
    return n * c if pol == "TE" else n / c

def tmm_s21(f, stack, theta=0.0, pol="TE", n0=1.0, nL=1.0):
    """
    انتقال میدان (Complex) از چندلایه به روش ماتریس مشخصه.
    بازگشت: t = S21 (آمپلی‌تود میدان). برای توان: T = (Re(qL)/Re(q0)) * |t|^2
    """
    f = np.atleast_1d(f)
    c0 = 299_792_458.0
    k0 = 2.0 * np.pi * f / c0
    pol = pol.upper()

    # اندیس‌ها و زوایا در کل پشته
    ns = [complex(n0)]
    thetas = [complex(theta)]
    for L in stack:
        ns.append(np.sqrt(L["eps"]))
        thetas.append(_snell(thetas[-1], ns[-2], ns[-1]))
    ns.append(complex(nL))
    thetas.append(_snell(thetas[-1], ns[-2], ns[-1]))

    q0 = _q(pol, ns[0], thetas[0])
    qL = _q(pol, ns[-1], thetas[-1])

    out = np.zeros_like(f, dtype=complex)

    for i, k in enumerate(k0):
        # ماتریس کلی
        M11 = 1.0 + 0.0j
        M12 = 0.0 + 0.0j
        M21 = 0.0 + 0.0j
        M22 = 1.0 + 0.0j

        # هر لایه: M_j = [[cosδ, (i/q_j) sinδ], [i q_j sinδ, cosδ]]
        for j, L in enumerate(stack, start=1):
            n = ns[j]
            th = thetas[j]
            qj = _q(pol, n, th)
            delta = k * n * L["d"] * np.cos(th)
            c = np.cos(delta)
            s = 1j * np.sin(delta)

            A = c
            B = s / qj
            C = s * qj
            D = c

            # ضرب ماتریس‌ها: M = M @ M_j
            M11, M12, M21, M22 = (
                M11*A + M12*C,
                M11*B + M12*D,
                M21*A + M22*C,
                M21*B + M22*D,
            )

        denom = (q0 * M11 + q0 * qL * M12 + M21 + qL * M22)
        t = 2.0 * q0 / denom
        out[i] = t

    return out
