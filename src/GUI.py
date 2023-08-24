from game2dboard import Board

BLOCK_SIZE = 64

field = None
path = None
cur_node_index = 0


def step():
    pass


def visualize():
    num_rows, num_cols = 3, 12
    field = Board(num_rows, num_cols)

    field.cell_size = BLOCK_SIZE
    field.title = "Super Mario!"
    field.cursor = None  # Hide the cursor
    field.margin = 40
    field.grid_color = "AntiqueWhite"
    field.background_image = "background"
    field.margin_color = "AntiqueWhite"
    field.cell_color = "Peru"
    # field.start_timer(700)  # 300 ms

    field[0][0] = "luigi"
    field.show()


visualize()
