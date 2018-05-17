from tkinter import Canvas
from HeapVariables import HeapVariables

CANVAS_HEIGHT = 600
MAIN_REC_WIDTH = 150
MAIN_REC_HEIGHT = 300
MAIN_REC_X = 50
MAIN_REC_Y = 25
TEXT_HEIGHT = 20

class MemoryMapCanvas(Canvas):

    def __init__(self, master):
        Canvas.__init__(self, master,
                        bg="blue",
                        height=CANVAS_HEIGHT)

        self.create_rectangle(MAIN_REC_X,
                              MAIN_REC_Y,
                              MAIN_REC_X + MAIN_REC_WIDTH,
                              MAIN_REC_Y + MAIN_REC_HEIGHT,
                              fill="gray")
        self.create_text(MAIN_REC_X + (MAIN_REC_WIDTH/2),
                         MAIN_REC_Y + (TEXT_HEIGHT/2),
                         text="SystemCoreClock",
                         fill="#000000",
                         font=("Consolas", 10))

        self.pack(fill="none")

    def update_memory_table(self, heap_var_list):

        self.delete("all")

        var_range_size = heap_var_list.heap_var_l[-1].addr + heap_var_list.heap_var_l[-1].size
        var_range_size -= heap_var_list.heap_var_l[0].addr - 1
        total_size_px = 0

        for glbl in heap_var_list.heap_var_l:
            var_size_px = (glbl.size / var_range_size) * MAIN_REC_HEIGHT

            if var_size_px <= TEXT_HEIGHT:
                var_size_px = TEXT_HEIGHT
            total_size_px += var_size_px

        self.create_rectangle(MAIN_REC_X,
                              MAIN_REC_Y,
                              MAIN_REC_X + MAIN_REC_WIDTH,
                              MAIN_REC_Y + total_size_px,
                              fill="gray")

        prev_addr = heap_var_list.heap_var_l[0].addr

        x_pos = MAIN_REC_X + (MAIN_REC_WIDTH / 2)
        y_pos =  MAIN_REC_Y

        for glbl in heap_var_list.heap_var_l:
            pixel_var_size = (glbl.size / var_range_size) * MAIN_REC_HEIGHT

            if pixel_var_size <= TEXT_HEIGHT:
                pixel_var_size = TEXT_HEIGHT

            self.create_text(x_pos,
                             y_pos + (pixel_var_size / 2),
                             text=glbl.name,
                             fill="#000000",
                             font=("Consolas", 10),
                             activefill="white",
                             tag=glbl.name)

            self.tag_bind(glbl.name, "<ButtonPress-1>", (lambda ev: self.small(ev)))

            y_pos += pixel_var_size

            self.create_line(MAIN_REC_X,
                             y_pos,
                             MAIN_REC_X + MAIN_REC_WIDTH,
                             y_pos,
                             dash=(2,10))

    def small(self, event):
        widget_id = event.widget.find_closest(event.x, event.y)
        print("hello " + self.itemcget(widget_id, "text"))