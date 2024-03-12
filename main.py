from tkinter import Tk, Canvas, Button, Frame, Label, Entry


class Coordinates:
    x = None
    y = None

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class App(Tk):
    canvas = None
    pen_enabled = False
    eraser_enabled = False
    rectangle_enabled = False
    text_enabled = False
    start_position = Coordinates()
    active_shape = None
    active_entry = None
    active_label = None

    def __init__(self):
        super().__init__("DrawingBoard")
        self.wm_title("Drawing Board")
        self.add_buttons()
        self.canvas = Canvas(self, bg="white", width=800, height=600)
        self.canvas.bind("<ButtonPress-1>", self.set_start_position)
        self.canvas.bind("<ButtonRelease-1>", self.set_end_position)
        self.canvas.bind("<B1-Motion>", self.run_tool_operation)
        self.canvas.grid(row=1, column=4, padx=8, pady=8)

    def run_tool_operation(self, event):
        self.draw_with_pen(event)
        self.erase_area(event)
        self.draw_rectangle(event)

    def disable_all_tools(self):
        self.pen_enabled = False
        self.eraser_enabled = False
        self.rectangle_enabled = False
        self.text_enabled = False

    def enable_pen(self):
        if self.pen_enabled:
            self.pen_enabled = False
        else:
            self.disable_all_tools()
            self.pen_enabled = True

    def enable_eraser(self):
        if self.eraser_enabled:
            self.eraser_enabled = False
        else:
            self.disable_all_tools()
            self.eraser_enabled = True

    def enable_rectangle(self):
        if self.rectangle_enabled:
            self.rectangle_enabled = False
        else:
            self.disable_all_tools()
            self.rectangle_enabled = True

    def enable_text(self):
        if self.text_enabled:
            self.text_enabled = False
        else:
            self.disable_all_tools()
            self.text_enabled = True

    def add_buttons(self):
        tool_frame = Frame(self, width=800, height=200)
        tool_frame.grid(row=0, column=4, padx=8, pady=8)
        Button(tool_frame, text="Pen", command=self.enable_pen).grid(row=0, column=0, padx=4, pady=4)
        Button(tool_frame, text="Eraser", command=self.enable_eraser).grid(row=0, column=1, padx=4, pady=4)
        Button(tool_frame, text="Rectangle", command=self.enable_rectangle).grid(row=0, column=2, padx=4, pady=4)
        Button(tool_frame, text="Text", command=self.enable_text).grid(row=0, column=3, padx=4, pady=4)

    def draw_with_pen(self, event):
        if self.pen_enabled:
            self.canvas.create_line(
                (self.start_position.x, self.start_position.y, event.x, event.y),
                fill="black",
                width=2
            )
            self.start_position = event

    def erase_area(self, event):
        if self.eraser_enabled:
            closest_object_id = self.canvas.find_overlapping(event.x-1, event.y-1, event.x+1, event.y+1)
            if len(closest_object_id) > 0 and closest_object_id is not None:
                self.canvas.delete(closest_object_id[0])

    def draw_rectangle(self, event):
        if self.rectangle_enabled:
            if self.active_shape is not None:
                self.canvas.delete(self.active_shape)
            self.active_shape = self.canvas.create_rectangle(self.start_position.x, self.start_position.y, event.x,
                                                             event.y)

    def add_text_box(self, _):
        if self.start_position is not None and self.text_enabled:
            width = 50
            height = 50
            entry_frame = Frame(self.canvas, width=width, height=height)
            entry_frame.grid_configure(column=2, columnspan=width, row=1, rowspan=height)
            entry = Entry(entry_frame, width=width)
            entry.bind("<Return>", self.replace_with_label)
            self.active_entry = entry
            entry.grid(row=0, column=0)
            confirm_button = Button(entry_frame, text=">>", command=self.replace_with_label_key)
            confirm_button.grid(row=0, column=1)
            entry_frame.place(x=self.start_position.x - width/2, y=self.start_position.y - height/2)

    def replace_with_label(self, _):
        value = self.active_entry.get()
        if self.start_position is not None:
            value_label = Label(self.canvas, text=value)
            value_label.place(
                x=self.start_position.x,
                y=self.start_position.y)
            self.start_position = None
            if isinstance(self.active_entry.master, Frame):
                self.active_entry.master.destroy()
            self.active_entry = None

    def replace_with_label_key(self):
        value = self.active_entry.get()
        if self.start_position is not None:
            value_label = Label(self.canvas, text=value)
            value_label.place(
                x=self.start_position.x,
                y=self.start_position.y)
            self.start_position = None
            if isinstance(self.active_entry.master, Frame):
                self.active_entry.master.destroy()
            self.active_entry = None

    def set_start_position(self, event):
        self.start_position = Coordinates(event.x, event.y)
        if self.text_enabled:
            self.add_text_box(event)

    def set_end_position(self, event):
        self.draw_rectangle(event)
        self.active_shape = None


app = App()
app.mainloop()
