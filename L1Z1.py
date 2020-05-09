import numpy as np
import re
from itertools import combinations

def levenshtein(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros ((size_x, size_y))
    for x in range(size_x):
        matrix [x, 0] = x
    for y in range(size_y):
        matrix [0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x-1] == seq2[y-1]:
                matrix [x,y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1],
                    matrix[x, y-1] + 1
                )
            else:
                matrix [x,y] = min(
                    matrix[x-1,y] + 1,
                    matrix[x-1,y-1] + 1,
                    matrix[x,y-1] + 1
                )
    return (matrix[size_x - 1, size_y - 1])

def main():
    pattern = re.compile(r"''[a-zA-Z0-9_ ]+''")
    pattern_line = re.compile(r"^([^.]+)")
    with open("Dane/poczatki_wikipediowe.txt", "r") as infile:
        with open("Dane/output.txt", "w") as outfile:
            for i, line in enumerate(infile):
                if i % 3 == 1:
                    lines = pattern_line.findall(line)
                    if len(lines) > 0:
                        line = lines[0]
                    words = pattern.findall(line)
                    if len(words) == 0:
                        continue
                    result = [words[0][2:-2]]
                    for w in words:
                        if levenshtein(words[0],w) > 6 and len(w) > 5:
                            result.append(w[2:-2])
                    if len(result) > 1:
                        outfile.write(" # ".join(result) + "\n")
                   

if __name__ == "__main__":
    main()
