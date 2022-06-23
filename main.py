import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, Button, CheckButtons
from thomas_algorithm import get_x_set, calculate_exact, classic_scheme, characteristics_scheme

_Cu = 1
_Pe = 3

# appearance
WINDOW_WIDTH = 8
WINDOW_HEIGHT = 6
EXACT_SOLUTION_COLOR = 'black'

if __name__ == '__main__':
    fig, ax = plt.subplots()
    plt.subplots_adjust(left=0.10, bottom=0.25, right=0.95, top=0.95)
    ax.figure.set_size_inches(WINDOW_WIDTH, WINDOW_HEIGHT)

    ax_cu = plt.axes([0.5, 0.15, 0.1, 0.03])
    ax_pe = plt.axes([0.5, 0.1, 0.1, 0.03])
    ax_draw = plt.axes([0.7, 0.10, 0.15, 0.03])
    ax_check = plt.axes([0.15, 0.10, 0.2, 0.08])

    cu_input = TextBox(ax_cu, 'Cu: ', initial=str(_Cu))
    pe_input = TextBox(ax_pe, 'Pe: ', initial=str(_Pe))
    draw_button = Button(ax_draw, 'Draw')
    check_classic = CheckButtons(ax_check, 'With classic scheme', [])

    # setting the x - coordinates
    x = get_x_set(_Pe)

    # setting the corresponding y - coordinates
    y_exact = calculate_exact(_Pe)
    y_classic = classic_scheme(_Cu, _Pe)
    y_characteristics = characteristics_scheme(_Cu, _Pe)

    # plotting the points
    l1, = ax.plot(x, y_exact, label='exact solution', color=EXACT_SOLUTION_COLOR)
    l2, = ax.plot(x, y_classic, label='classic scheme')
    l3, = ax.plot(x, y_characteristics, label='characteristics scheme')
    ax.legend(handles=[l1, l2, l3])

    lines = [l2]
    labels = [l2.get_label() for line in lines]
    visibility = [line.get_visible() for line in lines]
    check_classic = CheckButtons(ax_check, labels, visibility)

    def check_func(label):
        index = labels.index(label)
        lines[index].set_visible(not lines[index].get_visible())
        plt.draw()

    def redraw(val):

        # updating Cu and Pe
        global _Cu, _Pe
        _Cu = int(cu_input.text)
        _Pe = int(pe_input.text)

        # setting the x and y coordinates
        global x, y_exact, y_classic, y_characteristics
        x = get_x_set(_Pe)
        y_exact = calculate_exact(_Pe)
        y_classic = classic_scheme(_Cu, _Pe)
        y_characteristics = characteristics_scheme(_Cu, _Pe)

        global l1, l2, l3
        l1.set_xdata(x)
        l1.set_ydata(y_exact)
        l2.set_xdata(x)
        l2.set_ydata(y_classic)
        l3.set_xdata(x)
        l3.set_ydata(y_characteristics)

        fig.canvas.draw()
        fig.canvas.flush_events()

    check_classic.on_clicked(check_func)
    draw_button.on_clicked(redraw)

    plt.show()
