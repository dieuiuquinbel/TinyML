# Hướng dẫn dự án TinyML ECG

## Mục đích của file này

Đây là tài liệu định hướng cho dự án **Nghiên cứu mô hình TinyML cho phát hiện rối loạn nhịp tim theo thời gian thực trên thiết bị biên**. Con người và AI làm việc với dự án phải đọc file này trước khi thay đổi mã nguồn, dữ liệu, notebook hoặc báo cáo.

Đề cương chính thức được lưu ở thư mục gốc trong file `TinyML_De_cuong_NCKHSV_2026-2027_900_tu.docx`. File đề cương là tài liệu gốc về mục tiêu và phạm vi; không tự ý sửa hoặc di chuyển file này.

## Mục tiêu cuối cùng

Xây dựng và đánh giá hệ thống TinyML phân loại năm nhóm nhịp ECG theo chuẩn AAMI trên ESP32-S3. Chuỗi xử lý đích gồm tín hiệu ECG một kênh, phát hiện đỉnh R, cắt nhịp 180 mẫu, phân loại N/S/V/F/Q, lượng tử hóa INT8 và đo tài nguyên trên phần cứng.

Đây là đề tài nghiên cứu 9 tháng. Không được suy diễn rằng việc hoàn thành Dataset v1 đồng nghĩa với đã hoàn thành CNN, INT8 hoặc ESP32-S3.

## Cấu trúc thư mục

```text
Nghiên Cứu Khoa Học/
├─ mitdb/                         # Dữ liệu MIT-BIH thô, không sửa trực tiếp
├─ Tuần 1-2/                      # Khảo sát dữ liệu, lọc thử nghiệm, báo cáo tuần 1-2
├─ Tuần 3-4/                      # Pipeline 48 record, cắt nhịp, split Train/Test ban đầu
├─ Tuần 5-6-7/                    # Kiểm định detector, Train/Val/Test, Dataset v1
├─ TinyML_De_cuong_NCKHSV_2026-2027_900_tu.docx
└─ HUONG_DAN_DU_AN.md             # File này
```

Mỗi giai đoạn mới phải có thư mục riêng. Không đưa notebook, ảnh kết quả hoặc dữ liệu sinh ra trở lại thư mục gốc.

## Những gì đã hoàn thành

### Tuần 1-2

Nhóm đã tải và khảo sát MIT-BIH Arrhythmia Database, lựa chọn đạo trình MLII, tìm hiểu ánh xạ nhãn AAMI và thử nghiệm bộ lọc Butterworth 0,5–45 Hz. Các script khảo sát nằm trong `Tuần 1-2`.

### Tuần 3-4

Nhóm đã tạo pipeline xử lý 48 record: lọc Butterworth 0,5–45 Hz, detector theo hướng Pan-Tompkins, cắt nhịp 180 mẫu quanh R-peak và tạo split Train/Test theo bệnh nhân. Kết quả gốc nằm trong `Tuần 3-4/ket_qua_ecg`.

Các số liệu quan trọng:

- 48 record đã xử lý.
- 105.948 nhịp detector-aligned có đủ cửa sổ 180 mẫu.
- Bốn record paced `102`, `104`, `107`, `217` không dùng cho cohort phân loại.
- Record `201` và `202` phải luôn ở cùng một split vì thuộc cùng một bệnh nhân.

### Tuần 5-7

Nhóm đã hoàn thiện phần dữ liệu của Giai đoạn 1 trong `Tuần 5-6-7`.

- `01_kiem_dinh_detector_R_peak.ipynb`: kiểm định R-peak bằng ghép một-một với annotation MIT-BIH ở dung sai ±50 ms. Kết quả toàn bộ 48 record: PPV 97,32%, Recall 94,16%, F1 95,71%.
- `02_chot_train_val_test_theo_benh_nhan.ipynb`: tách Train/Validation/Test theo bệnh nhân, tạo dữ liệu căn theo annotation chuẩn và căn theo detector.
- `03_dong_goi_dataset_v1.ipynb`: chuẩn hóa dữ liệu chỉ bằng thống kê Train, kiểm tra chất lượng và đóng gói Dataset v1.

## Dataset v1: nguồn dữ liệu chuẩn cho mô hình phân loại

Đường dẫn: `Tuần 5-6-7/dataset_v1/`.

Dataset v1 sử dụng **reference-aligned beats**, tức nhịp được căn theo annotation chuẩn của MIT-BIH. Đây là bộ bắt buộc dùng để huấn luyện, chọn mô hình và đánh giá chất lượng phân loại riêng.

| Tập | Số nhịp | Số record | Số nhóm bệnh nhân |
|---|---:|---:|---:|
| Train | 43.744 | 19 | 18 |
| Validation | 9.402 | 4 | 4 |
| Test | 47.562 | 21 | 21 |
| Tổng | 100.708 | 44 | 43 |

Mỗi mẫu có 180 giá trị, với R-peak tại chỉ số 90. Nhãn hợp lệ là `N`, `S`, `V`, `F`, `Q`.

Các file cần giữ nguyên:

- `train.npz`, `val.npz`, `test.npz`: dữ liệu đã chuẩn hóa.
- `manifest.json`: cấu hình nguồn, lọc, split và kích thước dữ liệu.
- `normalization.json`: mean/std được fit trên Train.
- `class_distribution.csv`: thống kê lớp.

## Quy tắc dữ liệu bắt buộc

1. Không dùng Test để fit chuẩn hóa, cân bằng lớp, chọn kiến trúc, chọn hyperparameter hoặc early stopping.
2. Chỉ dùng Train để fit scaler, class weight, augmentation, oversampling hoặc bất kỳ bước học dữ liệu nào.
3. Chỉ dùng Validation để lựa chọn cấu hình; Test chỉ dùng một lần cho đánh giá cuối cùng của mô hình đã chốt.
4. Không chia ngẫu nhiên theo từng nhịp. Split phải theo bệnh nhân/record đã cố định.
5. Không di chuyển record `201` và `202` sang hai tập khác nhau.
6. Không thêm nhãn `?` vào lớp Q. Nhãn `?` và ký hiệu ngoài ánh xạ AAMI bị loại khỏi supervised dataset.
7. Không ghi đè `Tuần 3-4/ket_qua_ecg` hoặc Dataset v1. Nếu cần thử nghiệm dữ liệu mới, tạo thư mục/phiên bản mới.
8. Dữ liệu detector-aligned chỉ dùng để đánh giá end-to-end ở giai đoạn sau; không thay thế Dataset v1 khi đánh giá riêng CNN.

## Giới hạn đã biết

- Bộ lọc hiện tại là zero-phase `sosfiltfilt`, phù hợp tiền xử lý offline nhưng chưa thể sử dụng nguyên trạng cho xử lý thời gian thực trên ESP32-S3.
- Detector Pan-Tompkins hiện là bản triển khai theo hướng thực nghiệm, chưa có đầy đủ search-back, loại sóng T và mọi quy tắc của thuật toán gốc.
- Các lớp S, F và đặc biệt Q mất cân bằng mạnh so với N. Mọi biện pháp xử lý mất cân bằng chỉ được thực hiện trên Train.
- Record 228 có Recall R-peak thấp; giữ record này trong Test để phản ánh tình huống khó khi đánh giá end-to-end.

## Hướng đi tiếp theo

### Giai đoạn 2: mô hình học máy và lượng tử hóa

1. Xây baseline đơn giản trên Dataset v1 để có mốc so sánh.
2. Thiết kế CNN 1D gốc và CNN 1D tinh gọn cho nhịp 180 mẫu.
3. Huấn luyện lặp lại với ba seed; sử dụng class weight hoặc kỹ thuật cân bằng chỉ trên Train.
4. Chọn cấu hình dựa trên Validation.
5. Báo cáo trên Test: Macro-F1, Precision, Recall, F1 từng lớp, confusion matrix, số mẫu mỗi lớp và trung bình/độ lệch chuẩn qua các seed.
6. Sau khi chốt mô hình FP32, thực hiện Post-Training INT8 Quantization và so sánh suy giảm hiệu năng.

### Giai đoạn 3: triển khai ESP32-S3

1. Chuyển mô hình INT8 sang TensorFlow Lite for Microcontrollers.
2. Triển khai bộ lọc nhân quả và detector phù hợp thời gian thực, không dùng trực tiếp `sosfiltfilt`.
3. Đo kích thước `.tflite`, firmware, tensor arena, RAM ngoài arena và độ trễ suy luận.
4. Đánh giá phát lại ECG theo thời gian thực: số mẫu mất, nhịp bỏ sót, độ trễ từ R-peak đến kết quả và kết quả end-to-end.

## Quy tắc làm việc cho AI

- Đọc file này trước khi đề xuất hoặc thực hiện thay đổi.
- Kiểm tra notebook và tệp đầu ra trước khi tuyên bố một kết quả đã hoàn thành.
- Không tạo số liệu, chỉ số hoặc kết luận không có tệp kết quả hỗ trợ.
- Khi tạo notebook, cell đầu phải import đủ thư viện cần thiết và notebook phải vẽ bảng/biểu đồ trực quan trong lúc chạy.
- Ưu tiên đường dẫn tương đối dựa trên thư mục dự án; không hard-code đường dẫn máy cá nhân.
- Giữ notebook, file đầu ra và hình minh họa trong thư mục của giai đoạn tương ứng.
- Khi viết báo cáo, phân biệt rõ việc đã hoàn thành, giới hạn hiện tại và kế hoạch; không tuyên bố đã triển khai ESP32, INT8 hoặc CNN khi chưa có hiện vật xác minh.
