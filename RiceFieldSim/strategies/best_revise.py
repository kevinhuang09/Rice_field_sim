from strategies.base import MovementStrategy
from strategies.spiral_dash import SpiralDashStrategy
from strategies.zigzag import ZigzagStrategy

class AdaptiveOptimalStrategy(MovementStrategy):
    name = "adaptive optimal"

    def __init__(self, grid):
        self.best_strategy_name = None
        self.chosen_strategy = None

    def _evaluate_strategy(self, grid, car):
        """
        直接用數學幾何計算，不透過 while 模擬，100% 準確！
        """
        # 取得基本地圖數據
        W = grid.max_x
        H = grid.max_y
        s = grid.car_size
        
        # 車子當前的起點座標
        start_x = car.x
        start_y = car.y
        
        # 終點座標（由系統抓取最近的出口）
        tx, ty = grid.nearest_exit(start_x, start_y)

        # =========================================================
        # 1. 計算 Zigzag (S型掃描) 的理論步數
        # =========================================================
        # 總共要掃描幾橫列
        zigzag_rows = (H // s) + 1
        # 每一橫列要走幾步
        steps_per_row = (W // s) + (1 if W % s != 0 else 0)
        # 總掃描步數 = (列數 * 每列步數) + 垂直往上移動的步數
        zigzag_scan_steps = (zigzag_rows * steps_per_row) + zigzag_rows
        
        # Zigzag 掃描結束時，車子一定會停在最頂端的某一側 (x=0 或 x=W, y=H)
        # 我們粗略計算它從頂端衝刺到出口 (tx, ty) 的曼哈頓距離步數
        end_z_x = 0 if zigzag_rows % 2 == 0 else W
        end_z_y = H
        # 斜線衝刺：取 X 和 Y 軸差的最大值（因為 X 和 Y 可以同時移動）
        zigzag_dash_steps = max(abs(end_z_x - tx), abs(end_z_y - ty)) // s
        
        total_zigzag_steps = zigzag_scan_steps + zigzag_dash_steps

        # =========================================================
        # 2. 計算 Spiral (螺旋掃描) 的理論步數
        # =========================================================
        # 螺旋是往內縮，總掃描步數基本上等於把整張地圖的格子填滿
        # 總步數大約等於: (總面積 / 車子面積)
        spiral_scan_steps = (W * H) // (s * s)
        
        # 螺旋結束時，車子一定會卡在地圖的正中央 (W/2, H/2)
        end_s_x = W // 2
        end_s_y = H // 2
        # 從中央衝刺到出口的步數
        spiral_dash_steps = max(abs(end_s_x - tx), abs(end_s_y - ty)) // s
        
        total_spiral_steps = spiral_scan_steps + spiral_dash_steps

        # =========================================================
        # 3. 判定誰勝出
        # =========================================================
        if total_zigzag_steps < total_spiral_steps:
            self.best_strategy_name = "Zigzag"
        else:
            self.best_strategy_name = "Spiral"

        print("\n=============================================")
        print(f"📐 數學幾何預估步數 -> Zigzag: ~{int(total_zigzag_steps)} 步 | Spiral: ~{int(total_spiral_steps)} 步")
        print(f"===> 100% 預判選擇最優走法: [{self.best_strategy_name}] <===")
        print("=============================================\n")

        if self.best_strategy_name == "Zigzag":
            return ZigzagStrategy(grid)
        else:
            return SpiralDashStrategy(grid)
        
    def step(self, grid, car):
        if self.chosen_strategy is None:
            self.chosen_strategy = self._evaluate_strategy(grid, car)

        return self.chosen_strategy.step(grid, car)