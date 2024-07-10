# Importing the required library
import tkinter as tk
from tkinter import filedialog,messagebox
import csv
import pandas as pd


# Application's memory 
# Reading the options file
df = pd.read_csv("options.csv")
mapping = pd.read_csv("mapping.csv")
# Convert the DataFrame column to a list
options_list = df['Options'].tolist()


# Running the application
class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Valuefy file converter")
        self.uploaded_file = None
        self.desired_format = None
        self.mapping = {""}

        # Creating frames for uploading and downloading the file
        self.upload_frame = tk.Frame(self)
        self.upload_frame.pack(fill="x")
        self.format_frame = tk.Frame(self)
        self.format_frame.pack(fill="x")
        self.mapping_frame = tk.Frame(self)
        self.mapping_frame.pack(fill="both", expand=True)
        self.download_frame = tk.Frame(self)
        self.download_frame.pack(fill="x")

        # Create upload button
        self.upload_button = tk.Button(self.upload_frame, text="Upload", command=self.upload_file)

        self.upload_button.pack(side="left")
 
        # Create the list of options 
        self.options_list = options_list

        # Create format selection
        self.format_label = tk.Label(self.format_frame, text="Choose format:")
        self.format_label.pack(side="left")
        self.format_var = tk.StringVar()
        self.format_var.set("Select format")
        self.format_menu = tk.OptionMenu(self.format_frame, self.format_var, "Select format", command=self.select_format,*self.options_list)
        self.format_menu.pack(side="left")
        self.add_format_button = tk.Button(self.format_frame, text="Add new format", command=self.add_format)
        self.add_format_button.pack(side="left")

        # Create mapping columns
        # Add entry widget in the loop
        self.desired_column = tk.Listbox(self.mapping_frame, width=20)
        idx = 1
        for x in list(mapping["vf"]):
            self.desired_column.insert(idx,x)
            idx = idx + 1
        self.desired_column.pack(side="left")
        self.uploaded_column = tk.Listbox(self.mapping_frame, width=20)
        self.uploaded_column.pack(side="left")

        # Create download button
        self.download_button = tk.Button(self.download_frame, text="Download in chosen format", command=self.download_file)
        self.download_button.pack(side="left")
                
    def select_format(self, format):
        self.desired_format = format
        if format != "Select format":
            idx = 1
            for x in list(mapping[str(format)]):
                self.uploaded_column.insert(idx,x)
                idx = idx + 1
        if format == "Select format":
            self.uploaded_column.delete(0,tk.END)

    def upload_file(self):
        self.uploaded_file = filedialog.askopenfilename()
        self.uploaded_column.delete(0, tk.END)
        with open(self.uploaded_file, "r") as file:
            reader = csv.reader(file)
            headers = next(reader)
            for header in headers:
                self.uploaded_column.insert(tk.END, header)
                
    def add_format(self):
        format_name = tk.simpledialog.askstring("Add new format", "Enter format name:")
        if format_name:
            new_format = pd.DataFrame([{ 'Options': format_name }])
            df_2 = pd.concat([df, new_format], ignore_index=True)
            df_2.to_csv("options.csv",index=False)
            messagebox.showinfo("Info", "Format added successfully. The application will reload.")
            reload_app()


    def download_file(self):
        if self.uploaded_file and self.desired_format:
            uploaded_df = pd.read_csv(self.uploaded_file)
            desired_df = pd.DataFrame(columns=[self.desired_column.get(i) for i in range(self.desired_column.size())])
            for i in range(self.desired_column.size()):
                desired_df[self.desired_column.get(i)] = uploaded_df[self.uploaded_column.get(i)]
            desired_df.to_csv(f"{self.desired_format}.csv", index=False)

def reload_app():
    app.destroy()
    main()

def main():
    global df, mapping, options_list, app
    df = pd.read_csv("options.csv")
    mapping = pd.read_csv("mapping.csv")
    options_list = df['Options'].tolist()
    app = Application()
    app.mainloop()

if __name__ == "__main__":
    main()