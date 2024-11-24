import numpy as np
import os

matrix = np.load('second_task.npy')

indexes = np.argwhere(matrix > 576)
x, y = indexes[:, 0], indexes[:, 1]
z = matrix[matrix > 576]

np.savez('result_arrays.npz', x=x, y=y, z=z)
np.savez_compressed('result_arrays_compressed.npz', x=x, y=y, z=z)

print(f"Размер файла result_arrays: {os.path.getsize('result_arrays.npz')} байт")
print(f"Размер файла result_arrays_compressed: {os.path.getsize('result_arrays_compressed.npz')} байт")


