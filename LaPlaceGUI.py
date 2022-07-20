import PySimpleGUI as sg
from time import time

sg.theme('DarkAmber')


def input_int(prompt):
    try:
        return int(input(prompt))
    except ValueError:
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
        for k, v in results.items():
            det += k * v

        return det

    else:
        raise ValueError


def first_page():

    layout = [
        [sg.Titlebar("LaPlace", text_color="#FFFFFF", background_color="#444444", )],
        [sg.Text('THIS PROGRAM CALCULATES THE DETERMINANT OF A MATRIX OF ANY ORDER.', font="arial", pad=20)],
        [sg.Text('note: orders upon 20 may be really slow to calculate.', text_color='#B9B9B9')],
        [sg.Stretch(), sg.Stretch(), sg.Text('by bononi', text_color="grey")],
        [sg.Text("Order"), sg.InputText(size=6, border_width=2, key='-OR-'), sg.Text(text="input only integers", text_color="grey"), sg.Stretch(), sg.Text('July, 2022', text_color="grey")],
        [sg.Text()],
        [sg.Button('submit', border_width=3)]
    ]
    return sg.Window('LaPlace', layout=layout, finalize=True, border_depth=3)


def second_page(ord, siz_sqr=(4, 4)):

    layout2 = [
        [sg.Titlebar("LaPlace", text_color="#FFFFFF", background_color="#444444")],
        [sg.Text('Input the elements in their proper square', font='arial')],
        [sg.Text('Order', text_color="grey"), sg.Text(text=ord, text_color="grey", key='-OR2-')],
        [sg.Text()],
        [[sg.InputText(tooltip=f'a {r+1},{c+1}', text_color="#C8C8C8", border_width=2, size=siz_sqr, key=f'-{r},{c}-') for c in range(ord)] for r in range(ord)],
        [sg.Text()],
        [sg.Button('back', border_width=3), sg.Button('clear', border_width=3), sg.Stretch(), sg.Button('Enter', border_width=3)],
        [sg.Text()],
        [sg.Text("", key="-RESULTS-"), sg.Stretch(), sg.Text("", text_color="grey", key='-TIME-')]
    ]
    return sg.Window('LaPlace', layout=layout2, finalize=True, border_depth=3)


window1, window2 = first_page(), None

while True:
    shown_screen, event, key = sg.read_all_windows()

    if shown_screen == window1 and event == sg.WIN_CLOSED:
        break

    if shown_screen == window1 and event == 'submit':
        try:
            order = int(key['-OR-'])

            if order > 15:
                big_size = (2, 2)
                window2 = second_page(order, siz_sqr=big_size)
            else:
                window2 = second_page(order)

            window1.hide()
        except ValueError:
            pass

    if shown_screen == window2 and event == sg.WIN_CLOSED:
        break

    if shown_screen == window2 and event == 'back':
        window2.close()
        window1.un_hide()

    if shown_screen == window2 and event == 'Enter':

        try:
            matrix = [
                [int(key[f'-{r},{c}-']) for c in range(order)]for r in range(order)
            ]
            t1 = time()
            window2['-RESULTS-'].update(f'Determinant: {determinant(matrix)}', text_color="#CFA600")
            t2 = time()
            window2['-TIME-'].update(f'Computation time: {t2-t1:.3f} s')

        except ValueError:
            window2['-RESULTS-'].update('Fill all the boxes with integers', text_color='#B9B9B9')

    if shown_screen == window2 and event == 'clear':
        window2.close()
        window2 = second_page(order)
