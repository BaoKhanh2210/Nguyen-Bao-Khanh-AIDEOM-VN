# Kế hoạch Showcase React + Vite + Vercel

> **Mục tiêu**: Website tĩnh showcase 12 bài tập cuối kì — code Python + kết quả (ảnh/text).
> **Repo**: `D:\Code\Python\mamz`
> **Tech**: React 18 + Vite + TypeScript + Tailwind CSS → deploy Vercel

---

## Mục lục

1. [Kiến trúc thư mục](#1-kiến-trúc-thư-mục)
2. [Tech stack chi tiết](#2-tech-stack-chi-tiết)
3. [Data: inventory & mapping](#3-data-inventory--mapping)
4. [Step-by-step implementation](#4-step-by-step-implementation)
   - 4.1 Init Vite project
   - 4.2 Config Tailwind + Vite
   - 4.3 Copy assets (PNG)
   - 4.4 Extract code từ notebook
   - 4.5 Build data layer
   - 4.6 Build components
   - 4.7 Build pages
   - 4.8 Routing + App shell
   - 4.9 Responsive & polish
   - 4.10 Deploy Vercel
5. [Component specs chi tiết](#5-component-specs-chi-tiết)
6. [Page specs chi tiết](#6-page-specs-chi-tiết)
7. [Decisions & trade-offs](#7-decisions--trade-offs)
8. [Timeline](#8-timeline)

---

## 1. Kiến trúc thư mục

```
D:\Code\Python\mamz\mamz-showcase\
│
├── public/
│   └── results/                          # 15 file PNG (copy từ mamz/)
│       ├── bai1_tfp_trend.png
│       ├── bai1_growth_decomposition.png
│       ├── bai2_sensitivity.png
│       ├── bai3_heatmap_sensitivity.png
│       ├── bai4_heatmap_allocation.png
│       ├── bai6_topsis_sensitivity.png
│       ├── bai7_pareto.png
│       ├── bai8_trajectory.png
│       ├── bai9_sankey.png
│       ├── bai9_retraining_threshold.png
│       ├── bai10_stochastic.png
│       ├── bai11_qlearning.png
│       └── bai12_aideom_dashboard.png
│
├── src/
│   ├── main.tsx                          # ReactDOM.createRoot
│   ├── App.tsx                           # BrowserRouter + Routes + Layout
│   ├── index.css                         # Tailwind directives (@import "tailwindcss")
│   │
│   ├── data/
│   │   ├── exercises.ts                  # Exercise[] — metadata 12 bài
│   │   └── codeBlocks.ts                 # Record<number, SubQuestion[]> — code Python
│   │
│   ├── components/
│   │   ├── Layout.tsx                    # Shell: sidebar + main content
│   │   ├── Sidebar.tsx                   # Nav list 12 bài
│   │   ├── CodeBlock.tsx                 # Syntax highlight Python
│   │   ├── ResultImage.tsx               # Ảnh + click-to-zoom modal
│   │   ├── ResultText.tsx                # Text output dạng <pre> monospace
│   │   ├── ResultTable.tsx               # Structured table (nếu cần parse)
│   │   ├── ExerciseCard.tsx              # Card trên Home page
│   │   ├── Tag.tsx                       # Badge tag nhỏ
│   │   └── Accordion.tsx                 # Collapsible section (code + kết quả)
│   │
│   └── pages/
│       ├── Home.tsx                      # Grid 12 cards
│       └── ExercisePage.tsx              # Chi tiết 1 bài
│
├── index.html                            # Vite entry HTML
├── package.json
├── vite.config.ts
├── tsconfig.json
├── tsconfig.app.json
├── tsconfig.node.json
├── postcss.config.js                     # (nếu dùng PostCSS với Tailwind)
└── vercel.json                           # SPA rewrite rule
```

---

## 2. Tech stack chi tiết

| Layer             | Package                                  | Version  | Lý do                                        |
| ----------------- | ---------------------------------------- | -------- | -------------------------------------------- |
| Build tool        | **vite**                                 | ^6.x     | HMR nhanh, build nhỏ                         |
| UI framework      | **react** + **react-dom**                | ^18.x    | De facto standard                            |
| Language          | **typescript**                           | ^5.x     | Type safety                                  |
| Routing           | **react-router-dom**                     | ^6.x     | File-based SPA routing                       |
| Syntax highlight  | **react-syntax-highlighter**             | ^15.x    | Prism engine, nhiều theme                    |
| Styling           | **tailwindcss** + **@tailwindcss/vite**  | ^4.x     | Utility-first, tích hợp Vite plugin          |
| Icons             | **lucide-react**                         | ^0.460+  | Tree-shakeable SVG icons                     |
| Deploy            | **Vercel**                               | —        | `vite build` → static, Vercel auto-detect    |

### Tại sao Tailwind v4 + `@tailwindcss/vite`?

- Tailwind v4 dùng `@import "tailwindcss"` trong CSS (không cần `tailwind.config.js`)
- Plugin `@tailwindcss/vite` thay thế PostCSS → build nhanh hơn
- Không cần `content` array config → auto-detect class trong `.tsx`

---

## 3. Data: inventory & mapping

### 3.1 Mapping 12 bài → slug, title, tags, images, sub-questions

```ts
// src/data/exercises.ts

export interface SubQuestion {
  id: string;           // "1.4.1", "1.4.2", ...
  title: string;        // "Tính A_t (TFP)"
  code: string;         // Python source code cho sub-question này
  results: ResultItem[];
}

export interface ResultItem {
  type: 'text' | 'image';
  title?: string;       // Ví dụ: "Bảng A_t theo năm"
  content: string;      // Text string hoặc path "/results/bai1_tfp_trend.png"
}

export interface Exercise {
  id: number;
  slug: string;
  title: string;
  subtitle: string;     // Mô tả ngắn 1 dòng
  tags: string[];
  image?: string;       // Thumbnail (ảnh đầu tiên)
  subQuestions: SubQuestion[];
}
```

### 3.2 Bảng mapping đầy đủ

| #  | Slug                       | Title                                    | Tags                                             | Ảnh                                                                        | Sub-questions |
| -- | -------------------------- | ---------------------------------------- | ------------------------------------------------ | -------------------------------------------------------------------------- | ------------- |
| 1  | `bai1-cobb-douglas`        | Cobb-Douglas mở rộng (AI & số hóa)      | Cobb-Douglas, TFP, Growth, Forecast              | `bai1_tfp_trend.png`, `bai1_growth_decomposition.png`                      | 1.4.1, 1.4.2, 1.4.3, 1.4.4 |
| 2  | `bai2-budget-allocation`   | Phân bổ ngân sách 4 hạng mục            | LP, linprog, PuLP, Shadow Price, Sensitivity     | `bai2_sensitivity.png`                                                     | 2.4.1, 2.4.2, 2.4.3, 2.4.4 |
| 3  | `bai3-priority-index`      | Chỉ số ưu tiên ngành                     | Min-max, Priority, Sensitivity, Heatmap          | `bai3_heatmap_sensitivity.png`                                             | 3.4.1, 3.4.2, 3.4.3, 3.4.4 |
| 4  | `bai4-regional-lp`         | LP phân bổ vùng miền                     | LP, PuLP, CVXPY, Equity, Heatmap                 | `bai4_heatmap_allocation.png`                                              | 4.4.1, 4.4.2, 4.4.3, 4.4.4 |
| 5  | `bai5-mip-projects`        | MIP chọn dự án                           | MIP, PuLP, Binary, Expected Value, Risk          | _(none — chỉ text output)_                                                 | 5.4.1, 5.4.2, 5.4.3, 5.4.4 |
| 6  | `bai6-topsis`              | TOPSIS xếp hạng vùng                     | TOPSIS, Entropy, AHP, Sensitivity                | `bai6_topsis_sensitivity.png`                                              | 6.4.1, 6.4.2, 6.4.3, 6.4.4 |
| 7  | `bai7-nsga2`               | NSGA-II đa mục tiêu Pareto               | NSGA-II, pymoo, Pareto, TOPSIS, Multi-objective  | `bai7_pareto.png`                                                          | 7.4.1, 7.4.2, 7.4.3, 7.4.4 |
| 8  | `bai8-dynamic-opt`         | Tối ưu động liên thời gian              | SLSQP, Dynamic, Welfare, Shock, Trajectory       | `bai8_trajectory.png`                                                      | 8.3.1, 8.3.3, 8.3.4 |
| 9  | `bai9-labor`               | Tác động AI tới lao động                 | LP, Labor, NetJob, Retraining, Vulnerable        | `bai9_sankey.png`, `bai9_retraining_threshold.png`                         | 9.4.1, 9.4.2, 9.4.3, 9.4.4 |
| 10 | `bai10-stochastic`         | Quy hoạch ngẫu nhiên 2 giai đoạn         | Pyomo, Stochastic, VSS, EVPI, Robust             | `bai10_stochastic.png`                                                     | 10.5.1, 10.5.2, 10.5.3, 10.5.4 |
| 11 | `bai11-qlearning`          | Q-learning chính sách kinh tế            | Q-learning, Gymnasium, RL, Policy                | `bai11_qlearning.png`                                                      | 11.3.1, 11.3.3, 11.3.4 |
| 12 | `bai12-aideom`             | AIDEOM-VN nguyên mẫu tích hợp            | Integration, Cobb-Douglas, TOPSIS, LP, NSGA-II   | `bai12_aideom_dashboard.png`                                               | M1, M2, M3, M4, M5, M6 |

### 3.3 Script extract code từ notebook

```python
# extract_code.py — chạy 1 lần để generate codeBlocks.ts
import json, re

nb = json.load(open('bai_tap_cuoi_ki.ipynb', encoding='utf-8'))

current_bai = None
current_sub = None
output = {}  # {bai_id: [{id, title, code}]}

for cell in nb['cells']:
    src = ''.join(cell['source'])

    # Detect bài mới từ markdown header
    if cell['cell_type'] == 'markdown':
        m = re.search(r'Bài\s+(\d+)', src)
        if m:
            current_bai = int(m.group(1))
            output[current_bai] = []

    # Detect sub-question từ comment trong code
    if cell['cell_type'] == 'code' and current_bai:
        sub_matches = re.findall(r'Cau\s+(\d+\.\d+\.\d+|M\d)', src)
        if sub_matches:
            for sub_id in sub_matches:
                # Split code theo sub-question markers
                pass
        # Hoặc: lưu toàn bộ code 1 bài = 1 block lớn
        output[current_bai].append({
            'id': str(current_bai),
            'title': f'Bài {current_bai}',
            'code': src
        })

# Output: TypeScript file
with open('src/data/codeBlocks.ts', 'w', encoding='utf-8') as f:
    f.write('export const codeBlocks: Record<number, string> = {\n')
    for bai_id, blocks in output.items():
        code = blocks[0]['code'] if blocks else ''
        # Escape backticks + ${} for template literal
        escaped = code.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${')
        f.write(f'  {bai_id}: `{escaped}`,\n')
    f.write('}\n')

print("Done → src/data/codeBlocks.ts")
```

**Lưu ý quan trọng**: Script trên chỉ là template. Cần adjust regex dựa trên format thực tế của notebook. Cách tiếp cận tốt hơn:

1. Chạy notebook trên Colab (miễn phí, có sẵn mọi thư viện)
2. Copy-paste output text vào `results.ts`
3. Code thì extract tự động bằng script trên

---

## 4. Step-by-step implementation

### 4.1 Init Vite project

```powershell
# Tại D:\Code\Python\mamz
npm create vite@latest mamz-showcase -- --template react-ts
cd mamz-showcase
```

Output sẽ tạo:
```
mamz-showcase/
├── index.html
├── package.json
├── tsconfig.json
├── tsconfig.app.json
├── tsconfig.node.json
├── vite.config.ts
└── src/
    ├── main.tsx
    ├── App.tsx
    ├── App.css
    ├── index.css
    └── vite-env.d.ts
```

### 4.2 Install dependencies + config

```powershell
cd mamz-showcase

# Dependencies
npm install react-router-dom react-syntax-highlighter lucide-react
npm install -D tailwindcss @tailwindcss/vite @types/react-syntax-highlighter
```

**`vite.config.ts`** — thêm Tailwind plugin:
```ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
})
```

**`src/index.css`** — Tailwind v4 directives:
```css
@import "tailwindcss";
```

Xóa `App.css` (không cần).

**`vercel.json`** — SPA rewrite (để refresh không 404):
```json
{
  "rewrites": [{ "source": "/(.*)", "destination": "/" }]
}
```

### 4.3 Copy assets (PNG)

```powershell
# Tại D:\Code\Python\mamz
mkdir mamz-showcase\public\results
Copy-Item bai1_tfp_trend.png mamz-showcase\public\results\
Copy-Item bai1_growth_decomposition.png mamz-showcase\public\results\
Copy-Item bai2_sensitivity.png mamz-showcase\public\results\
Copy-Item bai3_heatmap_sensitivity.png mamz-showcase\public\results\
Copy-Item bai4_heatmap_allocation.png mamz-showcase\public\results\
Copy-Item bai6_topsis_sensitivity.png mamz-showcase\public\results\
Copy-Item bai7_pareto.png mamz-showcase\public\results\
Copy-Item bai8_trajectory.png mamz-showcase\public\results\
Copy-Item bai9_sankey.png mamz-showcase\public\results\
Copy-Item bai9_retraining_threshold.png mamz-showcase\public\results\
Copy-Item bai10_stochastic.png mamz-showcase\public\results\
Copy-Item bai11_qlearning.png mamz-showcase\public\results\
Copy-Item bai12_aideom_dashboard.png mamz-showcase\public\results\
```

### 4.4 Extract code từ notebook

Cách tiếp cận: **dùng Python script để parse `.ipynb` JSON**.

`.ipynb` là JSON có cấu trúc:
```json
{
  "cells": [
    { "cell_type": "markdown", "source": ["# Title\n"] },
    { "cell_type": "code", "source": ["import numpy\n", "import pandas\n"] }
  ]
}
```

**Script `extract_code.py`** (chạy tại `D:\Code\Python\mamz`):

```python
import json, re, os

with open('bai_tap_cuoi_ki.ipynb', encoding='utf-8') as f:
    nb = json.load(f)

# Parse: tách code theo bài (cell markdown có "## Bài X")
exercises = {}  # {1: [code_cell_1, code_cell_2, ...], 2: [...]}
current_bai = None
setup_code = ""  # Cell setup chung

for cell in nb['cells']:
    src = ''.join(cell['source'])

    if cell['cell_type'] == 'markdown':
        m = re.search(r'##\s*Bài\s+(\d+)', src)
        if m:
            current_bai = int(m.group(1))
            exercises[current_bai] = []
    elif cell['cell_type'] == 'code':
        if current_bai is None:
            setup_code += src + "\n"
        else:
            exercises.setdefault(current_bai, []).append(src)

# Output directory
os.makedirs('mamz-showcase/src/data', exist_ok=True)

with open('mamz-showcase/src/data/codeBlocks.ts', 'w', encoding='utf-8') as f:
    f.write('// Auto-generated from bai_tap_cuoi_ki.ipynb\n')
    f.write('// Each key = bài number, value = array of code cell strings\n\n')
    f.write('export const codeBlocks: Record<number, string[]> = {\n')

    for bai_id in sorted(exercises.keys()):
        cells = exercises[bai_id]
        f.write(f'  {bai_id}: [\n')
        for cell_code in cells:
            escaped = cell_code.replace('\\', '\\\\') \
                               .replace('`', '\\`') \
                               .replace('${', '\\${')
            f.write(f'    `{escaped}`,\n')
        f.write('  ],\n')

    f.write('}\n')

print(f"Extracted {len(exercises)} bài → mamz-showcase/src/data/codeBlocks.ts")
for bai_id, cells in exercises.items():
    total_lines = sum(c.count('\n') for c in cells)
    print(f"  Bài {bai_id}: {len(cells)} cells, ~{total_lines} lines")
```

### 4.5 Build data layer

#### `src/data/exercises.ts`

```ts
export interface ResultItem {
  type: 'text' | 'image'
  title?: string
  content: string
}

export interface SubQuestion {
  id: string
  title: string
  codeIndex: number        // index vào codeBlocks[baiId][codeIndex]
  results: ResultItem[]
}

export interface Exercise {
  id: number
  slug: string
  title: string
  subtitle: string
  tags: string[]
  thumbnail?: string       // path trong /results/
  subQuestions: SubQuestion[]
}

export const exercises: Exercise[] = [
  {
    id: 1,
    slug: 'bai1-cobb-douglas',
    title: 'Bài 1 — Cobb-Douglas mở rộng',
    subtitle: 'Mô hình sản xuất tích hợp AI & số hóa, tính TFP, phân tích tăng trưởng',
    tags: ['Cobb-Douglas', 'TFP', 'Growth Decomposition', 'Forecast'],
    thumbnail: '/results/bai1_tfp_trend.png',
    subQuestions: [
      {
        id: '1.4.1',
        title: 'Tính Solow residual A_t (TFP)',
        codeIndex: 0,
        results: [
          { type: 'text', title: 'Bảng A_t theo năm 2020-2025', content: '...' },
          { type: 'image', title: 'Xu hướng A_t', content: '/results/bai1_tfp_trend.png' },
        ],
      },
      {
        id: '1.4.2',
        title: 'Dự báo sản lượng & MAPE',
        codeIndex: 0, // cùng cell code, phần dưới
        results: [
          { type: 'text', title: 'Bảng dự báo Y và MAPE', content: '...' },
        ],
      },
      {
        id: '1.4.3',
        title: 'Phân rã tăng trưởng GDP',
        codeIndex: 0,
        results: [
          { type: 'text', title: 'Bảng phân rã tăng trưởng', content: '...' },
          { type: 'image', title: 'Biểu đồ phân rã', content: '/results/bai1_growth_decomposition.png' },
        ],
      },
      {
        id: '1.4.4',
        title: 'Kịch bản đến 2030',
        codeIndex: 0,
        results: [
          { type: 'text', title: 'GDP dự báo 2030', content: '...' },
        ],
      },
    ],
  },
  // ... 11 bài tiếp theo (xem Section 3.2 cho mapping)
  {
    id: 2,
    slug: 'bai2-budget-allocation',
    title: 'Bài 2 — Phân bổ ngân sách 4 hạng mục',
    subtitle: 'Linear Programming: linprog, PuLP, CVXPY — phân tích shadow price & độ nhạy',
    tags: ['LP', 'linprog', 'PuLP', 'Shadow Price', 'Sensitivity'],
    thumbnail: '/results/bai2_sensitivity.png',
    subQuestions: [
      { id: '2.4.1', title: 'Giai bang scipy.optimize.linprog', codeIndex: 0, results: [
        { type: 'text', title: 'Kết quả LP', content: '...' },
      ]},
      { id: '2.4.2', title: 'Giai bang PuLP + shadow prices', codeIndex: 0, results: [
        { type: 'text', title: 'Shadow prices', content: '...' },
      ]},
      { id: '2.4.3', title: 'Phân tích độ nhạy ngân sách', codeIndex: 0, results: [
        { type: 'text', title: 'Bảng Z*(B)', content: '...' },
        { type: 'image', title: 'Đường cong Z*(B)', content: '/results/bai2_sensitivity.png' },
      ]},
      { id: '2.4.4', title: 'Ràng buộc x3 >= 30', codeIndex: 0, results: [
        { type: 'text', title: 'Kết quả khi x3 >= 30', content: '...' },
      ]},
    ],
  },
  // Bài 3-12: tương tự, điền đầy đủ khi có output
]
```

> **Lưu ý**: Trường `content` của `type: 'text'` sẽ được hardcode khi chạy notebook xong. Hiện tại để placeholder `'...'`.

### 4.6 Build components

Xem [Section 5: Component specs chi tiết](#5-component-specs-chi-tiết) bên dưới.

### 4.7 Build pages

Xem [Section 6: Page specs chi tiết](#6-page-specs-chi-tiết) bên dưới.

### 4.8 Routing + App shell

**`src/App.tsx`**:
```tsx
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { Layout } from './components/Layout'
import { Home } from './pages/Home'
import { ExercisePage } from './pages/ExercisePage'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<Home />} />
          <Route path="/bai/:slug" element={<ExercisePage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}
```

**`src/main.tsx`**:
```tsx
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App'
import './index.css'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
```

### 4.9 Responsive & polish

- **Bảng rộng** (heatmap, bảng nhiều cột): wrap trong `<div class="overflow-x-auto">`
- **Ảnh**: `max-w-full h-auto` + click-to-zoom modal
- **Code block**: `overflow-x-auto` + font-size nhỏ trên mobile (`text-xs sm:text-sm`)
- **Sidebar**: ẩn trên mobile, hiện hamburger menu
- **Breakpoint chính**: `sm:640px`, `md:768px`, `lg:1024px`

### 4.10 Deploy Vercel

```powershell
# Build
npm run build

# Option A: Vercel CLI
npx vercel --prod

# Option B: Push lên GitHub → connect Vercel dashboard
# Vercel auto-detect Vite framework, không cần config thêm
```

**`vercel.json`** (đã tạo ở Step 4.2):
```json
{
  "rewrites": [{ "source": "/(.*)", "destination": "/" }]
}
```

---

## 5. Component specs chi tiết

### 5.1 `Layout.tsx`

```
┌─────────────────────────────────────────────┐
│ Header: "AIDEOM-VN Final Exam Showcase"     │
├──────────┬──────────────────────────────────┤
│ Sidebar  │ <Outlet /> (page content)        │
│ - Home   │                                  │
│ - Bai 1  │                                  │
│ - Bai 2  │                                  │
│ - ...    │                                  │
│ - Bai 12 │                                  │
├──────────┴──────────────────────────────────┤
│ Footer: © 2026                              │
└─────────────────────────────────────────────┘
```

```tsx
import { Outlet } from 'react-router-dom'
import { Sidebar } from './Sidebar'

export function Layout() {
  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <header className="bg-white border-b px-6 py-4 sticky top-0 z-10">
        <h1 className="text-xl font-bold">AIDEOM-VN Final Exam Showcase</h1>
      </header>
      <div className="flex flex-1">
        <Sidebar />
        <main className="flex-1 p-6 max-w-5xl">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
```

### 5.2 `Sidebar.tsx`

- Danh sách 12 bài + link Home
- `NavLink` từ react-router-dom → active state highlight
- Sticky left, scroll independently
- Mobile: hidden by default, toggle hamburger

```tsx
import { NavLink } from 'react-router-dom'
import { exercises } from '../data/exercises'
import { Home, ChevronRight } from 'lucide-react'

export function Sidebar() {
  return (
    <aside className="hidden md:block w-64 border-r bg-white p-4 sticky top-16 h-[calc(100vh-4rem)] overflow-y-auto">
      <nav className="space-y-1">
        <NavLink to="/" end className="...">Home</NavLink>
        {exercises.map(ex => (
          <NavLink key={ex.id} to={`/bai/${ex.slug}`} className="...">
            <span className="font-mono text-xs mr-2">{ex.id}</span>
            {ex.title.split('—')[0].trim()}
          </NavLink>
        ))}
      </nav>
    </aside>
  )
}
```

### 5.3 `CodeBlock.tsx`

```tsx
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism'
import { useState } from 'react'
import { ChevronDown, ChevronRight, Copy, Check } from 'lucide-react'

interface Props {
  code: string
  title?: string
  defaultOpen?: boolean  // false = collapsed
}

export function CodeBlock({ code, title, defaultOpen = false }: Props) {
  const [open, setOpen] = useState(defaultOpen)
  const [copied, setCopied] = useState(false)

  const handleCopy = () => {
    navigator.clipboard.writeText(code)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className="border rounded-lg overflow-hidden">
      <button
        onClick={() => setOpen(!open)}
        className="w-full flex items-center gap-2 px-4 py-2 bg-gray-800 text-white text-sm"
      >
        {open ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
        <span className="flex-1 text-left">{title || 'Source Code (Python)'}</span>
        <span onClick={handleCopy} className="cursor-pointer">
          {copied ? <Check size={16} /> : <Copy size={16} />}
        </span>
      </button>
      {open && (
        <SyntaxHighlighter
          language="python"
          style={oneDark}
          showLineNumbers
          customStyle={{ margin: 0, fontSize: '0.85rem' }}
        >
          {code}
        </SyntaxHighlighter>
      )}
    </div>
  )
}
```

### 5.4 `ResultImage.tsx`

```tsx
import { useState } from 'react'
import { X, ZoomIn } from 'lucide-react'

interface Props {
  src: string
  alt?: string
  title?: string
}

export function ResultImage({ src, alt, title }: Props) {
  const [zoomed, setZoomed] = useState(false)

  return (
    <div className="space-y-2">
      {title && <h4 className="text-sm font-medium text-gray-700">{title}</h4>}
      <div className="relative group cursor-pointer" onClick={() => setZoomed(true)}>
        <img src={src} alt={alt || title || ''} className="max-w-full h-auto rounded border" />
        <div className="absolute inset-0 bg-black/0 group-hover:bg-black/10 flex items-center justify-center transition">
          <ZoomIn className="text-white opacity-0 group-hover:opacity-100" />
        </div>
      </div>

      {zoomed && (
        <div className="fixed inset-0 z-50 bg-black/80 flex items-center justify-center p-4"
             onClick={() => setZoomed(false)}>
          <button className="absolute top-4 right-4 text-white"><X size={24} /></button>
          <img src={src} alt={alt || ''} className="max-w-full max-h-full object-contain" />
        </div>
      )}
    </div>
  )
}
```

### 5.5 `ResultText.tsx`

```tsx
interface Props {
  content: string
  title?: string
}

export function ResultText({ content, title }: Props) {
  return (
    <div className="space-y-1">
      {title && <h4 className="text-sm font-medium text-gray-700">{title}</h4>}
      <pre className="bg-gray-900 text-green-400 p-4 rounded text-xs sm:text-sm overflow-x-auto font-mono">
        {content}
      </pre>
    </div>
  )
}
```

### 5.6 `ExerciseCard.tsx`

```tsx
import { Link } from 'react-router-dom'
import { Exercise } from '../data/exercises'
import { Tag } from './Tag'

export function ExerciseCard({ exercise }: { exercise: Exercise }) {
  return (
    <Link to={`/bai/${exercise.slug}`}
          className="block bg-white rounded-xl border hover:shadow-lg transition p-0 overflow-hidden">
      {exercise.thumbnail && (
        <img src={exercise.thumbnail} alt={exercise.title}
             className="w-full h-40 object-cover" />
      )}
      <div className="p-4 space-y-2">
        <div className="flex items-center gap-2">
          <span className="text-xs font-mono bg-blue-100 text-blue-700 px-2 py-0.5 rounded">
            Bài {exercise.id}
          </span>
        </div>
        <h3 className="font-semibold text-sm">{exercise.title}</h3>
        <p className="text-xs text-gray-500">{exercise.subtitle}</p>
        <div className="flex flex-wrap gap-1">
          {exercise.tags.slice(0, 3).map(tag => <Tag key={tag} label={tag} />)}
        </div>
      </div>
    </Link>
  )
}
```

### 5.7 `Accordion.tsx`

Dùng cho mỗi sub-question: click header → expand code + results.

```tsx
import { useState, ReactNode } from 'react'
import { ChevronDown, ChevronRight } from 'lucide-react'

interface Props {
  title: string
  id: string
  children: ReactNode
  defaultOpen?: boolean
}

export function Accordion({ title, id, children, defaultOpen = false }: Props) {
  const [open, setOpen] = useState(defaultOpen)

  return (
    <div className="border rounded-lg overflow-hidden">
      <button
        onClick={() => setOpen(!open)}
        className="w-full flex items-center gap-2 px-4 py-3 bg-white hover:bg-gray-50 text-left"
      >
        {open ? <ChevronDown size={18} /> : <ChevronRight size={18} />}
        <span className="font-mono text-xs text-blue-600 mr-2">{id}</span>
        <span className="font-medium">{title}</span>
      </button>
      {open && <div className="p-4 space-y-4 border-t">{children}</div>}
    </div>
  )
}
```

---

## 6. Page specs chi tiết

### 6.1 `Home.tsx`

Hiển thị grid 12 ExerciseCard.

```tsx
import { exercises } from '../data/exercises'
import { ExerciseCard } from '../components/ExerciseCard'

export function Home() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold">Đề bài cuối kì</h2>
        <p className="text-gray-500 mt-1">
          12 bài tập tích hợp — Các mô hình ra quyết định
        </p>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {exercises.map(ex => (
          <ExerciseCard key={ex.id} exercise={ex} />
        ))}
      </div>
    </div>
  )
}
```

Layout:
```
┌─────────────────────────────────────────────┐
│  Đề bài cuối kì                             │
│  12 bài tập tích hợp — Các mô hình ...      │
├─────────────┬─────────────┬─────────────────┤
│ [Card 1]    │ [Card 2]    │ [Card 3]        │
│ [img]       │ [img]       │ [img]           │
│ Bài 1       │ Bài 2       │ Bài 3           │
│ Cobb-Douglas│ Budget LP   │ Priority Index  │
├─────────────┼─────────────┼─────────────────┤
│ [Card 4]    │ [Card 5]    │ [Card 6]        │
│ ...         │ ...         │ ...             │
├─────────────┼─────────────┼─────────────────┤
│ [Card 7]    │ [Card 8]    │ [Card 9]        │
├─────────────┼─────────────┼─────────────────┤
│ [Card 10]   │ [Card 11]   │ [Card 12]       │
└─────────────┴─────────────┴─────────────────┘
```

### 6.2 `ExercisePage.tsx`

```tsx
import { useParams, Link } from 'react-router-dom'
import { exercises } from '../data/exercises'
import { codeBlocks } from '../data/codeBlocks'
import { CodeBlock } from '../components/CodeBlock'
import { ResultImage } from '../components/ResultImage'
import { ResultText } from '../components/ResultText'
import { Accordion } from '../components/Accordion'
import { Tag } from '../components/Tag'
import { ArrowLeft, ArrowRight } from 'lucide-react'

export function ExercisePage() {
  const { slug } = useParams<{ slug: string }>()
  const exercise = exercises.find(e => e.slug === slug)

  if (!exercise) return <div>Bài tập không tồn tại.</div>

  const code = codeBlocks[exercise.id] || []
  const prevExercise = exercises.find(e => e.id === exercise.id - 1)
  const nextExercise = exercises.find(e => e.id === exercise.id + 1)

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="space-y-3">
        <div className="flex items-center gap-2">
          <span className="text-xs font-mono bg-blue-100 text-blue-700 px-2 py-0.5 rounded">
            Bài {exercise.id}
          </span>
          {exercise.tags.map(tag => <Tag key={tag} label={tag} />)}
        </div>
        <h1 className="text-2xl font-bold">{exercise.title}</h1>
        <p className="text-gray-500">{exercise.subtitle}</p>
      </div>

      {/* Code section — 1 cell code cho toàn bài */}
      {code.length > 0 && (
        <CodeBlock code={code[0]} title={`Source Code — Bài ${exercise.id}`} defaultOpen={false} />
      )}

      {/* Results — theo sub-question */}
      <div className="space-y-4">
        <h2 className="text-lg font-semibold">Kết quả</h2>
        {exercise.subQuestions.map(sq => (
          <Accordion key={sq.id} id={sq.id} title={sq.title}>
            {sq.results.map((r, i) =>
              r.type === 'image' ? (
                <ResultImage key={i} src={r.content} title={r.title} />
              ) : (
                <ResultText key={i} content={r.content} title={r.title} />
              )
            )}
          </Accordion>
        ))}
      </div>

      {/* Navigation */}
      <div className="flex justify-between pt-8 border-t">
        {prevExercise ? (
          <Link to={`/bai/${prevExercise.slug}`} className="flex items-center gap-2 text-blue-600">
            <ArrowLeft size={16} /> Bài {prevExercise.id}
          </Link>
        ) : <div />}
        {nextExercise ? (
          <Link to={`/bai/${nextExercise.slug}`} className="flex items-center gap-2 text-blue-600">
            Bài {nextExercise.id} <ArrowRight size={16} />
          </Link>
        ) : <div />}
      </div>
    </div>
  )
}
```

Layout trang chi tiết:
```
┌─────────────────────────────────────────────┐
│  [Bài 1] [Cobb-Douglas] [TFP] [Growth]      │
│                                              │
│  Bài 1 — Cobb-Douglas mở rộng               │
│  Mô hình sản xuất tích hợp AI & số hóa...   │
│                                              │
│  ┌─ Source Code — Bài 1 ──────────────────┐  │
│  │ ▶ (click to expand)                    │  │
│  └────────────────────────────────────────┘  │
│                                              │
│  ## Kết quả                                  │
│                                              │
│  ┌─ 1.4.1 — Tính Solow residual A_t ─────┐  │
│  │ ▶ (click to expand)                    │  │
│  │   [text: Bảng A_t theo năm]           │  │
│  │   [image: Xu hướng A_t]               │  │
│  └────────────────────────────────────────┘  │
│                                              │
│  ┌─ 1.4.2 — Dự báo sản lượng & MAPE ────┐  │
│  │ ▶ (collapsed)                          │  │
│  └────────────────────────────────────────┘  │
│                                              │
│  ┌─ 1.4.3 — Phân rã tăng trưởng ────────┐  │
│  │ ▶ (collapsed)                          │  │
│  └────────────────────────────────────────┘  │
│                                              │
│  ┌─ 1.4.4 — Kịch bản 2030 ──────────────┐  │
│  │ ▶ (collapsed)                          │  │
│  └────────────────────────────────────────┘  │
│                                              │
│  ◄ Home                        Bài 2 ►      │
└─────────────────────────────────────────────┘
```

---

## 7. Decisions & trade-offs

| #  | Quyết định                        | Lựa chọn                          | Lý do                                                         |
| -- | --------------------------------- | --------------------------------- | ------------------------------------------------------------- |
| 1  | Code: 1 block hay tách sub?       | **1 block/bài** + accordion kết quả | Tránh phức tạp parse, code 1 bài liền mạch dễ đọc hơn        |
| 2  | Text output: hardcode hay runtime? | **Hardcode** trong `results.ts`  | Static site, không chạy Python trên browser                   |
| 3  | Bài 5 không có PNG                 | **Chỉ hiển text output**          | Không cần tạo ảnh giả                                         |
| 4  | Sidebar hay top nav?               | **Sidebar** (desktop) + hamburger (mobile) | Phù hợp 12 bài, dễ navigate                           |
| 5  | Tailwind v4 hay v3?                | **v4** + `@tailwindcss/vite`     | Nhanh hơn, không cần config file                              |
| 6  | Dark mode?                         | **Không** (chỉ light)             | Giản đơn, notebook gốc không có dark mode                    |
| 7  | i18n?                              | **Không** (chỉ tiếng Việt)        | Notebook viết tiếng Việt                                      |
| 8  | Markdown render cho text output?   | **Không** — dùng `<pre>` monospace | Text output là plain text, không cần Markdown                 |
| 9  | Table parsing từ text output?      | **Manual** — hardcode HTML table hoặc giữ `<pre>` | Text format không đồng đều, parse fragile        |
| 10 | Framer Motion animation?           | **Không** — chỉ CSS transition    | Đơn giản, ít dependency                                       |

---

## 8. Timeline

| Bước | Nội dung                                                        | Output                                           | Thời gian |
| ---- | --------------------------------------------------------------- | ------------------------------------------------ | --------- |
| 1    | `npm create vite` + install deps + config Tailwind + vercel.json | Project skeleton chạy được `npm run dev`         | 5 phút    |
| 2    | Copy 13 PNG vào `public/results/`                               | Ảnh sẵn sàng                                     | 1 phút    |
| 3    | Viết `extract_code.py` → chạy → generate `codeBlocks.ts`        | 12 entry code Python                             | 10 phút   |
| 4    | Viết `exercises.ts` metadata 12 bài (template, placeholder text)| Data layer hoàn chỉnh                            | 15 phút   |
| 5    | Build `CodeBlock`, `ResultImage`, `ResultText`, `Tag`           | 4 components base                                | 10 phút   |
| 6    | Build `Accordion`, `ExerciseCard`, `Sidebar`, `Layout`          | 4 components composite                           | 10 phút   |
| 7    | Build `Home` page                                               | Grid 12 cards                                    | 5 phút    |
| 8    | Build `ExercisePage`                                            | Trang chi tiết với code + accordion results      | 10 phút   |
| 9    | Chạy notebook trên Colab → copy text output vào `exercises.ts`  | Kết quả thực tế đầy đủ                          | 15 phút   |
| 10   | Responsive check + polish CSS                                   | Mobile-friendly                                  | 10 phút   |
| 11   | `npm run build` + deploy Vercel                                 | Live URL                                         | 2 phút    |

**Tổng: ~93 phút**
