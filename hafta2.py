"""Hafta 2 · Parçacığın Kinetiği — Ders 2.1–2.4.
  python hafta2.py   → ekran/2.x/*.txt + *.png, OLCUMLER.json (d2_*)"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from ortak import kayit, yumusat, olc, oturum, sekil, g


def ders_2_1():
    """Newton'un ikinci yasası: bardak tepside taşınsaydı kaymaması için gereken sürtünme katsayısı."""
    ns = oturum("2.1", "gereken-surtunme", """
import numpy as np
from ortak import kayit, yumusat
g = 9.81
m = 0.2
k = kayit()
t = k["zaman_s"]
p = yumusat(np.column_stack([k["bardak_x_m"], k["bardak_y_m"], k["bardak_z_m"]]))
a = np.gradient(np.gradient(p, t, axis=0), t, axis=0)
a_yatay = np.hypot(a[:, 0], a[:, 1])
N = m * (g + a[:, 2])
f = m * a_yatay
mu_gerekli = f / N
i = mu_gerekli.argmax()
round(t[i], 2), round(a_yatay[i], 3)
round(f[i], 3), round(N[i], 3)
round(mu_gerekli[i], 3)
""")
    t, mu, i = ns["t"], ns["mu_gerekli"], ns["i"]
    ns = oturum("2.1", "surtunme-karsilastir", """
for mu_s in (0.05, 0.1, 0.2, 0.4):
    asim = (mu_gerekli > mu_s).sum() / 50
    print(f"mu = {mu_s:4.2f}   kayma riski süresi {asim:5.2f} s")
""", ns)
    fig, ax = plt.subplots()
    ax.plot(t, mu, color="#7E22CE", label="gereken sürtünme katsayısı  f / N")
    for mu_s, r in [(0.1, "#C2410C"), (0.4, "#0F766E")]:
        ax.axhline(mu_s, ls="--", color=r, label=f"tepsi–bardak sürtünmesi {mu_s} (ÖRNEK)")
    ax.annotate(f"en büyük {mu[i]:.3f}", (t[i], mu[i]), xytext=(t[i] + 8, mu[i] + 0.03), arrowprops=dict(arrowstyle="->"))
    ax.set_xlabel("zaman (s)"); ax.set_ylabel("katsayı"); ax.legend(loc="upper left")
    ax.set_title("Bardak tepsideyse kayar mı? · ivme benzetim kaydından, kütle 0,2 kg (ÖRNEK)")
    sekil("2.1", "surtunme-grafik")
    risk = {str(m_): float((mu > m_).sum() / 50) for m_ in (0.05, 0.1, 0.2, 0.4)}
    olc(d2_1_t=t[i], d2_1_a=ns["a_yatay"][i], d2_1_f=ns["f"][i], d2_1_N=ns["N"][i], d2_1_mu=mu[i], d2_1_risk_s=risk)


def ders_2_2():
    """Hareket denklemini sayısal çözmek: hava dirençli düşüş, limit hız (ÖRNEK top)."""
    ns = oturum("2.2", "hareket-denklemi", """
import numpy as np
from scipy.integrate import solve_ivp
g = 9.81
m, c = 0.45, 0.0071
def denklem(t, s):
    y, v = s
    return [v, -g + c / m * v**2]
yere = lambda t, s: s[0]
yere.terminal = True
cozum = solve_ivp(denklem, [0, 10], [40, 0], events=yere, max_step=0.01)
t_yer = cozum.t_events[0][0]
v_yer = cozum.y_events[0][0][1]
round(t_yer, 3), round(v_yer, 2)
v_limit = np.sqrt(m * g / c)
round(v_limit, 2)
""")
    ns = oturum("2.2", "kapali-ile-sinama", """
v_kapali = -v_limit * np.tanh(g * cozum.t / v_limit)
hata = np.abs(cozum.y[1] - v_kapali).max()
f"{hata:.1e}"
t_direncsiz = np.sqrt(2 * 40 / g)
round(t_direncsiz, 3), round(-g * t_direncsiz, 2)
""", ns)
    c = ns["cozum"]; vl = ns["v_limit"]
    fig, ax = plt.subplots()
    ax.plot(c.t, -c.y[1], color="#7E22CE", lw=5, label="sayısal çözüm (solve_ivp)")
    ax.plot(c.t, vl * np.tanh(g * c.t / vl), "--", color="#C2410C", label="kapalı çözüm  v_L · tanh(g t / v_L)")
    tt = np.linspace(0, ns["t_direncsiz"], 50); ax.plot(tt, g * tt, ":", color="#555555", label="hava direnci olmasaydı")
    ax.axhline(vl, color="#0F766E", ls="-.", lw=2, label=f"limit hız {vl:.1f} m/s")
    ax.set_xlabel("zaman (s)"); ax.set_ylabel("düşme hızı (m/s)"); ax.legend(loc="lower right")
    ax.set_title("40 metreden düşen top · kütle 0,45 kg, direnç katsayısı 0,0071 kg/m (ÖRNEK)")
    sekil("2.2", "dusme-hizi")
    olc(d2_2_t_yer=ns["t_yer"], d2_2_v_yer=ns["v_yer"], d2_2_v_limit=vl, d2_2_hata=float(ns["hata"]),
        d2_2_t_direncsiz=ns["t_direncsiz"], d2_2_v_direncsiz=g * ns["t_direncsiz"])


def ders_2_3():
    """Yay, kütle ve sönüm: serbest titreşim (ÖRNEK)."""
    ns = oturum("2.3", "titresim", """
import numpy as np
from scipy.integrate import solve_ivp
m, k, c = 2.0, 200.0, 4.0
w_n = np.sqrt(k / m)
zeta = c / (2 * np.sqrt(k * m))
w_d = w_n * np.sqrt(1 - zeta**2)
round(w_n, 3), round(zeta, 3), round(w_d, 3)
T_d = 2 * np.pi / w_d
round(T_d, 4)
""")
    ns = oturum("2.3", "periyot-olcmek", """
cozum = solve_ivp(lambda t, s: [s[1], -(c * s[1] + k * s[0]) / m], [0, 3], [0.05, 0],
                  max_step=0.001)
x = cozum.y[0]
tepe = np.flatnonzero((x[1:-1] > x[:-2]) & (x[1:-1] > x[2:])) + 1
T_olcum = np.diff(cozum.t[tepe]).mean()
round(T_olcum, 4)
azalma = np.log(x[tepe[0]] / x[tepe[1]])
round(azalma, 4), round(2 * np.pi * zeta / np.sqrt(1 - zeta**2), 4)
""", ns)
    fig, ax = plt.subplots()
    m, k = 2.0, 200.0
    for c, r in [(4.0, "#7E22CE"), (20.0, "#1D4ED8"), (40.0, "#0F766E")]:
        s = solve_ivp(lambda t, s: [s[1], -(c * s[1] + k * s[0]) / m], [0, 3], [0.05, 0], max_step=0.001)
        z = c / (2 * np.sqrt(k * m))
        ax.plot(s.t, 1000 * s.y[0], color=r, label=f"sönüm {c:g} N·s/m  →  ζ = {z:.1f}")
    ax.set_xlabel("zaman (s)"); ax.set_ylabel("konum (mm)"); ax.legend(loc="upper right")
    ax.set_title("Yay–kütle–sönüm · 2 kg, 200 N/m, başlangıç 50 mm (ÖRNEK)")
    sekil("2.3", "sonum-karsilastir")
    olc(d2_3_wn=ns["w_n"], d2_3_zeta=ns["zeta"], d2_3_wd=ns["w_d"], d2_3_Td=ns["T_d"], d2_3_T_olcum=ns["T_olcum"],
        d2_3_azalma=ns["azalma"])


def ders_2_4():
    """Sarkaç: normal ve teğetsel bileşenlerle ip gerilmesi (ÖRNEK)."""
    ns = oturum("2.4", "ip-gerilmesi", """
import numpy as np
from scipy.integrate import solve_ivp
g, m, L = 9.81, 0.5, 1.0
th0 = np.radians(60)
cozum = solve_ivp(lambda t, s: [s[1], -g / L * np.sin(s[0])], [0, 4], [th0, 0],
                  max_step=0.001, rtol=1e-9, atol=1e-9)
th, th_n = cozum.y
T = m * g * np.cos(th) + m * L * th_n**2
round(T.max(), 3), round(T.min(), 3)
T_alt = m * g * (3 - 2 * np.cos(th0))
round(T_alt, 3), round(m * g * np.cos(th0), 3)
""")
    c = ns["cozum"]; T = ns["T"]
    fig, ax = plt.subplots(2, 1, sharex=True)
    ax[0].plot(c.t, np.degrees(ns["th"]), color="#7E22CE"); ax[0].set_ylabel("açı (°)")
    ax[0].set_title("Sarkaç · 0,5 kg, ip 1 m, 60°'den bırakılıyor (ÖRNEK)")
    ax[1].plot(c.t, T, color="#C2410C", label="ip gerilmesi  m g cos θ + m L θ̇²")
    ax[1].axhline(0.5 * 9.81, ls="--", color="#555555", label="ağırlık  m g")
    ax[1].set_ylabel("kuvvet (N)"); ax[1].set_xlabel("zaman (s)"); ax[1].set_ylim(0, 14); ax[1].legend(loc="upper center", ncol=2)
    sekil("2.4", "sarkac-grafik")
    olc(d2_4_T_max=T.max(), d2_4_T_min=T.min(), d2_4_T_alt=ns["T_alt"], d2_4_T_uc=ns["m"] * 9.81 * np.cos(ns["th0"]))


if __name__ == "__main__":
    for f in (ders_2_1, ders_2_2, ders_2_3, ders_2_4):
        f(); print(f.__name__, "tamam")
