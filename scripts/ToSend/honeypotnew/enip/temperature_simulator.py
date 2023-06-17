import random

# TemperatureSimulator returns stream of values that are between "low" and "high".
# Each next value can differ from previous value by maximally "max_change"
# However the stream mostly oscillates around average temperature (high-low)/2
class TemperatureSimulator:
    def __init__(self, low, high, max_change):
        self.low = low
        self.high = high
        self.max_change = max_change
        self.last = (low + high) / 2

    def get_next(self):
        next_target = random.uniform(self.low, self.high)
        self.last = self.last + (next_target - self.last)/(self.high - self.low) * self.max_change
        return self.last

# Uncomment this to test how TemperatureSimulator behaves for some arguments

#simulator = TemperatureSimulator(-110.0, 150.0, 5.0)
#for i in range(0, 100):
#    print simulator.get_next()