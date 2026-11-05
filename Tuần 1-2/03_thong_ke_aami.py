import os
import sys
import wfdb
import matplotlib.pyplot as plt

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)
DATA_DIR = os.path.join(PROJECT_DIR, 'mitdb', 'mit-bih-arrhythmia-database-1.0.0', 'mit-bih-arrhythmia-database-1.0.0')

RECORDS = [
    '100', '101', '102', '103', '104', '105', '106', '107', '108', '109',
    '111', '112', '113', '114', '115', '116', '117', '118', '119', '121'
]

AAMI_CLASSES = {
    'N': ['N', 'L', 'R', 'e', 'j'],              # Nhịp bình thường / Blốc nhánh
    'S': ['A', 'a', 'J', 'S'],                   # Ngoại tâm thu trên thất
    'V': ['V', 'E'],                             # Ngoại tâm thu thất
    'F': ['F'],                                  # Nhịp dung hợp
    'Q': ['/', 'f', 'Q', '?']                     # Nhịp tạo nhịp / không xác định
}

def map_to_aami(symbol):
    for aami_class, symbols in AAMI_CLASSES.items():
        if symbol in symbols:
            return aami_class
    return None

total_counts = {'N': 0, 'S': 0, 'V': 0, 'F': 0, 'Q': 0}

for rec in RECORDS:
    rec_path = os.path.join(DATA_DIR, rec)
    ann = wfdb.rdann(rec_path, 'atr')
    for sym in ann.symbol:
        c = map_to_aami(sym)
        if c:
            total_counts[c] += 1

# Vẽ biểu đồ trực quan phân bố 5 nhóm nhịp AAMI
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

classes = list(total_counts.keys())
counts = list(total_counts.values())
colors = ['#2ca02c', '#1f77b4', '#d62728', '#ff7f0e', '#9467bd']
class_labels = [
    'N: Bình thường',
    'S: Trên thất',
    'V: Ngoại tâm thu thất',
    'F: Dung hợp',
    'Q: Khác'
]

# Biểu đồ cột thể hiện số lượng mẫu
bars = ax1.bar(classes, counts, color=colors, edgecolor='black', alpha=0.85)
ax1.set_title('Số lượng nhịp theo 5 nhóm chuẩn AAMI', fontsize=12, fontweight='bold')
ax1.set_xlabel('Nhóm nhịp AAMI', fontsize=11)
ax1.set_ylabel('Số lượng mẫu (nhịp)', fontsize=11)
for bar in bars:
    yval = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2, yval + 500, f'{yval:,}', ha='center', va='bottom', fontsize=9, fontweight='bold')
ax1.grid(True, linestyle='--', alpha=0.5)

# Biểu đồ tròn thể hiện tỷ lệ % mất cân bằng dữ liệu
explode = (0.05, 0.1, 0.1, 0.15, 0.1)
ax2.pie(counts, labels=class_labels, autopct='%1.1f%%', startangle=140, colors=colors, explode=explode, shadow=True)
ax2.set_title('Tỷ lệ % phân bố các nhóm nhịp (Mất cân bằng dữ liệu)', fontsize=12, fontweight='bold')

plt.tight_layout()
output_file = os.path.join(BASE_DIR, 'hinh3_phan_bo_aami.png')
plt.savefig(output_file, dpi=300)
print(f"[+] Đã tạo biểu đồ phân bố nhịp trực quan: {output_file}")
