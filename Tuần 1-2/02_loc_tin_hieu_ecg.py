import os
import sys
import wfdb
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# 1. Đường dẫn dữ liệu
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)
DATA_DIR = os.path.join(PROJECT_DIR, 'mitdb', 'mit-bih-arrhythmia-database-1.0.0', 'mit-bih-arrhythmia-database-1.0.0')
RECORD_NAME = '100'
record_path = os.path.join(DATA_DIR, RECORD_NAME)

print(f"[*] Đang đọc dữ liệu bản ghi {RECORD_NAME}...")
# Đọc 10 giây đầu tiên (Fs = 360 Hz -> 3600 mẫu)
fs = 360
num_samples = 3600
record = wfdb.rdrecord(record_path, sampto=num_samples)
ecg_raw = record.p_signal[:, 0]  # Kênh MLII
time_axis = np.arange(num_samples) / fs

# 2. Thiết kế bộ lọc thông dải Bandpass (0.5 Hz - 45 Hz)
def butter_bandpass_filter(data, lowcut, highcut, fs, order=4):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    y = filtfilt(b, a, data)
    return y

print("[*] Đang áp dụng bộ lọc Bandpass Butterworth (0.5 - 45 Hz)...")
ecg_filtered = butter_bandpass_filter(ecg_raw, lowcut=0.5, highcut=45.0, fs=fs, order=2)

# 3. Vẽ biểu đồ so sánh chi tiết trước và sau lọc
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 8), sharex=True)

# Đồ thị 1: Tín hiệu thô
ax1.plot(time_axis, ecg_raw, color='#d9534f', linewidth=1.2, label='ECG Thô (Chưa lọc)')
ax1.set_title(f'Tín hiệu ECG gốc (Raw) - Bản ghi MIT-BIH {RECORD_NAME} (Chứa nhiễu trôi đường nền và cơ)', fontsize=12, fontweight='bold')
ax1.set_ylabel('Biên độ (mV)', fontsize=10)
ax1.legend(loc='upper right')
ax1.grid(True, linestyle='--', alpha=0.6)

# Đồ thị 2: Tín hiệu đã lọc
ax2.plot(time_axis, ecg_filtered, color='#0275d8', linewidth=1.2, label='ECG sau lọc Bandpass (0.5 - 45 Hz)')
ax2.axhline(0, color='gray', linestyle=':', alpha=0.7)
ax2.set_title('Tín hiệu ECG sau khi lọc thông dải (Đường nền phẳng, rõ phức bộ QRS)', fontsize=12, fontweight='bold')
ax2.set_ylabel('Biên độ (mV)', fontsize=10)
ax2.legend(loc='upper right')
ax2.grid(True, linestyle='--', alpha=0.6)

# Đồ thị 3: So sánh chồng lớp
ax3.plot(time_axis, ecg_raw, color='#d9534f', alpha=0.4, linewidth=1, label='Tín hiệu thô')
ax3.plot(time_axis, ecg_filtered, color='#0275d8', linewidth=1.2, label='Tín hiệu sau lọc')
ax3.set_title('So sánh đối chiếu trực tiếp giữa tín hiệu thô và tín hiệu sau lọc', fontsize=12, fontweight='bold')
ax3.set_xlabel('Thời gian (giây)', fontsize=10)
ax3.set_ylabel('Biên độ (mV)', fontsize=10)
ax3.legend(loc='upper right')
ax3.grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()
output_img = os.path.join(BASE_DIR, 'hinh2_loc_tin_hieu_bandpass.png')
plt.savefig(output_img, dpi=300)
print(f"[+] Đã lưu biểu đồ kết quả lọc thành công vào: {output_img}")
