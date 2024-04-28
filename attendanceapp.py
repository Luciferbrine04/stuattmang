import tkinter as tk
from tkinter import messagebox


class AttendanceApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Shape Display")
        self.geometry("1024x600")

        self.original_rect_width = 50
        self.original_rect_height = 30
        self.rect_width = int(self.original_rect_width * 1.3)
        self.rect_height = int(self.original_rect_height * 1.3)
        self.padding = 5

        self.canvas_width = 1024
        self.canvas_height = 600

        self.offset_x = (self.canvas_width - (7 * self.rect_width + 6 * self.padding)) // 2
        self.offset_y = (self.canvas_height - (5 * self.rect_height + 4 * self.padding)) // 2

        self.current_column = 0
        self.current_rol = 0
        self.create_canvas()
        self.create_period_labels()
        self.create_row_labels()
        self.create_rectangles()
        self.create_buttons()

    def create_canvas(self):
        self.canvas = tk.Canvas(self, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()

    def create_period_labels(self):
        self.period_labels = ['Period 0', 'Period 1', 'Period 2', 'Period 3', 'Period 4', 'Period 5', 'Period 6']
        for col, period_label in enumerate(self.period_labels):
            x_center = self.offset_x + col * (self.rect_width + self.padding) + self.rect_width // 2
            self.canvas.create_text(x_center, self.offset_y - 20, text=period_label)

    def create_row_labels(self):
        self.row_labels = ['224027', '224004', '224117', '224014', '224111']
        for row, row_label in enumerate(self.row_labels):
            y_center = self.offset_y + row * (self.rect_height + self.padding) + self.rect_height // 2
            self.canvas.create_text(self.offset_x - 50, y_center, text=row_label)

    def create_rectangles(self):
        self.rectangles = []
        self.colors = [['red' for _ in range(7)] for _ in range(5)]  # Initialize all rectangles to red
        for row in range(5):
            row_rectangles = []
            for col in range(7):
                x0 = self.offset_x + col * (self.rect_width + self.padding)
                y0 = self.offset_y + row * (self.rect_height + self.padding)
                x1 = x0 + self.rect_width
                y1 = y0 + self.rect_height
                rectangle_color = self.colors[row][col]
                rectangle = self.canvas.create_rectangle(x0, y0, x1, y1, fill=rectangle_color)

                row_rectangles.append(rectangle)
            self.rectangles.append(row_rectangles)

    def toggle_color(self, row, col):
        if col != self.current_column:
            return

        self.canvas.itemconfig(self.rectangles[row][col], fill='green')
        messagebox.showinfo("scan complete","entered data")


    def end_period(self):
        if self.current_column == 6:
            messagebox.showinfo("College is over", "Classes have ended for the day.")
            self.destroy()
        else:
            self.current_column += 1

    def copy_attendance(self):
        if self.current_column == 0:
            return

        for row in range(5):
            prev_color = self.colors[row][self.current_column - 1]
            self.colors[row][self.current_column] = prev_color
            self.canvas.itemconfig(self.rectangles[row][self.current_column], fill=prev_color)

    def create_buttons(self):
        self.end_period_button = tk.Button(self, text="End Period", command=self.end_period)
        self.end_period_button.pack(side=tk.LEFT, padx=10)

        self.copy_attendance_button = tk.Button(self, text="Copy Attendance", command=self.copy_attendance)
        self.copy_attendance_button.pack(side=tk.LEFT, padx=10)

        self.scan_button = tk.Button(self, text="Scan", command=self.scan)
        self.scan_button.pack(side=tk.RIGHT, padx=10, pady=10)

    def scan(self):
        import barcode

        scanned_data = barcode.scan()

        for row in range(5):
            if self.row_labels[row] == scanned_data:
                self.toggle_color(row, self.current_column)
                return

if __name__ == "__main__":
    app = AttendanceApp()
    app.mainloop()
