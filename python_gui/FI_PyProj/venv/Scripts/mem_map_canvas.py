from tkinter import Canvas
from HeapVariables import HeapVariables
from tkinter import Checkbutton

CANVAS_HEIGHT = 600
MAIN_REC_WIDTH = 150
MAIN_REC_HEIGHT = 300
MAIN_REC_X = 50
MAIN_REC_Y = 25
TEXT_HEIGHT = 20
VAR_NAME_WIDTH = 110
VAR_NAME_CHAR_MAX = 15 # at font size 10, Consolas
SIZE_LINES_X_OFFSET = -10
SIZE_LINES_TICK_WIDTH = 10
SIZE_LINES_TEXT_OFFSET = -25
SELECTION_COLOR = "blue"

class MemoryMapCanvas(Canvas):
    '''
    Canvas subclass that draws out a memory map using canvas widgets (lines,
    rectangles, circles, etc)
    Part of a collection of widgets used to create the memory map Frame subclass.
    '''

    def __init__(self, master):
        Canvas.__init__(self, master,
                        bg="white",
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

        self.selected_tags = []

        self.pack(fill="none")

    def update_memory_table(self, heap_var_list):

        self.delete("all") # clear previous memory map graphics

        # calculate the difference between the highest and lowest addresses
        var_range_size = heap_var_list.heap_var_l[-1].addr + heap_var_list.heap_var_l[-1].size
        var_range_size -= heap_var_list.heap_var_l[0].addr - 1
        total_size_px = 0

        # calculate size of memory map on canvas
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

        # draw variables in memory map with relative sizes
        for glbl in heap_var_list.heap_var_l:
            pixel_var_size = (glbl.size / var_range_size) * MAIN_REC_HEIGHT

            if pixel_var_size <= TEXT_HEIGHT:
                pixel_var_size = TEXT_HEIGHT

            # check and account for long varialble names
            if (len(glbl.name) > VAR_NAME_CHAR_MAX):
                display_name = glbl.name[0:11] + "..."
            else:
                display_name = glbl.name

            self.create_text(x_pos,
                             y_pos + (pixel_var_size / 2),
                             text=display_name,
                             fill="#000000",
                             font=("Consolas", 10),
                             activefill="white",
                             width=VAR_NAME_WIDTH,
                             tag=glbl.name)

            self.create_text(MAIN_REC_X + SIZE_LINES_TEXT_OFFSET,
                             y_pos + (pixel_var_size / 2),
                             text=str(glbl.size),
                             fill="#000000",
                             font=("Consolas", 10),
                             activefill="white",
                             width=VAR_NAME_WIDTH,
                             anchor="e",
                             tag=glbl.name + "_line_size")

            # binds clicking on text with specific action
            self.tag_bind(glbl.name,
                          "<ButtonPress-1>",
                          (lambda ev: self.selection_click(ev)))

            y_pos += pixel_var_size

            # draw line between variables
            self.create_line(MAIN_REC_X,
                             y_pos,
                             MAIN_REC_X + MAIN_REC_WIDTH,
                             y_pos,
                             dash=(2,10))

            # draw size lines
            self.create_line(MAIN_REC_X + SIZE_LINES_X_OFFSET,
                             y_pos - pixel_var_size + 1,
                             MAIN_REC_X + SIZE_LINES_X_OFFSET,
                             y_pos - 1,
                             tag=glbl.name + "_line_size")
            self.create_line(MAIN_REC_X + SIZE_LINES_X_OFFSET + (SIZE_LINES_TICK_WIDTH/2),
                             y_pos - pixel_var_size + 1,
                             MAIN_REC_X + SIZE_LINES_X_OFFSET - (SIZE_LINES_TICK_WIDTH/2),
                             y_pos - pixel_var_size + 1,
                             tag=glbl.name + "_line_size")
            self.create_line(MAIN_REC_X + SIZE_LINES_X_OFFSET + (SIZE_LINES_TICK_WIDTH / 2),
                             y_pos - 1,
                             MAIN_REC_X + SIZE_LINES_X_OFFSET - (SIZE_LINES_TICK_WIDTH / 2),
                             y_pos - 1,
                             tag=glbl.name + "_line_size")


    def selection_click(self, event):
        widget_id = event.widget.find_closest(event.x, event.y)
        tag_str = self.itemcget(widget_id, "tag")  # returns (widget tag) and "current" separated by a space
        tag_str = tag_str.split()[0]

        line_color = self.itemcget(tag_str + "_line_size", "fill")
        if line_color == SELECTION_COLOR:
            self.itemconfig(tag_str + "_line_size", fill="black")
        else:
            self.itemconfig(tag_str + "_line_size", fill=SELECTION_COLOR)

        self.update_selected_tags(tag_str)

    def update_selected_tags(self, widget_tag):
        line_color = self.itemcget(widget_tag + "_line_size", "fill")  # returns (widget tag) and "current" separated by a space
        if line_color == SELECTION_COLOR:
            self.selected_tags.append(widget_tag)
        else:
            self.selected_tags.remove(widget_tag)
