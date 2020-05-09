def edit_distance(seq1, seq2, ins_cost, del_cost, chan_cost, swap_cost):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros ((size_x, size_y))
    for x in range(size_x):
        matrix [x, 0] = x
    for y in range(size_y):
        matrix [0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            ch_c = 0 if seq1[x-1] == seq2[y-1] else chan_cost
            if x < 2 or y < 2 or  seq1[x:x-2:-1] != seq2[y-2:y]:
                matrix [x,y] = min(
                    matrix[x-1,y] + del_cost,
                    matrix[x-1,y-1] + ch_c,
                    matrix[x,y-1] + ins_cost
                )
            else:
                matrix [x,y] = min(
                    matrix[x-1,y] + del_cost,
                    matrix[x-1,y-1] + ch_c,
                    matrix[x,y-1] + ins_cost,
                    matrix[x-2,y-2] + swap_cost
                )
    return (matrix[size_x - 1, size_y - 1])