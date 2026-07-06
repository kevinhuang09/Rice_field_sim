import os
import datetime
import tkinter as tk

from core.grid import Grid
from core.car import Car

class Simulator:
    def __init__(self, root, strategy, grid = None, delay_ms = 100, results_dir = "results"):
        self.root = root
        self.grid = grid or Grid()
        self.car = Car(self.grid, x = 0, y = 0)
        self.strategy = strategy
        self.delay_ms = delay_ms

        self.results_dir = results_dir
        os.makedirs(self.results_dir, exist_ok = True)
        self.step_log = []
        self.step_count = 0
        self.finished = False

        self.root.title(f"Rice Field : {strategy.name}")

        self.distance_label = tk.Label(
            root, text = self._distance_text(),
            font = ("Arial", 12, "bold"), fg = "#333333", pady = 5,
        )
        self.distance_label.pack()

        # draw 
        self.canvas = tk.Canvas(root, width = self.grid.canvas_width,
                                 height = self.grid.canvas_height, bg = "white")
        self.canvas.pack()

        self._draw_grid()
        self._draw_exit()
        self.car_rect = self._draw_car()


        # self.root.after(self.delay_ms, self._tick)

    def run(self):
        self.root.after(self.delay_ms, self._tick)

    def _distance_text(self):
        return (f"走法：{self.strategy.name}  |  "
                f"總移動距離：{self.car.total_distance} 格 "
                f"(每次移動 {self.grid.car_size} 格)")
    

    def _draw_grid(self):
        g = self.grid

        for i in range(g.grid_width + 1):
            pos_x = g.offset + (i * g.cell_pixel)
            self.canvas.create_line(pos_x, g.offset, pos_x, g.canvas_height - g.offset, fill="#e0e0e0")

        for j in range(g.grid_height + 1):
            pos_y = g.offset + (j * g.cell_pixel)
            self.canvas.create_line(g.offset, pos_y, g.canvas_width - g.offset, pos_y, fill="#e0e0e0")
   
    def _draw_exit(self):
        g = self.grid
        for ex, ey in g.exits:
            x1, y1, x2, y2 = g.to_canvas_coords(ex, ey)
            
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="#ccffcc", outline="#00aa00")
            
            text_x = (x1 + x2) / 2
            text_y = (y1 + y2) / 2
            self.canvas.create_text(text_x, text_y, text="出口",
                                    font=("Arial", 10, "bold"), fill="#006600")
            
    def _draw_car(self):
        x1, y1, x2, y2 = self.grid.to_canvas_coords(self.car.x, self.car.y)
        return self.canvas.create_rectangle(x1, y1, x2, y2, fill="#1e90ff", outline="#00008b")

    def _tick(self):
        if self.finished: return

        still_running = self.strategy.step(self.grid, self.car)
        self.step_count += 1

        line = (f"step {self.step_count:>4} | 座標 ({self.car.x:>2}, {self.car.y:>2}) "
                f"| 累計距離 {self.car.total_distance} 格")
        self.step_log.append(line)
        print(line)

        # update screen
        self.distance_label.config(text = self._distance_text())
        x1, y1, _, _ = self.grid.to_canvas_coords(self.car.x, self.car.y)
        self.canvas.moveto(self.car_rect, x1, y1)

        if not still_running:
            self._finish()
            return 
        
        self.root.after(self.delay_ms, self._tick)

    # @property
    def _finish(self):
        self.finished = True
        self.strategy.on_finish(self.grid, self.car)
        self._write_results()

    # @property
    def _write_results(self):
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = self.strategy.name.replace(" ", "_").replace("+", "plus")

        # 1. step log
        log_path = os.path.join(self.results_dir, f"{ts}_{safe_name}_log.txt")
        with open(log_path, "w", encoding = "utf-8") as f:
            f.write(f"走法：{self.strategy.name}\n")
            f.write(f"時間：{ts}\n")
            f.write("=" * 40 + "\n")
            f.write("\n".join(self.step_log))
            f.write("\n")

        # 2. final summary
        
        reached = (self.car.x, self.car.y) in self.grid.exits

        summary_path = os.path.join(self.results_dir, f"{ts}_{safe_name}_summary.txt")
        with open(summary_path, "w", encoding = "utf-8") as f:
            f.write("==== 模擬結果摘要 ====\n")
            f.write(f"走法名稱   : {self.strategy.name}\n")
            f.write(f"總步數     : {self.step_count}\n")
            f.write(f"總移動距離 : {self.car.total_distance} 格\n")
            f.write(f"最終座標   : ({self.car.x}, {self.car.y})\n")
            f.write(f"是否抵達出口: {'是' if reached else '否'}\n")

        print(f"\nThe result write at : {log_path}\n - {summary_path}")            