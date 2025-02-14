import numpy as np
from scipy.optimize import minimize

def estimate_contributions(game_scores):
    game_scores = remove_lower_outliers(game_scores)
    def variance_objective(R1, scores):
        R2_scores = scores - R1
        return np.var(R2_scores)
    initial_guess = np.min(game_scores)
    result = minimize(variance_objective, initial_guess, args=(game_scores,), method='Nelder-Mead')
    return result.x[0]

def remove_lower_outliers(data, threshold=3):
    mean = np.mean(data)
    std = np.std(data)
    return [x for x in data if (x - mean) / std >= -threshold]

# Just testing stuff
if __name__ == "__main__":
    s = np.array([10, 224, 237, 229, 372, 152, 228, 170, 223, 266, 204, 262, 297, 324, 274, 233, 323, 350, 248, 249, 283, 214, 243, 234, 213, 325, 420, 254, 263, 263, 265, 400, 378, 405, 411, 362])
    print(estimate_contributions(s))