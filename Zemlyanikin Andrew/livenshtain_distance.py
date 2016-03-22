def levenshtein_dist(word_1, word_2):
    m = len(word_1)
    n = len(word_2)
    distance_matrix = []
    for i in range(m+1):
        distance_matrix.append([i])
    del distance_matrix[0][0]
    for j in range(n+1):
        distance_matrix[0].append(j)
    for j in range(1, n+1):
        for i in range(1, m+1):
            if word_1[i-1] == word_2[j-1]:
                distance_matrix[i].insert(j, distance_matrix[i-1][j-1])
            else:
                minimum = min(distance_matrix[i-1][j]+1, distance_matrix[i][j-1]+1, distance_matrix[i-1][j-1]+2)
                distance_matrix[i].insert(j, minimum)
    levens_distance = distance_matrix[-1][-1]


    return print('distance_levenshtein:', levens_distance)

if __name__ == "__main__":
    levenshtein_dist("QW", "QWE")
