import unicodedata
from collections import defaultdict as dd
import numpy as np
from sklearn.cluster import KMeans

cat = dd(lambda:[])

def to_binary(n, m):
    res = [0] * m
    for i in range(m):
        res[i] = n % 2
        n //=2
    return res

def characters_to_array(chars):
    res = [to_binary(ord(c), 32) for c in chars]
    return np.array(res)

with open("Dane/znaki_wikipedii.txt", "r") as infile:
    for txt in infile:
        for r in txt:
            cat[unicodedata.category(r)].append(r)

letters = cat["Lu"] + cat["Ll"] + cat["Lt"] + cat["Lm"] + cat["Lo"]
X = characters_to_array(letters)
n = 8
clustering = KMeans(n_clusters = n).fit(X)
clusters = clustering.predict(X)
letters = np.array(letters)

with open("Dane/output2.txt","w") as outfile:
    for i in range(n):
        outfile.write(f"Cluster {i}\n")
        for j, letter in enumerate(letters):
            if clusters[j] == i:
                outfile.write(f"{letter} ")
        outfile.write(f"\n")