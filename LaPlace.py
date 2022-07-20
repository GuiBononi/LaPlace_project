import time


def input_int(prompt):
    try:
        return int(input(prompt))
    except ValueError:
        print("Please enter an integer.")
        return input_int(prompt)


def minor(lst, i, j):
    return [
        [num for pos, num in enumerate(row) if pos != j]
        for n, row in enumerate(lst) if n != i
    ]


def cofactor(lst, i, j):
    return (-1) ** (i + j) * determinant(minor(lst, i, j))


def determinant(lst):
    if len(lst) == 1:
        return lst[0][0]

    return sum(entry * cofactor(lst, 0, pos) for pos, entry in enumerate(lst[0]))


def third_order(lst):

    right_side = lst[0] * lst[4] * lst[8] +\
                 lst[3] * lst[7] * lst[2] +\
                 lst[6] * lst[1] * lst[5]

    left_side = -1 * lst[2] * lst[4] * lst[6] +\
                -1 * lst[5] * lst[7] * lst[0] +\
                -1 * lst[8] * lst[1] * lst[3]

    return right_side + left_side


def fourth_order(lst):

    if len(lst) == 16:
        fourth_o_m = list(lst)

        # cofactors
        results = dict()

        for i, el in enumerate(fourth_o_m[:4]):

            del (fourth_o_m[i::4])
            a_set = set(fourth_o_m)
            fourth_o_m = list(lst)

            del (fourth_o_m[:4])
            b_set = set(fourth_o_m)
            fourth_o_m = list(lst)

            results[el] = -1 ** (i + 2) * third_order(list(a_set.intersection(b_set)))

        # determinant
        det = 0
        for key, value in results.items():
            det += key * value

        return det

    else:
        raise ValueError


order = input_int('Matrix Order: ')
while order == 0:
    print('Enter a number greater than 0')
    order = input_int('Matrix Order: ')

matrix = [list(range(x*order+1, x*order+order+1)) for x in range(order)]

print()
print('Matrix: ')
for line in range(order):
    print(matrix[line], end='\n')

print()
t1 = time.time()
print(f'Determinant: {determinant(matrix)}')
t2 = time.time()

print()
print(f'Time: {t2-t1:.2f} seconds')
