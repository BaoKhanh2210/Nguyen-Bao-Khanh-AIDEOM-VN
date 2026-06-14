# AIDEOM-VN Showcase

Trang web trình bày kết quả 12 bài tập thực hành về **các mô hình ra quyết định phát triển kinh tế Việt Nam trong kỉ nguyên AI**.

Dữ liệu được tính toán trước từ Python (Google Colab) và hiển thị dưới dạng bảng, biểu đồ tương tác và hình ảnh kết quả.

## 12 bài tập

| # | Bài | Phương pháp chính |
|---|-----|-------------------|
| 1 | Cobb-Douglas mở rộng | TFP, tăng trưởng, dự báo 2030 |
| 2 | Phân bổ ngân sách | Linear Programming, shadow price |
| 3 | Chỉ số ưu tiên ngành | Min-max, MCDM, sensitivity |
| 4 | LP phân bổ vùng miền | 24 biến, 25 ràng buộc, equity |
| 5 | MIP chọn dự án | Mixed Integer Programming, binary |
| 6 | TOPSIS xếp hạng vùng | TOPSIS, Entropy, AHP |
| 7 | NSGA-II đa mục tiêu | Pareto 4 mục tiêu |
| 8 | Tối ưu động | SLSQP, welfare 2026–2035 |
| 9 | Tác động AI tới lao động | Net job, retraining threshold |
| 10 | Quy hoạch ngẫu nhiên | Stochastic LP, VSS, EVPI |
| 11 | Q-learning chính sách | Reinforcement learning, MDP |
| 12 | AIDEOM-VN tích hợp | Pipeline 6 module |

## Cách chạy trên máy tính

### Bước 1 — Cài Node.js

Tải Node.js tại https://nodejs.org/ (chọn bản LTS). Sau khi cài xong, mở Terminal (hoặc PowerShell) và kiểm tra:

```bash
node --version
```

Nếu thấy số phiên bản (ví dụ `v20.x.x`) là đã cài thành công.

### Bước 2 — Tải mã nguồn

Nếu dùng Git:

```bash
git clone <repository-url>
cd aideom-mamz
```

Hoặc tải file ZIP từ GitHub rồi giải nén.

### Bước 3 — Cài thư viện

```bash
npm install
```

Lệnh này sẽ tải các thư viện cần thiết. Chờ khoảng 1–2 phút.

### Bước 4 — Chạy thử

```bash
npm run dev
```

Mở trình duyệt vào địa chỉ `http://localhost:5173` (hoặc địa chỉ hiển trong terminal).

### Bước 5 — Build trang web hoàn chỉnh

```bash
npm run build
```

Kết quả sẽ nằm trong thư mục `dist/`. Có thể dùng `npm run preview` để xem trước bản build.

## Cấu trúc thư mục

```
src/
  components/
    results/        ← 12 component kết quả (mỗi bài 1 file)
    Accordion.tsx
    ResultImage.tsx
    RichResultText.tsx
  data/
    exercises.ts    ← Danh sách 12 bài tập
    results.ts      ← Dữ liệu kết quả từ Python
  pages/
    Home.tsx        ← Trang chủ
    ExercisePage.tsx ← Trang chi tiết bài tập
public/
  results/          ← Ảnh kết quả tĩnh (.png)
```

## Triển khai lên Vercel

1. Tạo tài khoản tại https://vercel.com
2. Kết nối với repository GitHub
3. Vercel sẽ tự động detect dự án Vite và deploy
4. Không cần cấu hình thêm — trang web là tĩnh (static site)

## Ghi chú

- Dữ liệu kết quả được **hardcode** từ notebook Python, không gọi API
- Biểu đồ sử dụng [Recharts](https://recharts.org/)
- Thiết kế theo phong cách Apple, hỗ trợ responsive
- Tất cả nội dung bằng tiếng Việt
