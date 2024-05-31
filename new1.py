import tkinter as tk
from tkinter import messagebox
import csv
import os
from datetime import datetime

from tabulate import tabulate

class AttendanceApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Attendance")
        self.geometry("1366x768")
        self.iconbitmap("graduation-cap.ico")

        self.roll_numbers = self.read_roll_numbers("roll_numbers.txt")

        self.original_rect_width = 50
        self.original_rect_height = 30
        self.rect_width = int(self.original_rect_width * 1.3)
        self.rect_height = int(self.original_rect_height * 1.3)
        self.padding = 5
        self.canvas_width = 1024
        self.canvas_height = 600
        self.offset_x = (self.canvas_width - (7 * self.rect_width + 6 * self.padding)) // 2
        self.offset_y = (self.canvas_height - (len(self.roll_numbers) * self.rect_height + (len(self.roll_numbers)-1) * self.padding)) // 2
        self.current_column = 0

        self.current_day = datetime.now().strftime("%A")
        self.day_label = tk.Label(self, text=f"Today is {self.current_day}", font=("Arial", 20))
        self.day_label.pack(side=tk.RIGHT, anchor=tk.NE, padx=10, pady=10)

        self.period_number = 0
        self.period_info_label = tk.Label(self, text="Period: 0", font=("Helvetica", 25))
        self.period_info_label.pack(side=tk.LEFT, before=self.day_label, anchor=tk.NE, padx=10, pady=10)

        self.staff_label = tk.Label(self, text=f"Staff : {self.staff(self.period_number)}", font=("Arial", 20))
        self.staff_label.pack(side=tk.LEFT, anchor=tk.NE, padx=10, pady=10)

        self.create_scrollable_frame()
        self.create_period_labels()
        self.create_row_labels()
        self.create_rectangles()
        self.create_buttons()

        self.canvas.bind("<MouseWheel>", self.on_mousewheel)

    def staff(self, period):
        day = self.current_day = datetime.now().strftime("%A")
        days = {
            'Monday': {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g'},
            'Tuesday': {0: 'Jhansi', 1: 'Vidhya', 2: 'Vanitha', 3: 'Kumari', 4: 'Prem', 5: 'Sangamithra', 6: 'Subhashini'},
            'Wednesday': {0: 'o', 1: 'p', 2: 'q', 3: 'r', 4: 's', 5: 't', 6: 'u'},
            'Thursday': {0: 'v', 1: 'w', 2: 'x', 3: 'y', 4: 'z', 5: 'A', 6: 'B'},
            'Friday': {0: 'Jhansi', 1: 'Vidhya', 2: 'Vanitha', 3: 'Kumari', 4: 'Prem', 5: 'Sangamithra', 6: 'Subhashini'},
            'Saturday': {0: 'J', 1: 'K', 2: 'L', 3: 'M', 4: 'N', 5: 'O', 6: 'P'}
        }

        self.teacher = days[day][period] if day in days and period in days[day] else None
        print(self.teacher)
        return self.teacher

    def read_roll_numbers(self, filename):
        try:
            with open(filename, "r") as file:
                return [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            messagebox.showerror("Error", "Roll numbers file not found!")
            self.destroy()

    def create_scrollable_frame(self):
        self.scrollable_frame = tk.Frame(self)
        self.scrollable_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.scrollable_frame, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.scrollable_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))

        self.canvas_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.canvas_frame, anchor='nw')

    def create_period_labels(self):
        self.period_labels = ['Period 0', 'Period 1', 'Period 2', 'Period 3', 'Period 4', 'Period 5', 'Period 6']
        for col, period_label in enumerate(self.period_labels):
            x_center = self.offset_x + col * (self.rect_width + self.padding) + self.rect_width // 2
            self.canvas.create_text(x_center, self.offset_y - 20, text=period_label)

    def create_row_labels(self):
        self.row_labels = self.roll_numbers
        for row, row_label in enumerate(self.row_labels):
            y_center = self.offset_y + row * (self.rect_height + self.padding) + self.rect_height // 2
            self.canvas.create_text(self.offset_x - 50, y_center, text=row_label)

    def create_rectangles(self):
        self.rectangles = []
        self.colors = [['red' for _ in range(7)] for _ in range(len(self.roll_numbers))]  # Initialize all rectangles to red
        for row in range(len(self.roll_numbers)):
            row_rectangles = []
            for col in range(7):
                x0 = self.offset_x + col * (self.rect_width + self.padding)
                y0 = self.offset_y + row * (self.rect_height + self.padding)
                x1 = x0 + self.rect_width
                y1 = y0 + self.rect_height
                rectangle_color = self.colors[row][col]
                rectangle = self.canvas.create_rectangle(x0, y0, x1, y1, fill=rectangle_color)
                self.canvas.tag_bind(rectangle, '<Button-1>',
                                     lambda event, row=row, col=col: self.toggle_color(row, col))
                row_rectangles.append(rectangle)
            self.rectangles.append(row_rectangles)

    def toggle_color(self, row, col):
        if col != self.current_column:
            return

        self.canvas.itemconfig(self.rectangles[row][col], fill='green')
        current_color = self.colors[row][col]
        new_color = 'green' if current_color == 'red' else 'red'
        self.colors[row][col] = new_color
        self.canvas.itemconfig(self.rectangles[row][col], fill=new_color)

    def end_period(self):
        self.period_number += 1
        self.staff(self.period_number)
        self.period_info_label.config(text=f"Period: {self.period_number}")
        self.staff_label.config(text=f"Staff: {self.staff(self.period_number)}")


        if self.current_column == 6:
            messagebox.showinfo("College is over", "Classes have ended for the day.")
            self.save_attendance_data()
            self.current_column = 0
            self.create_reset_button()

        else:
            self.current_column += 1

    def create_reset_button(self):
        self.reset_button = tk.Button(self, text="Reset", command=self.reset_attendance)
        self.reset_button.pack(side=tk.RIGHT, padx=10)
        self.period_number = 0


    def reset_attendance(self):
        self.reset_button.destroy()
        self.period_info_label.config(text="Period: 0")
        self.staff_label.config(text=f"Staff: {self.staff(0)}")
        for row_rectangles in self.rectangles:
            for rectangle in row_rectangles:
                self.canvas.itemconfig(rectangle, fill='red')

    def save_attendance_data(self):
        folder_name = "attendancedata"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        messagebox.showinfo("Attendance Saved", "Attendance data has been saved to attendance.csv")
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{folder_name}/attendance_{timestamp}.csv"

        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(
                ["Roll Number", "Period 0", "Period 1", "Period 2", "Period 3", "Period 4", "Period 5", "Period 6"])
            for row, row_label in enumerate(self.row_labels):
                data = [row_label]
                attendance_status = ['Present' if color == 'green' else 'Absent' for color in self.colors[row]]
                data.extend(attendance_status)
                writer.writerow(data)
        os.system(f'start excel {filename}')

    def copy_attendance(self):
        if self.current_column == 0:
            return

        for row in range(len(self.roll_numbers)):
            prev_color = self.colors[row][self.current_column - 1]
            self.colors[row][self.current_column] = prev_color

            self.canvas.itemconfig(self.rectangles[row][self.current_column], fill=prev_color)
    def print_attendance_details(self):
        # Initialize data for the table
        table_data = [["Roll Number"] + self.period_labels]

        # Add attendance data for each student
        for row_label, colors in zip(self.row_labels, self.colors):
            attendance_status = ['Present' if color == 'green' else 'Absent' for color in colors]
            table_data.append([row_label] + attendance_status)

        # Generate the table
        attendance_table = tabulate(table_data, headers="firstrow", tablefmt="grid")

        # Display attendance details in message box
        messagebox.showinfo("Attendance Details", attendance_table)

    def create_buttons(self):
        self.end_period_button = tk.Button(self, text="End Period", command=self.end_period)
        self.end_period_button.pack(side=tk.LEFT, padx=10)

        self.copy_attendance_button = tk.Button(self, text="Copy Attendance", command=self.copy_attendance)
        self.copy_attendance_button.pack(side=tk.LEFT, padx=10)

        self.scan_button = tk.Button(self, text="Scan", command=self.scan)
        self.scan_button.pack(side=tk.RIGHT, padx=10, pady=10)

        self.print_attendance_button = tk.Button(self, text="Show Attendance Details", command=self.print_attendance_details)
        self.print_attendance_button.pack(side=tk.LEFT, padx=10)

    def scan(self):
        import barcode
        scanned_data = barcode.scan()

        for row in range(len(self.roll_numbers)):
            for col in range(7):
                if self.row_labels[row] == scanned_data:  # Check if the scanned data matches the row label
                    self.toggle_color(row, self.current_column)

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

if __name__ == "__main__":
    app = AttendanceApp()
    app.mainloop()

