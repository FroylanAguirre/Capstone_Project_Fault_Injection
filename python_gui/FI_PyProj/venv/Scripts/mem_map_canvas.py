from tkinter import Canvas
from HeapVariables import HeapVariables
from tkinter import Checkbutton

CANVAS_HEIGHT = 600
MAIN_REC_WIDTH = 150
MAIN_REC_HEIGHT = 300
MAIN_REC_X = 75
MAIN_REC_Y = 25
TEXT_HEIGHT = 20
VAR_NAME_WIDTH = 110
VAR_NAME_CHAR_MAX = 15 # at font size 10, Consolas
SIZE_LINES_X_OFFSET = -10
SIZE_LINES_TICK_WIDTH = 10
SIZE_LINES_TEXT_OFFSET = -25
SELECTION_COLOR = "blue"
DISTANCE_BTW_CHECKBOXES = 60
FIRST_CHECKBOX_X = MAIN_REC_X + MAIN_REC_WIDTH + 30
HALF_DIAGONAL_LENGTH = 8


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

            # draw check boxes
            self.create_rectangle(FIRST_CHECKBOX_X - HALF_DIAGONAL_LENGTH,
                                  y_pos - (pixel_var_size/2) - HALF_DIAGONAL_LENGTH,
                                  FIRST_CHECKBOX_X + HALF_DIAGONAL_LENGTH,
                                  y_pos - (pixel_var_size/2) + HALF_DIAGONAL_LENGTH,
                                  fill='',
                                  activefill="gray",
                                  outline='black',
                                  tag=glbl.name + "_sample")
            self.create_rectangle(FIRST_CHECKBOX_X + DISTANCE_BTW_CHECKBOXES - HALF_DIAGONAL_LENGTH,
                                  y_pos - (pixel_var_size/2) - HALF_DIAGONAL_LENGTH,
                                  FIRST_CHECKBOX_X + DISTANCE_BTW_CHECKBOXES + HALF_DIAGONAL_LENGTH,
                                  y_pos - (pixel_var_size/2) + HALF_DIAGONAL_LENGTH,
                                  fill='',
                                  activefill="gray",
                                  outline='black',
                                  tag=glbl.name + "_critical")
            # bind click event to sampling checkbox
            self.tag_bind(glbl.name + "_sample",
                          "<ButtonPress-1>",
                          (lambda ev: self.sample_click(ev)))

            # bind click event to critical checkbox
            self.tag_bind(glbl.name + "_critical",
                          "<ButtonPress-1>",
                          (lambda ev: self.critical_click(ev)))

        self.create_text(FIRST_CHECKBOX_X,
                         y_pos,
                         font=("Consolas", 9),
                         text="Sample",
                         anchor="n")
        self.create_text(FIRST_CHECKBOX_X + DISTANCE_BTW_CHECKBOXES,
                         y_pos,
                         font=("Consolas", 9),
                         text="Crit.",
                         anchor="n")

        self.create_text(MAIN_REC_X + SIZE_LINES_TEXT_OFFSET,
                         y_pos,
                         font=("Consolas", 9),
                         text="size\n(bytes)",
                         anchor="n")

        self.create_line(FIRST_CHECKBOX_X + DISTANCE_BTW_CHECKBOXES/2,
                         MAIN_REC_Y,
                         FIRST_CHECKBOX_X + DISTANCE_BTW_CHECKBOXES/2,
                         y_pos,
                         width=5,
                         capstyle="round")

    def sample_click(self, event):
        '''
        Called when a sample checkbox is clicked on.
        '''
        widget_id = event.widget.find_closest(event.x, event.y)
        tag_str = self.itemcget(widget_id, "tag")  # returns (widget tag) and "current" separated by a space
        tag_str = tag_str.split()[0]
        print("sample on: " + tag_str)

        fill_color = self.itemcget(tag_str, "fill")
        if fill_color == SELECTION_COLOR:
            self.itemconfig(tag_str, fill="")
            tag_str = tag_str.replace("_sample", "_critical")
            self.itemconfig(tag_str, fill="")
        else:
            self.itemconfig(tag_str, fill=SELECTION_COLOR)

    def critical_click(self, event):
        '''
        Called when a sample checkbox is clicked on.
        '''
        widget_id = event.widget.find_closest(event.x, event.y)
        tag_str = self.itemcget(widget_id, "tag")  # returns (widget tag) and "current" separated by a space
        tag_str = tag_str.split()[0]
        print("critical on: " + tag_str)
        fill_color = self.itemcget(tag_str, "fill")
        if fill_color == SELECTION_COLOR:
            self.itemconfig(tag_str, fill="")
        else:
            self.itemconfig(tag_str, fill=SELECTION_COLOR)

        # also select sample since critical is ALWAYS sampled, but not the other way around
        tag_str = tag_str.replace("_critical", "_sample")
        self.itemconfig(tag_str, fill=SELECTION_COLOR)



class SingleGlobalVar:
    '''
    Describes a global variable's possible sampling settings.
    A sample true means that if an error is found, it counts as latent.
    A critical true means that if an error is found, it counts as a data error.
    '''

    def __init__(self, name):
        self.name = name
        self.sample = False
        self.critical = False

    def set_critical(self):
        self.critical = True
        self.sample = True

    def set_sample(self):
        self.critical = False
        self.sample = True

    def clear_all(self):
        self.critical = False
        self.sample = False

    def __eq__(self, other):
        return self.name == other.name