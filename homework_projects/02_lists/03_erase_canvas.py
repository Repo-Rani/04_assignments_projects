import tkinter as tk

CANVAS_WIDTH = 400
CANVAS_HEIGHT = 400
CELL_SIZE = 40
ERASER_SIZE = 20

def erase_objects(event):
    x, y = event.x, event.y  # Get mouse position
    for row in range(0, CANVAS_HEIGHT, CELL_SIZE):
        for col in range(0, CANVAS_WIDTH, CELL_SIZE):
            if col <= x <= col + CELL_SIZE and row <= y <= row + CELL_SIZE:
                canvas.create_rectangle(col, row, col + CELL_SIZE, row + CELL_SIZE, fill="white", outline="white")

root = tk.Tk()
root.title("Eraser Tool")

canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="white")
canvas.pack()

# Create grid of blue cells
for row in range(0, CANVAS_HEIGHT, CELL_SIZE):
    for col in range(0, CANVAS_WIDTH, CELL_SIZE):
        canvas.create_rectangle(col, row, col + CELL_SIZE, row + CELL_SIZE, fill="blue", outline="black")

# Bind mouse motion event to eraser function
canvas.bind("<B1-Motion>", erase_objects)

root.mainloop()
