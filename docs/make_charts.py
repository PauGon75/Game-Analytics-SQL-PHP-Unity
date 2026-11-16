import glob, os, sys, openpyxl, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
src = sys.argv[1]; out = sys.argv[2]; os.makedirs(out, exist_ok=True)
wb = openpyxl.load_workbook(src, data_only=True)
S, M = wb["Summary"], wb["Monthly"]
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 13, "axes.spines.top": False,
                     "axes.spines.right": False, "axes.edgecolor": "#888", "axes.titleweight": "bold"})
A, B, C, G = "#2a78d6", "#f08a24", "#1baa7a", "#9aa3ad"
def save(f, n):
    f.tight_layout(); f.savefig(f"{out}/{n}.jpg", dpi=100, pil_kwargs={"quality": 85}); plt.close(f)
mon = [M.cell(r, 1).value for r in range(4, 16)]
dau = [M.cell(r, 2).value for r in range(4, 16)]
d1 = [M.cell(r, 5).value * 100 for r in range(4, 16)]
f, ax = plt.subplots(figsize=(12.8, 7.2))
ax.bar(mon, dau, color=[G] * 5 + [A] * 7)
ax.set_ylabel("Average DAU"); ax.set_title("Daily active users and D1 retention per month (2022)", loc="left")
ax2 = ax.twinx(); ax2.plot(mon, d1, color=B, lw=3, marker="o"); ax2.set_ylabel("D1 retention (%)", color=B)
ax2.set_ylim(0, 100); ax2.spines["top"].set_visible(False)
ax.annotate("Change in June:\nDAU x3, D1 31% → 79%", xy=(5, dau[5]), xytext=(1.2, max(dau) * 0.85),
            arrowprops=dict(arrowstyle="->", color="#555"), fontsize=13)
save(f, "analytics-1")
lab = ["D1", "D3", "D7"]
pre = [S.cell(31, c).value * 100 for c in (2, 3, 4)]; post = [S.cell(32, c).value * 100 for c in (2, 3, 4)]
f, ax = plt.subplots(figsize=(12.8, 7.2)); x = range(3)
b1 = ax.bar([i - .2 for i in x], pre, .4, color=G, label="Jan – May")
b2 = ax.bar([i + .2 for i in x], post, .4, color=A, label="Jun – Dec")
ax.bar_label(b1, fmt="%.0f%%"); ax.bar_label(b2, fmt="%.0f%%")
ax.set_xticks(list(x), lab); ax.set_ylabel("Players who come back (%)"); ax.legend(frameon=False)
ax.set_title("Retention before and after June", loc="left"); save(f, "analytics-2")
items = [f"{S.cell(r, 2).value:.2f} €" for r in range(37, 42)]
rev = [S.cell(r, 4).value for r in range(37, 42)]; tot = sum(rev)
f, ax = plt.subplots(figsize=(12.8, 7.2))
bars = ax.barh(items, rev, color=[G] * 4 + [C]); ax.invert_yaxis()
ax.bar_label(bars, labels=[f"{v:,.0f} €  ({v / tot:.0%})" for v in rev], padding=6)
ax.set_xlabel("Revenue (€)"); ax.set_xlim(0, max(rev) * 1.25)
ax.set_title(f"Revenue by item: the 99.99 € pack makes {rev[4] / tot:.0%} of {tot:,.0f} €", loc="left")
save(f, "analytics-3")
print("ok", os.listdir(out))
