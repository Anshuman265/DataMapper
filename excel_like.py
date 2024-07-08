import tkinter as tk

class ExcelApp:
    def __init__(self, root, rows, columns):
        self.root = root
        self.root.title("Simple Excel App")
        
        self.cells = {}
        
        for row in range(rows):
            for column in range(columns):
                self.create_cell(row, column)
        
    def create_cell(self, row, column):
        entry = tk.Entry(self.root, width=10)
        entry.grid(row=row, column=column, padx=1, pady=1)
        self.cells[(row, column)] = entry

if __name__ == "__main__":
    root = tk.Tk()
    app = ExcelApp(root, rows=10, columns=10)  # You can set the number of rows and columns here
    root.mainloop()
