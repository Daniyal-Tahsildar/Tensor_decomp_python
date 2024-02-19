import numpy as np
import tensorly as tl
from tensorly.decomposition import parafac


with open("data_in_file.txt", 'r') as file:
    data = []

    for line in file:
        values = list(map(float, line.split()))
        data.append(values)
       
    X1 = tl.tensor(data)

    # Specify the tensor and the rank
    X, rank = X1, 3

    print(X)

    # Perform CP decompositon using TensorLy
    factors_tl = parafac(X, rank=rank)

    print(tl.cp_to_tensor(factors_tl))
    
with open("data_out_file.txt", 'w') as file:
    for row in tl.cp_to_tensor(factors_tl):
        row_str = ' '.join(map(str, row)) + '\n'
        file.write(row_str)
