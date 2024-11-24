import numpy as np
import json

matrix = np.load('first_task.npy')

main_diagonal = np.diag(matrix)

side_diagonal = np.fliplr(matrix).diagonal()

result = {
    "sum": float(np.sum(matrix)),
    "avr": float(np.mean(matrix)),
    "sumMD": float(np.sum(main_diagonal)),
    "avrMD": float(np.mean(main_diagonal)),
    "sumSD": float(np.sum(side_diagonal)),
    "avrSD": float(np.mean(side_diagonal)),
    "max": float(np.max(matrix)),
    "min": float(np.min(matrix)),
}

with open('result.json', 'w') as f:
    json.dump(result, f, indent=4)

def normalize_matrix(m):
    matrix_min = m.min()
    matrix_max = m.max()

    if matrix_min == matrix_max:
        return np.zeros_like(m)

    return (m - matrix_min) / (matrix_max - matrix_min)

np.save('normalized_matrix.npy', normalize_matrix(matrix))

