"""Hareketin Hesabı: Mühendislik Dinamiği — lab ortak araçları.
Benzetim kaydı: veri/cay_servisi_kaydi.csv (Forenly AI kıraathane projesi, G1 insansı robot çay servisi, Isaac Lab, 50 örnek/saniye).
Kayıttan gelmeyen bütün sayılar derslerde ÖRNEK diye işaretlenir.

  oturum(ders, ad, kod)  : kodu Python etkileşimli oturumundaki gibi satır satır çalıştırır, çıktıyı ekran/<ders>/<ad>.txt'ye yazar
  sekil(ders, ad)        : açık şekli ekran/<ders>/<ad>.png olarak kaydeder (1920 × 1080)
  olc(anahtar=değer)     : ölçümü OLCUMLER.json'a yazar (derslerdeki bütün sayılar buradan gelir)
"""
import ast, contextlib, io, json, pathlib
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

LAB = pathlib.Path(__file__).resolve().parent
OLC = LAB / "OLCUMLER.json"
g = 9.81
np.set_printoptions(precision=4, suppress=True, linewidth=88, legacy="1.25")
plt.rcParams.update({"font.size": 22, "axes.titlesize": 26, "axes.labelsize": 24, "legend.fontsize": 20,
                     "figure.figsize": (19.2, 10.8), "axes.grid": True, "grid.alpha": 0.35, "lines.linewidth": 3,
                     "font.family": "DejaVu Sans"})


def kayit():
    """Benzetim kaydını sözlük olarak döndürür: zaman_s, dirsek_rad, dirsek_hiz_rad_s, bardak_x_m, bardak_y_m, bardak_z_m …"""
    d = np.genfromtxt(LAB / "veri/cay_servisi_kaydi.csv", delimiter=",", names=True)
    return {k: d[k] for k in d.dtype.names}


def yumusat(x, n=25):
    """Hareketli ortalama (n örnek; 25 örnek = yarım saniye). Kenarlarda yansıtarak doldurur."""
    x = np.asarray(x, float)
    k = np.ones(n) / n
    if x.ndim == 1:
        return np.convolve(np.pad(x, n, mode="reflect"), k, mode="same")[n:-n]
    return np.column_stack([yumusat(x[:, i], n) for i in range(x.shape[1])])


def _j(v):
    if isinstance(v, np.ndarray):
        return [_j(x) for x in v.tolist()]
    if isinstance(v, (list, tuple)):
        return [_j(x) for x in v]
    if isinstance(v, (float, np.floating)):
        return round(float(v), 4)
    if isinstance(v, (np.integer,)):
        return int(v)
    return v


def olc(**kw):
    d = json.loads(OLC.read_text()) if OLC.exists() else {}
    d.update({k: _j(v) for k, v in kw.items()})
    OLC.write_text(json.dumps(d, ensure_ascii=False, indent=1))


def oturum(ders, ad, kod, ns=None):
    """Kodu etkileşimli Python oturumu gibi çalıştırır: ifadenin değeri yazdırılır, atama sessizdir."""
    ns = {} if ns is None else ns
    ns.setdefault("__name__", "__oturum__")
    kod = kod.strip("\n")
    agac = ast.parse(kod)
    satirlar = kod.splitlines()
    out = []
    for st in agac.body:
        parca = satirlar[st.lineno - 1: st.end_lineno]
        out.append(">>> " + parca[0])
        out += ["... " + l for l in parca[1:]]
        if len(parca) > 1:
            out.append("...")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            if isinstance(st, ast.Expr):
                v = eval(compile(ast.Expression(st.value), "<oturum>", "eval"), ns)
                if v is not None:
                    print(repr(v))
            else:
                exec(compile(ast.Module([st], []), "<oturum>", "exec"), ns)
        out += buf.getvalue().rstrip("\n").splitlines() if buf.getvalue() else []
    yol = LAB / "ekran" / ders / f"{ad}.txt"
    yol.parent.mkdir(parents=True, exist_ok=True)
    yol.write_text("\n".join(out) + "\n", encoding="utf-8")
    return ns


def sekil(ders, ad, fig=None):
    fig = fig or plt.gcf()
    yol = LAB / "ekran" / ders / f"{ad}.png"
    yol.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(yol, dpi=100)
    plt.close(fig)
    return yol
