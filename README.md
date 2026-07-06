需要先搜尋載入檔案寫入工具。# 🌾 Rice Field Sim（稻田模擬器）

一個以 **Python + Tkinter** 打造的**網格化路徑規劃模擬器**。畫面上有一台 3×3 的車子從稻田左下角出發，依照可插拔的「走法策略（Strategy）」在網格中移動，最終抵達指定出口。模擬過程會即時視覺化，並自動把每一步的軌跡與結果摘要輸出到檔案。

> 專案定位：教學／實驗用的**策略模式（Strategy Pattern）示範**與**路徑演算法沙盒**。你可以輕鬆新增自己的走法，觀察它在稻田中如何移動、走了多少距離、能否成功抵達出口。

---

## 📑 目錄

- [專案特色](#-專案特色)
- [畫面示意](#-畫面示意)
- [專案結構](#-專案結構)
- [環境需求與安裝](#-環境需求與安裝)
- [快速開始](#-快速開始)
- [核心概念說明](#-核心概念說明)
- [內建走法策略](#-內建走法策略)
- [如何自訂新的走法策略](#-如何自訂新的走法策略)
- [輸出結果說明](#-輸出結果說明)
- [設定參數說明](#-設定參數說明)
- [已知事項 / TODO](#-已知事項--todo)
- [授權](#-授權)

---

## ✨ 專案特色

- **即時視覺化**：使用 Tkinter Canvas 繪製網格、出口與車子，逐步動畫呈現移動過程。
- **策略模式架構**：走法（策略）與模擬引擎完全解耦，新增走法不需要動到核心程式。
- **可設定的稻田**：網格寬高、格子像素、車子大小、出口位置皆可自由設定。
- **多出口支援**：可設定多個出口，車子會自動選擇曼哈頓距離最近的出口。
- **距離計算**：直線移動計 `car_size` 格，斜向移動以 √2 加權（更貼近真實距離）。
- **自動存檔**：模擬結束後自動輸出「逐步軌跡 log」與「結果摘要」兩份檔案。

---

## 🖼 畫面示意

執行後會出現一個視窗：

- 淺灰色格線＝稻田網格
- 綠色方塊（標示「出口」）＝目標出口
- 藍色方塊＝車子（3×3 大小）
- 視窗上方文字＝目前走法名稱、累計移動距離

```
走法：spiral + dash | 總移動距離：xxx 格 (每次移動 3 格)
┌─────────────────────────────┐
│  · · · · · · · · · · · · ·   │
│  · · · · · · · · · · · · ·   │
│  · · · · · · · · ┌──┐ · · ·   │  ← 出口
│  · · · · · · · · └──┘ · · ·   │
│  ┌──┐ · · · · · · · · · · ·   │  ← 車子
│  └──┘ · · · · · · · · · · ·   │
└─────────────────────────────┘
```

---

## 📂 專案結構

```text
Rice_field_sim/
├── build.sh                    # 一鍵建立專案骨架的 shell 腳本
├── revise.md                   # 開發修訂紀錄
└── RiceFieldSim/
    ├── main.py                 # 程式進入點（設定稻田、選擇走法、啟動模擬）
    ├── README.md               # 環境建置說明
    ├── core/                   # 核心模組（與走法無關的基礎設施）
    │   ├── __init__.py
    │   ├── grid.py             # Grid：稻田網格、座標轉換、出口計算
    │   ├── car.py              # Car：車子狀態、移動與距離累計
    │   └── simulator.py        # Simulator：Tkinter 視覺化與模擬主迴圈
    ├── strategies/             # 走法策略（可插拔）
    │   ├── __init__.py
    │   ├── base.py             # MovementStrategy：策略抽象基底類別
    │   └── spiral_dash.py      # SpiralDashStrategy：螺旋 + 衝刺走法
    └── results/                # 模擬結果輸出資料夾（log 與摘要）
        └── .gitkeep
```

> ⚠️ **注意**：`main.py` 目前另外 import 了 `strategies.zigzag`（ZigzagStrategy）與 `strategies.best`（AdaptiveOptimalStrategy），但這兩個檔案尚未包含在 repository 中。若要執行預設的 `main("zigzag")`，你需要先自行補上這兩個策略檔（見 [如何自訂新的走法策略](#-如何自訂新的走法策略)），或改為只使用已存在的 `spiral_dash` 走法。

---

## 🛠 環境需求與安裝

- **Python 版本**：3.10.0
- **主要相依套件**：`tkinter`（標準函式庫內建，大多數 Python 發行版皆已內含）

### 使用 Conda / Mamba 建立環境（建議）

```bash
# 使用 mamba（速度較快）或將 mamba 換成 conda
mamba create -n RiceFieldSim python=3.10.0
conda activate RiceFieldSim
```

> 本專案未使用額外的第三方套件（純標準函式庫 + tkinter），因此不需要額外 `pip install`。若你的環境（例如某些 Linux 精簡版）缺少 tkinter，請依系統另行安裝，例如 Ubuntu：`sudo apt-get install python3-tk`。

---

## 🚀 快速開始

### 1. 取得專案

```bash
git clone https://github.com/kevinhuang09/Rice_field_sim.git
cd Rice_field_sim
```

### 2.（可選）用腳本重建骨架

`build.sh` 可以一鍵建立整個資料夾與空白檔案骨架：

```bash
bash build.sh              # 預設建立名為 RiceFieldSim 的專案
bash build.sh MyProject    # 或自訂專案名稱
```

### 3. 執行模擬

```bash
cd RiceFieldSim
python main.py
```

### 4. 切換走法

打開 `main.py`，在最底部切換要執行的走法：

```python
if __name__ == "__main__":
    main("zigzag")        # 目前的預設（需先補上 zigzag 策略檔）
    # main("spiral_dash") # 已內建，可直接使用
    # main("select_best") # 需先補上 best 策略檔
```

> 若只想立即跑起來，建議先改成 `main("spiral_dash")`，因為那是目前 repo 中已完整實作的走法。

---

## 🧠 核心概念說明

### `core/grid.py` — 稻田網格 `Grid`

負責描述稻田本身以及所有座標相關運算：

| 屬性 / 方法 | 說明 |
|---|---|
| `grid_width` / `grid_height` | 網格的寬與高（格數） |
| `cell_pixel` | 每一格在畫面上的像素大小 |
| `car_size` | 車子邊長（幾格），也是每次移動的步長 |
| `offset` | 畫面邊界留白 |
| `exits` | 出口清單（支援多個出口） |
| `canvas_width` / `canvas_height` | 依網格自動計算的畫布尺寸 |
| `max_x` / `max_y` | 車子左下角可到達的最大座標（`grid_width - car_size`） |
| `nearest_exit(x, y)` | 回傳離目前位置**曼哈頓距離最近**的出口 |
| `to_canvas_coords(gx, gy)` | 把網格座標轉換為 Tkinter 畫布像素座標（並做 Y 軸翻轉，讓原點在左下角） |

### `core/car.py` — 車子 `Car`

追蹤車子的位置與累計移動距離：

- `move_to(new_x, new_y)`：移動車子，並累計距離。
  - **直線移動**：距離加 `car_size` 格。
  - **斜向移動**（X、Y 同時改變）：距離以 `car_size × √2 ≈ car_size × 1.414` 計算。
- `position`：回傳目前 `(x, y)` 座標。

### `core/simulator.py` — 模擬引擎 `Simulator`

整個模擬的主控者，負責：

1. 建立 Tkinter 視窗、畫布，繪製網格、出口與車子。
2. 依 `delay_ms` 週期性呼叫 `_tick()`，每個 tick 讓策略走一步。
3. 逐步在終端機印出、並蒐集每一步的軌跡 log。
4. 判斷模擬是否結束（策略回傳 `False` 代表結束）。
5. 結束後呼叫 `strategy.on_finish()` 並把結果寫入 `results/`。

---

## 🧭 內建走法策略

所有走法都繼承自 `strategies/base.py` 的 `MovementStrategy` 抽象類別，必須實作 `step(self, grid, car)` 方法。

### `SpiralDashStrategy`（`spiral_dash.py`）— 「螺旋 + 衝刺」

名稱：`spiral + dash`

分為兩個階段：

1. **螺旋階段（spiral）**
   - 車子沿著 `RIGHT → UP → LEFT → DOWN` 的順序繞圈前進。
   - 優先以「大步（`car_size` 格）」前進；若剩餘空間不足一大步但仍有空間，則以「小步貼邊」補齊。
   - 撞到邊界時**安全轉向**並**縮小可移動邊界**（螺旋向內收斂）。
   - 轉向後立即嘗試在新方向走一步，避免原地空轉。
   - 當螺旋收斂到再也走不動時，切換到衝刺階段。
2. **衝刺階段（dash）**
   - 直接朝**最近的出口**方向逼近，每步以 `car_size` 為步長向出口靠攏。
   - 抵達出口座標後結束模擬。

### `ZigzagStrategy`（`zigzag`）與 `AdaptiveOptimalStrategy`（`select_best`）

- 這兩個走法已在 `main.py` 的 `STRATEGY_REGISTRY` 中登錄，但**對應的策略檔目前尚未包含在 repository 中**。
- 若要使用，請依下一節說明自行實作 `strategies/zigzag.py` 與 `strategies/best.py`。

---

## 🧩 如何自訂新的走法策略

只要三步就能加入你自己的走法：

**第 1 步**：在 `strategies/` 下新增一個檔案，例如 `my_strategy.py`：

```python
from strategies.base import MovementStrategy

class MyStrategy(MovementStrategy):
    name = "my awesome strategy"

    def __init__(self, grid):
        # 在這裡初始化你需要的狀態
        pass

    def step(self, grid, car):
        """
        每個 tick 會被呼叫一次，讓車子走一步。
        回傳 True  -> 模擬繼續
        回傳 False -> 模擬結束
        """
        target_x, target_y = grid.nearest_exit(car.x, car.y)
        # ... 你的移動邏輯 ...
        car.move_to(new_x, new_y)
        if (car.x, car.y) == (target_x, target_y):
            return False
        return True
```

**第 2 步**：在 `main.py` 匯入並登錄到 `STRATEGY_REGISTRY`：

```python
from strategies.my_strategy import MyStrategy

STRATEGY_REGISTRY = {
    "spiral_dash": lambda grid: SpiralDashStrategy(grid),
    "my_strategy": lambda grid: MyStrategy(grid),   # ← 新增這行
}
```

**第 3 步**：在 `main.py` 底部呼叫：

```python
if __name__ == "__main__":
    main("my_strategy")
```

---

## 📄 輸出結果說明

每次模擬結束後，`Simulator` 會在 `results/` 資料夾產生**兩個檔案**（檔名含時間戳與走法名稱）：

1. **逐步軌跡 log**：`YYYYMMDD_HHMMSS_<走法>_log.txt`
   ```
   走法：spiral + dash
   時間：20260706_183814
   ========================================
   step    1 | 座標 ( 3,  0) | 累計距離 3 格
   step    2 | 座標 ( 6,  0) | 累計距離 6 格
   ...
   ```

2. **結果摘要**：`YYYYMMDD_HHMMSS_<走法>_summary.txt`
   ```
   ==== 模擬結果摘要 ====
   走法名稱 : spiral + dash
   總步數 : 42
   總移動距離 : 168 格
   最終座標 : (27, 27)
   是否抵達出口: 是
   ```

---

## ⚙️ 設定參數說明

在 `main.py` 中透過 `Grid(...)` 與 `Simulator(...)` 調整模擬設定：

```python
grid = Grid(
    grid_width=30,     # 網格寬（格數）
    grid_height=32,    # 網格高（格數）
    cell_pixel=20,     # 每格像素
    car_size=3,        # 車子邊長 / 步長
    offset=10,         # 畫面留白
    exits=[(27, 27)]   # 出口座標（可多個）
)

sim = Simulator(
    root,
    strategy=strategy,
    grid=grid,
    delay_ms=100,          # 每步之間的動畫延遲（毫秒），越小動得越快
    results_dir="results"  # 結果輸出資料夾
)
```

---

## 📌 已知事項 / TODO

依據 `revise.md` 的修訂紀錄與目前程式狀態：

- [x] `grid_size` 已拆分為 `grid_width` 與 `grid_height`。
- [x] 已加入「抵達出口品質（quality of exit）」的判斷（`summary` 中的「是否抵達出口」）。
- [ ] 補齊 `strategies/zigzag.py`（`ZigzagStrategy`）。
- [ ] 補齊 `strategies/best.py`（`AdaptiveOptimalStrategy`）。
- [ ] 可考慮加入模擬結果的圖表化統計（不同走法的距離／步數比較）。

---

## 📜 授權

本專案目前未於 repository 指定授權條款（License）。如需開放他人使用，建議補上一份 `LICENSE` 檔（例如 MIT）。

---

> 由 kevinhuang09 開發 · Rice Field Sim 🌾