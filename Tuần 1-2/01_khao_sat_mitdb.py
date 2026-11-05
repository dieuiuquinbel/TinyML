import os
import sys
import wfdb
import numpy as np
import matplotlib.pyplot as plt

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)
DATA_DIR = os.path.join(PROJECT_DIR, 'mitdb', 'mit-bih-arrhythmia-database-1.0.0', 'mit-bih-arrhythmia-database-1.0.0')
RECORD_NAME = '100'
record_path = os.path.join(DATA_DIR, RECORD_NAME)

# Đọc 5 giây đầu (1800 mẫu) của 2 kênh MLII và V5
fs = 360
num_samples = 1800
record = wfdb.rdrecord(record_path, sampto=num_samples)
annotation = wfdb.rdann(record_path, 'atr', sampto=num_samples)

time_axis = np.arange(num_samples) / fs

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6), sharex=True)

# Kênh 1: MLII
ax1.plot(time_axis, record.p_signal[:, 0], color='#1f77b4', linewidth=1.2, label='Đạo trình chính (MLII)')
# Đánh dấu các nhịp tim do bác sĩ gán nhãn
for s, sym in zip(annotation.sample, annotation.symbol):
    ax1.axvline(x=s/fs, color='red', linestyle='--', alpha=0.5)
    ax1.text(s/fs, np.max(record.p_signal[:, 0]) * 0.9, f"[{sym}]", color='red', fontsize=10, ha='center', fontweight='bold')
ax1.set_title(f'Tín hiệu ECG Bản ghi MIT-BIH {RECORD_NAME} - Kênh MLII (Có đánh dấu vị trí nhịp)', fontsize=12, fontweight='bold')
ax1.set_ylabel('Biên độ (mV)', fontsize=10)
ax1.legend(loc='upper right')
ax1.grid(True, linestyle='--', alpha=0.6)

# Kênh 2: V5
ax2.plot(time_axis, record.p_signal[:, 1], color='#2ca02c', linewidth=1.2, label='Đạo trình phụ (V5)')
ax2.set_title(f'Tín hiệu ECG Bản ghi MIT-BIH {RECORD_NAME} - Kênh V5', fontsize=12, fontweight='bold')
ax2.set_xlabel('Thời gian (giây)', fontsize=10)
ax2.set_ylabel('Biên độ (mV)', fontsize=10)
ax2.legend(loc='upper right')
ax2.grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()
output_file = os.path.join(BASE_DIR, 'hinh1_khao_sat_tin_hieu_mitdb.png')
plt.savefig(output_file, dpi=300)
print(f"[+] Đã tạo biểu đồ khảo sát tín hiệu trực quan: {output_file}")
