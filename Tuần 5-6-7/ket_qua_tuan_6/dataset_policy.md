# Chính sách Dataset v1 (tiền chuẩn hóa)

- Chỉ dùng 44 record không paced; loại 102, 104, 107, 217.
- Train/validation/test tách theo nhóm bệnh nhân; 201 và 202 luôn cùng split.
- Nhãn supervised gồm N, S, V, F, Q; `?` và ký hiệu ngoài ánh xạ bị loại.
- `reference_aligned` dùng annotation chuyên gia để đánh giá riêng mô hình phân loại.
- `detector_aligned` dùng R-peak detector để đánh giá pipeline end-to-end sau này.
