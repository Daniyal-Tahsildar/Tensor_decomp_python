import numpy as np

# QR factorization
def QR_Factor(file_name):
    with open(file_name, 'r') as file:
        A = []
        
        for line in file:
            values = list(map(float, line.split()))
            A.append(values)
        A = np.array(A)
        print (f"input Tensor:\n {A}")

        def mat_round(M):
            for i in range(len(M)):
                for j in range(len(M[i])):
                    M[i][j] = round(M[i][j], 5)

        def getQ(M):
            Q = []
            M = np.transpose(M)

            for i in range(len(M)):
                v = np.copy(M[i])
                for j in range(i):
                    v -= (np.dot(M[i], Q[j]) / np.dot(Q[j], Q[j])) * Q[j]
                Q.append(v)

            Q = np.array(list(map(lambda v: v / sum(v**2)**0.5, Q)))
            Q = Q.transpose()

            return Q

        def getR(M, Q):
            Q_t = np.transpose(Q)
            return np.matmul(Q_t, M)

        Q = getQ(A)
        R = getR(A, Q)

        mat_round(Q)
        mat_round(R)

        print("\nQ:\n", Q)
        print("\nR:\n", R)
        return Q,R

#  write to file
def write_results(Q, R):
    with open("data_out_file.txt", 'w') as file:
        file.write("Q_matrix:\n")
        for row in Q:

            # changing values to check sbd
            row_str = '\t'.join([f'{element:.6f}' for element in (row + 0.1)]) + '\n'
            file.write(row_str)

        file.write("R_matrix:\n")
        for row in R:
            row_str = '\t'.join([f'{element:.6f}' for element in (row)]) + '\n'
            file.write(row_str)



def sbd(file_name, Q, R):
    Q_matrix = []
    R_matrix = []

    with open(file_name, 'r') as file:
        lines = file.readlines()

        Q_flag = False
        R_flag = False
        Q_correct = False
        R_correct = False

        for line in lines:
            if line.strip() == "Q_matrix:":
                Q_flag = True
                R_flag = False
            elif line.strip() == "R_matrix:":
                Q_flag = False
                R_flag = True
            else:
                if Q_flag:
                    Q_matrix.append([float(x) for x in line.strip().split()])
                elif R_flag:
                    R_matrix.append([float(x) for x in line.strip().split()])

    print("\nQ_matrix:\n", Q_matrix)
    print("\nR_matrix:\n", R_matrix)

# checker
    if (len(Q_matrix) != len(Q) or len(R_matrix) != len(R)):
        print("Error: Matrices dimensions do not match.")
        return

    for i in range(len(Q_matrix)):
        if (len(Q_matrix[i]) != len(Q[i])):
            print(f"Error: Row {i+1} dimensions in Q_matrix and Q do not match.")
            return
        for j in range(len(Q_matrix[i])):
            # if Q_matrix[i][j] != Q[i][j]:
        # Error margin of 0.2
            if (not (Q_matrix[i][j] - 0.2 <= Q[i][j] <= Q_matrix[i][j] + 0.2)):
                print(f"Error: Q_matrix and Q differ at row {i+1}, column {j+1}.")
                Q_correct = False
            else:
                Q_correct = True

    for i in range(len(R_matrix)):
        if (len(R_matrix[i]) != len(R)):
            print(f"Error: Row {i+1} dimensions in R_matrix and R do not match.")
            return
        for j in range(len(R_matrix[i])):
            # if R_matrix[i][j] != R[i][j]:
        # Error margin of 0.2
            if (not (R_matrix[i][j] - 0.2 <= R[i][j] <= R_matrix[i][j] + 0.2)):
                print(f"Error: R_matrix and R differ at row {i+1}, column {j+1}.")
                R_correct = False
            else:
                R_correct = True

    if (Q_correct and R_correct):
        print("\nQR Factorization is correct\n")
    else:
        print("\nQR Factorization is incorrect\n")


# main
Q,R = QR_Factor("data_in_file.txt")
write_results(Q,R)
sbd("data_out_file.txt", Q, R)
