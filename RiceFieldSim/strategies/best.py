import copy
from strategies.base import MovementStrategy
from strategies.spiral_dash import SpiralDashStrategy
from strategies.zigzag import ZigzagStrategy

class AdaptiveOptimalStrategy(MovementStrategy):
    name = "adaptive optimal"

    def __init__(self, grid):
        self.best_strategy_name = None
        self.chosen_strategy = None

    def _evaluate_strategy(self, grid, car):
        strategies_to_list = {
            "Zigzag" : lambda g : ZigzagStrategy(g),
            "Spiral" : lambda g : SpiralDashStrategy(g),
        }

        results = {}

        for name, StrategyClass in strategies_to_list.items():
            sim_grid = copy.deepcopy(grid)
            sim_car = copy.deepcopy(car)

            strat = StrategyClass(sim_grid)

            steps = 0
            max_steps = 5000
            success = False

            # 先拿初始位置算一次終點
            tx, ty = sim_grid.nearest_exit(sim_car.x, sim_car.y)

            while steps < max_steps:
                
                strat.step(sim_grid, sim_car)
                steps += 1

                tx, ty = sim_grid.nearest_exit(sim_car.x, sim_car.y)
                if sim_car.x == tx and sim_car.y == ty:
                    success = True
                    break
            
            results[name] = steps if success else float("inf")
        self.best_strategy_name = min(results, key = results.get)

        if self.best_strategy_name == "Zigzag":
            return ZigzagStrategy(grid)
        else:
            return SpiralDashStrategy(grid)
        
    def step(self, grid, car):
        if self.chosen_strategy is None:
            self.chosen_strategy = self._evaluate_strategy(grid, car)

        return self.chosen_strategy.step(grid, car)