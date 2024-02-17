from Evaluate.Evaluator import Evaluator
class BasicEval(Evaluator):
    def __init__(self):
        self.tired = False

    def evaluate(keys, ideal_max, ideal_min, data):
        i_min = i_max = 0
        for i in range(1, len(keys.columns.values)):
            key = keys.columns.values[i-1]
            if keys[key].iloc[0] == 0:
                continue
            if abs(data[key] - ideal_max[key][0]) < abs(data[key] - ideal_min[key][0]):
                i_max += 1
            else:
                i_min += 1
        if i_max > i_min:
            return True
        else:
            return False
