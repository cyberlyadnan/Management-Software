# importing modules
import csv
from tkinter import *
# from PIL import ImageTk, Image
import os
import random
import sqlite3
import time
import webbrowser
from multiprocessing import Process

import matplotlib.pyplot as plt
# from PIL import ImageTk
from matplotlib.backends.backend_pdf import PdfPages
import datetime
import json
import pandas
from tkinter import ttk, filedialog
from tkcalendar import *
from tkinter import messagebox




DATABASE_NAME="wood_management_system"
TITLE_FONT = ("Berlin Sans FB", 35,)
LABEL_FRAME_FONT = ("Times New Roman", 16, "bold")
BUTTONS_FONT= ("Arial", 16, "bold")
ENTRY_LABEL_FONT= ("Arial", 16, "bold")
BUTTONS_COLOR= "tan1"


class Window:
    def __init__(self, root):
        self.root = root
        self.root.wm_iconbitmap("icon.ico")
        self.root.state('zoomed')
        self.root.title("Wood Management System")
        self.root.geometry("1600x900+110+0")
        self.root.config(bg="lightgrey")
        self.button_text = "Raw Material"
        self.table_data = []

        with open("data.json", "r") as data_file:
            data = json.load(data_file)
        with open("notice.json", "r") as new_data_file:
            notice_data = json.load(new_data_file)

        def button_function(button, index):
            input_frame_box.config(text=button.cget("text"), font=("Times New Roman", 25, "bold"), fg="red3")
            default_button_color()
            button.config(bg=BUTTONS_COLOR)
            self.button_text = button.cget("text").title()
            dropdown()
            dropdown_search2()
            show_all2()
            notice_board()

        def button7_function():
            response = messagebox.askquestion("Exit", "Sure!\nDo You Want To Exit!!!!")
            if response == "yes":
                self.root.destroy()

        def default_button_color():
            for btn in [button1, button2, button3, button4, button5, button6]:
                btn.config(bg="#FFD384")

        # Buttons
        buttons = [button1, button2, button3, button4, button5, button6]
        for i, button in enumerate(buttons, start=1):
            button.config(command=lambda b=button, idx=i: button_function(b, idx))


        def calculate(self):
            amount_entry.delete(0, END)
            try:
                amount_entry.insert(END, f"{int(quantity_entry.get()) * int(rates_entry.get())}")
            except ValueError:
                messagebox.showerror("ValueError", "Please Enter Numbers Only!")

        def clear_fields(self):
            fields_to_clear = [amount_entry, quantity_entry, rates_entry, supplier_entry]
            for field in fields_to_clear:
                field.delete(0, END)
            date_entry.set_date(f"{date.year}/{date.month}/{date.day}")

        def change_table_head(self, text):
            table_head.config(text=f"{text.title()}")

        def extract_data(self, event=""):
            row_data = self.table.focus()
            content = self.table.item(row_data)
            data_fetch = content["values"]
            self.clear_fields()

            date_entry.set_date(data_fetch[0])
            heads_dropdown.set(data_fetch[1])
            subheads_dropdown.set(data_fetch[2])
            volume_unit_entry.set(data_fetch[3])

            quantity_entry.insert(END, f"{data_fetch[4]}")
            rates_entry.insert(END, f"{data_fetch[5]}")
            amount_entry.insert(END, f"{data_fetch[6]}")
            supplier_entry.insert(END, f"{data_fetch[7]}")

        def update_data(self):
            self.highlight_button()
            button_update.config(bg="tan3")

            def update_success():
                db = sqlite3.connect(f"{DATABASE_NAME}.db")
                mycursor = db.cursor()
                row_data = self.table.focus()
                content = self.table.item(row_data)
                data_fetch = content["values"]

                calculate()

                head_table = subheads_dropdown.get().lower() if subheads_dropdown.get().lower() != "no-subhead" else heads_dropdown.get().lower()
                head = f"UPDATE '{head_table}' SET Date='{date_entry.get()}', Head='{heads_dropdown.get().title()}', 'Sub-Head'='{subheads_dropdown.get().title()}', 'Volume Parameters'='{volume_unit_entry.get().upper()}', 'Volume/Quantity'='{quantity_entry.get()}', 'Rates'='{rates_entry.get()}', 'Amount'='{amount_entry.get()}', 'Supplier'='{supplier_entry.get().title()}' WHERE Date='{data_fetch[0]}';"

                mycursor.execute(head)
                db.commit()

                if subheads_dropdown.get().lower() == "no-subhead":
                    clear_fields()

                if messagebox.showinfo("Success", "Successfully Updated The Data", parent=self.root):
                    show_all()

            subhead_list2 = [subhead for subhead in data[self.button_text][heads_dropdown.get().title()]]
            heads_list2 = [head for head in data[self.button_text]]

            if not all([heads_dropdown.get(), subheads_dropdown.get(), rates_entry.get(), quantity_entry.get(),
                        amount_entry.get()]):
                messagebox.showerror("Oops!", "All Fields Are Required!")
            elif not all([quantity_entry.get().isdigit(), rates_entry.get().isdigit(), amount_entry.get().isdigit()]):
                messagebox.showerror("TypeError", "Please Enter Numbers, Not String!!")
            elif heads_dropdown.get().title() not in heads_list2:
                messagebox.showerror("1TypeError", "Invalid Head Selected, Add Them To Continue")
            elif volume_unit_entry.get().upper() not in data["Units"]:
                messagebox.showerror("2TypeError", "Invalid Unit Selected, Add Them To Continue")
            elif subheads_dropdown.get().title() not in subhead_list2:
                if subheads_dropdown.get().title() == "" or subheads_dropdown.get() == "No-SubHead":
                    update_success()
                else:
                    messagebox.showerror("3TypeError", "Invalid Sub-Head Selected, Add Them To Continue")
            else:
                update_success()

        def delete_data(self):
            self.highlight_button()
            button_delete.config(bg="tan3")

            db = sqlite3.connect(f"{DATABASE_NAME}.db")
            mycursor = db.cursor()

            row_data = self.table.focus()
            content = self.table.item(row_data)
            data_fetch = content["values"]

            head_table = subheads_dropdown.get().lower() if subheads_dropdown.get().lower() != "no-subhead" else heads_dropdown.get().lower()
            head = f"DELETE FROM '{head_table}' WHERE Date='{data_fetch[0]}'"

            mycursor.execute(head)

            if messagebox.showinfo("Success", "Successfully Deleted The Data", parent=self.root):
                db.commit()
                mycursor.close()

                try:
                    show_all2()
                    clear_fields()
                except:
                    pass

        all_tables = []
        def create_tables(self):
            for button in data:
                if button == "Units":
                    pass
                else:
                    for heads in data[button]:
                        if data[button][heads] == "" or len(data[button][heads]) == 0:
                            all_tables.append(heads)
                        else:
                            for element in data[button][heads]:
                                all_tables.append(element)
        create_tables()

        def save(self):
            self.highlight_button()
            button_save.config(bg="tan3")

            def save_success():
                db = sqlite3.connect(f"{DATABASE_NAME}.db")
                mycursor = db.cursor()

                head_table = subheads_dropdown.get().lower() if subheads_dropdown.get().lower() != "no-subhead" else heads_dropdown.get().lower()
                head = f"insert into '{head_table}' (Date, Head, 'Sub-Head', 'Volume Parameters', 'Volume/Quantity', 'Rates', 'Amount', 'Supplier') values ('{date_entry.get()}', '{heads_dropdown.get().title()}', '{subheads_dropdown.get().title()}', '{volume_unit_entry.get().upper()}', '{quantity_entry.get()}', '{rates_entry.get()}', '{amount_entry.get()}', '{supplier_entry.get().title()}')"

                mycursor.execute(head)
                db.commit()

                if subheads_dropdown.get().lower() == "no-subhead":
                    calculate()
                    clear_fields()

                if messagebox.showinfo("Success", "Successfully Saved The Data", parent=self.root):
                    show_all()
                    mycursor.close()

            subhead_list2 = [subhead for subhead in data[self.button_text][heads_dropdown.get().title()]]
            heads_list2 = [head for head in data[self.button_text]]

            if not all([heads_dropdown.get(), subheads_dropdown.get(), rates_entry.get(), quantity_entry.get(),
                        amount_entry.get()]):
                messagebox.showerror("Oops!", "All Fields Are Required!")
            elif not all([quantity_entry.get().isdigit(), rates_entry.get().isdigit(), amount_entry.get().isdigit()]):
                messagebox.showerror("TypeError", "Please Enter Numbers, Not String!!")
            elif heads_dropdown.get().title() not in heads_list2 or volume_unit_entry.get().upper() not in data[
                "Units"]:
                messagebox.showerror("TypeError", "Invalid Head, Sub-Head, or Unit Selected, Add Them To Continue")
            elif subheads_dropdown.get().title() not in subhead_list2:
                if subheads_dropdown.get().title() == "" or subheads_dropdown.get() == "No-SubHead":
                    save_success()
                else:
                    messagebox.showerror("TypeError", "Invalid Sub-Head Selected, Add Them To Continue")
            else:
                save_success()

        def fetch_data(self):
            db = sqlite3.connect(f"{DATABASE_NAME}.db")
            mycursor = db.cursor()

            head_table = 'gross raw wood'  # Change this to your default table name
            mycursor.execute(f"SELECT * FROM '{head_table}' ORDER BY Date DESC")
            data_sql = mycursor.fetchall()

            if len(data_sql) != 0:
                self.table_data.clear()
                for i in data_sql:
                    self.table_data.append(list(i))
                    self.table.insert("", END, values=i)
                db.commit()
            else:
                pass  # Handle the case where no data is found, or show an error message

            db.close()

        def search_by_date(self):
            db = sqlite3.connect(f"{DATABASE_NAME}.db")
            mycursor = db.cursor()

            try:
                if checked_state.get() == 1:
                    mycursor.execute(
                        f"SELECT * FROM '{heads_dropdown_search.get().lower()}' WHERE Date BETWEEN '{date_search.get()}' AND '{date_search1.get()}';")
                else:
                    if subheads_search.get() == "No-SubHead":
                        head_table = heads_dropdown_search.get().lower()
                    else:
                        head_table = subheads_search.get().lower()

                    change_table_head(head_table)
                    mycursor.execute(f"SELECT * FROM '{head_table}' WHERE Date = '{date_search.get()}'")

                data_sql = mycursor.fetchall()

                if len(data_sql) != 0:
                    self.table.delete(*self.table.get_children())
                    self.table_data.clear()
                    for i in data_sql:
                        self.table_data.append(list(i))
                        self.table.insert("", END, values=i)
                    db.commit()
                else:
                    self.table.delete(*self.table.get_children())
                    messagebox.showerror("Empty Table", "Oops!!\n No Data Found!!!")

            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

            db.close()

        def show_data(self, head_table):
            db = sqlite3.connect(f"{DATABASE_NAME}.db")
            mycursor = db.cursor()
            mycursor.execute(f"SELECT * FROM '{head_table}' ORDER BY Date DESC")
            data_sql = mycursor.fetchall()

            if len(data_sql) != 0:
                self.table.delete(*self.table.get_children())
                self.table_data.clear()
                for i in data_sql:
                    self.table_data.append(list(i))
                    self.table.insert("", END, values=i)
                db.commit()
            else:
                self.table.delete(*self.table.get_children())
                if head_table.lower() == "no-subhead" or head_table.lower() == "":
                    # messagebox.showerror("Empty Table", "Oops!!\n No Data Found!!!")  # Uncomment this line if needed
                    pass

            db.close()

        def show_all(self):
            head_table = heads_dropdown_search.get().lower() if subheads_search.get().lower() == "no-subhead" or subheads_search.get().lower() == "" else subheads_search.get().lower()
            change_table_head(head_table)
            self.show_data(head_table)

        def show_all2(self):
            head_table = subheads_search.get().lower() if subheads_search.get().lower() != "no-subhead" else heads_dropdown_search.get().lower()
            change_table_head(head_table)
            self.show_data(head_table)

        def combobox_conditions(self, e):
            self.sub_head_dropdown()

        def dropdown(self):
            heads_list654 = [i for i in data[self.button_text]]
            heads_dropdown["value"] = heads_list654
            heads_dropdown.set(heads_list654[0])
            self.sub_head_dropdown()

        def sub_head_dropdown(self):
            try:
                subhead_list = data[self.button_text][heads_dropdown.get()][0:]
            except:
                pass
            else:
                print("pass")
            finally:
                try:
                    if not data[self.button_text][heads_dropdown.get()][0:]:
                        subheads_dropdown.set("")
                        subheads_dropdown["value"] = ("No-SubHead")
                    else:
                        subheads_dropdown.set("")
                        subheads_dropdown["value"] = subhead_list
                except ValueError:
                    pass
                    # subheads_dropdown.set("No-SubHead")

        # for search portion

        def combobox_conditions_search(self, e):
            self.sub_head_dropdown_search2()

        def sub_head_dropdown_search2(self):
            try:
                subhead_list123 = data[self.button_text][heads_dropdown_search.get()][0:]
            except:
                print("pass")
            else:
                print("else pass")
            finally:
                try:
                    if not data[self.button_text][heads_dropdown_search.get()][0:]:
                        subheads_search["value"] = ("No-SubHead")
                        subheads_search.set("No-SubHead")
                    else:
                        subheads_search["value"] = subhead_list123
                        subheads_search.set(f"{subhead_list123[0]}")
                except:
                    print("some error in search")
                    subheads_dropdown.set("No-SubHead")

        def dropdown_search2(self):
            heads_list6542 = [i for i in data[self.button_text]]
            heads_dropdown_search["value"] = heads_list6542
            heads_dropdown_search.set(heads_list6542[0])
            self.sub_head_dropdown_search2()

        def add():
            highlight_button()
            button_add.config(bg="tan3")
            db = sqlite3.connect(f"{DATABASE_NAME}.db")
            mycursor = db.cursor()
            new_file = [i for i in data[self.button_text]]

            if volume_unit_entry.get().upper() not in data["Units"]:
                data["Units"].append(volume_unit_entry.get().upper())
                with open("data.json", "w") as data_file0:
                    json.dump(data, data_file0, indent=4)
                new_list = [unit for unit in data["Units"]]
                volume_unit_entry["value"] = new_list
                messagebox.showinfo("Success", "Successfully Added New Unit...")
                dropdown()

            if not heads_dropdown.get().title():
                messagebox.showerror("Error", "Head Field Empty!!!")
                return

            if heads_dropdown.get().title() not in new_file:
                if not subheads_dropdown.get().title():
                    create_and_show_message(data, heads_dropdown, "Successfully Added Head")
                elif subheads_dropdown.get() == "No-SubHead":
                    create_and_show_message(data, heads_dropdown, "Successfully Added Head")
                elif subheads_dropdown.get().title() not in all_tables:
                    data[self.button_text][heads_dropdown.get().title()].append(subheads_dropdown.get().title())
                    with open("data.json", "w") as data_file:
                        json.dump(data, data_file, indent=4)
                    create_table_and_show_message(mycursor, subheads_dropdown)
                    dropdown()
                else:
                    messagebox.showerror("Error", "SubHead Already Exist")
            elif heads_dropdown.get().title() in new_file:
                if not subheads_dropdown.get().title() or subheads_dropdown.get() == "No-SubHead":
                    messagebox.showerror("Error", "Head Already Exist")
                elif subheads_dropdown.get().title() not in all_tables:
                    data[self.button_text][heads_dropdown.get().title()].append(subheads_dropdown.get().title())
                    with open("data.json", "w") as data_file:
                        json.dump(data, data_file, indent=4)
                    create_table_and_show_message(mycursor, subheads_dropdown)
                    dropdown()

        def create_and_show_message(data, dropdown, success_message):
            data[self.button_text][dropdown.get().title()] = []
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
            messagebox.showinfo("Success", success_message)

        def create_table_and_show_message(mycursor, dropdown):
            mycursor.execute(
                f"CREATE TABLE '{dropdown.get().lower()}' (Date DATE, Head varchar(100), 'Sub-Head' varchar(100), 'Volume Parameters' varchar(100), 'Volume/Quantity' int, 'Rates' int, 'Amount' int, 'Supplier' varchar(100));")
            messagebox.showinfo("Success", "Successfully Added SubHead")

        def prepare_data_for_export():
            return {
                "Date": [row[0] for row in self.table_data],
                "Head": [row[1] for row in self.table_data],
                "SubHead": [row[2] for row in self.table_data],
                "Volume Parameters": [row[3] for row in self.table_data],
                "Volume/Quantity": [row[4] for row in self.table_data],
                "Rates": [row[5] for row in self.table_data],
                "Amount": [row[6] for row in self.table_data],
                "Supplier": [row[7] for row in self.table_data]
            }

        def print_function():
            if len(self.table_data) == 0:
                messagebox.showerror("Oops!", "No Data To Print")
            else:
                dictionary = prepare_data_for_export()

                fln1 = os.path.join(os.getcwd(), f"Report{random.randint(1, 10000)}.xlsx")
                fln = fln1.replace("\\", "/")

                df = pd.DataFrame(dictionary)
                writer = pd.ExcelWriter(fln)
                df.to_excel(writer, sheet_name="Report")
                writer.save()
                os.startfile(fln, "print")

        def export():
            if len(self.table_data) == 0:
                messagebox.showerror("Oops!", "No Data To Export")
            else:
                dictionary = prepare_data_for_export()

                fln = filedialog.asksaveasfilename(
                    title="Save File",
                    defaultextension='.xlsx',
                    filetypes=(("Excel File", ".xlsx"), ("PDF", ".pdf"), ("HTML", ".html"), ("All Files", "*.")))

                df = pd.DataFrame(dictionary)

                if ".xlsx" in fln:
                    writer = pd.ExcelWriter(fln)
                    df.to_excel(writer, sheet_name="Report")
                    writer.save()
                    messagebox.showinfo("Success", "Your Excel Sheet Successfully Exported")

                if ".pdf" in fln:
                    fig, ax = plt.subplots(figsize=(9, 14))
                    ax.axis('off')
                    the_table = ax.table(cellText=df.values, colLabels=df.columns, loc='top')
                    pp = PdfPages(fln)
                    pp.savefig(fig, bbox_inches='tight')
                    pp.close()
                    messagebox.showinfo("Success", "Your PDF Successfully Exported")

                if ".html" in fln:
                    html = df.to_html()
                    with open(fln, "w") as txt_file:
                        txt_file.write(html)
                    messagebox.showinfo("Success", "Your HTML Successfully Exported")

        def highlight_button(*buttons):
            for button in buttons:
                button.configure(bg=BUTTONS_COLOR)

        def create_database():
            try:
                db = connect_to_database()
                mycursor = db.cursor()

                for table in all_tables:
                    create_table_query = f"CREATE TABLE '{table.lower()}' (`Date` DATE, `Head` varchar(100), `Sub-Head` varchar(100), `Volume Parameters` varchar(100), `Volume/Quantity` int, `Rates` int, `Amount` int, `Supplier` varchar(100));"
                    mycursor.execute(create_table_query)

                db.commit()
                db.close()

            except sqlite3.OperationalError as e:
                print(f"Error creating database: {e}")

        def connect_to_database():
            return sqlite3.connect(f'{DATABASE_NAME}.db')

        # Call create_database to ensure tables are created when the script starts
        create_database()

        table_new = {}

        def show_result():
            total = 0
            self.table2.delete(*self.table2.get_children())

            for i, value in table_new.items():
                self.table2.insert("", END, values=(i, value))
                total += value

            total_data = ("Total", total)
            self.table2.insert("", END, values=total_data)

        def result(e):
            table_new.clear()

            try:
                db = sqlite3.connect(f'{DATABASE_NAME}.db')
                with db:
                    mycursor = db.cursor()

                    for _head_ in data[heads_variable_featured.get()]:
                        if _head_ in all_tables:
                            query = f"SELECT * FROM '{_head_.lower()}' WHERE Date = ?"
                            mycursor.execute(query, (date_search_featured.get(),))
                            result_data = mycursor.fetchall()

                            for row in result_data:
                                table_new[_head_] = row[6]

                        elif _head_ not in all_tables:
                            for k in data[heads_variable_featured.get()][_head_]:
                                query = f"SELECT * FROM '{k.lower()}' WHERE Date = ?"
                                mycursor.execute(query, (date_search_featured.get(),))
                                result_data = mycursor.fetchall()

                                for row in result_data:
                                    table_new[k] = row[6]

                    show_result()

            except sqlite3.Error as e:
                print(f"SQLite error: {e}")




#>>>>>>>>>>>>>>>>>Graphic User Interface<<<<<<<<<<<<<<<<<<<

        # ________________Top title bar__________________s
        title_frame = Frame(self.root, bg="#A64B2A")
        title_frame.place(x=0, y=0, width=1600, height=60)

        # title bar text
        title = Label(title_frame, text="AlSoft", font=TITLE_FONT, bg="#A64B2A", fg="Yellow")
        title.pack(pady=5)

        # __________sidebar__________________
        sidebar_frame = Frame(self.root, bg="#E5BA73")
        sidebar_frame.place(x=0, y=60, width=300, height=800)

        sidebar_frame_box = LabelFrame(sidebar_frame, text="Select", relief=RIDGE, font=LABEL_FRAME_FONT, bd=4,
                                               bg="#E5BA73", pady=5)
        sidebar_frame_box.place(x=0, y=0, width=300, height=800)

# sidebar Buttons
        button1 = Button(sidebar_frame_box, command=button1_function, text="Raw Material", cursor="hand2",
                                 font=BUTTONS_FONT, bg="#FFD384", padx=19,
                                 pady=10, width=19)
        button1.grid(row=0, column=0)

        button2 = Button(sidebar_frame_box, command=button2_function, text="Goods Purchased", cursor="hand2",
                                 font=BUTTONS_FONT, bg="#FFD384",
                                 padx=19, pady=10, width=19)
        button2.grid(row=1, column=0)

        button3 = Button(sidebar_frame_box, command=button3_function, text="Manufacturing", cursor="hand2",
                                 font=BUTTONS_FONT, bg="#FFD384",
                                 padx=19, pady=10, width=19)
        button3.grid(row=2, column=0)

        button4 = Button(sidebar_frame_box, command=button4_function, text="Paint & Finishing", cursor="hand2",
                                 font=BUTTONS_FONT, bg="#FFD384",
                                 padx=19, pady=10, width=19)
        button4.grid(row=3, column=0)

        button5 = Button(sidebar_frame_box, command=button5_function, text="Packing", cursor="hand2",
                                 font=BUTTONS_FONT, bg="#FFD384", padx=19,
                                 pady=10, width=19)
        button5.grid(row=4, column=0)

        button6 = Button(sidebar_frame_box, command=button6_function, text="Stationary & Supplies",
                                 cursor="hand2", font=BUTTONS_FONT, bg="#FFD384",
                                 padx=19, pady=10, width=19)
        button6.grid(row=5, column=0)

        button7 = Button(sidebar_frame_box, command=button7_function, text="Exit", cursor="hand2",
                                 font=BUTTONS_FONT, bg="#FFD384",
                                 padx=19, pady=10, width=19)
        button7.grid(row=6, column=0)

        def callback(url):
                    webbrowser.open_new_tab(url)

        about_me = Label(sidebar_frame_box, cursor="hand2", text="About Alsoft", font=("Berlin Sans FB", 18),
                                 bg="#E5BA73", fg="brown4")
        about_me.grid(row=7, column=0, pady=(290, 5))
        about_me.bind("<Button-1>", lambda e:
        callback(
                    "https://adnanahmad9334.nicepage.io/?version=fe3c1037-908a-467f-ac9c-f2ba0e13878d&uid=13e2aebf-7530-41e5-b9cb-2f721dd7ce9f"))

                # ________________input frame_________________
        input_frame = Frame(self.root, bg="#FAEAB1")
        input_frame.place(x=300, y=60, width=1000, height=300)

        input_frame_box = LabelFrame(input_frame, text="Information", relief=RIDGE, font=LABEL_FRAME_FONT, bd=4,
                                             bg="#FAEAB1", pady=7, padx=20)
        input_frame_box.place(x=0, y=0, width=1000, height=300)

        date_label = Label(input_frame_box, text="Select Date:", font=ENTRY_LABEL_FONT, bg="#FAEAB1")
        date_label.grid(column=0, row=0, sticky="w")

        head_label = Label(input_frame_box, text="Select Head:", font=ENTRY_LABEL_FONT, bg="#FAEAB1")
        head_label.grid(column=0, row=1, sticky="w")

        subheads_label = Label(input_frame_box, text="Select SubHead:", font=ENTRY_LABEL_FONT, bg="#FAEAB1")
        subheads_label.grid(column=0, row=2, sticky="w")

        volume_label = Label(input_frame_box, text="Volume Parameters:", font=ENTRY_LABEL_FONT, bg="#FAEAB1")
        volume_label.grid(column=0, row=3, sticky="w")

        quantity_label = Label(input_frame_box, text="Volmne/Quantity:", font=ENTRY_LABEL_FONT, bg="#FAEAB1")
        quantity_label.grid(column=0, row=4, sticky="w")

        rates_label = Label(input_frame_box, text="Rates:", font=ENTRY_LABEL_FONT, bg="#FAEAB1")
        rates_label.grid(column=0, row=5, sticky="w")

        amount_label = Label(input_frame_box, text="Amount:", font=ENTRY_LABEL_FONT, bg="#FAEAB1")
        amount_label.grid(column=0, row=6, sticky="w")

        supplier_label = Label(input_frame_box, text="Supplier:", font=ENTRY_LABEL_FONT, bg="#FAEAB1")
        supplier_label.grid(column=0, row=7, sticky="w")

        date = datetime.datetime.now()
        date_entry = DateEntry(input_frame_box, locale='en_US', date_pattern='y/mm/dd', selectmode="day",
                                       year=date.year, month=date.month, day=date.day,
                                       font=('Arial', 15), width=22, borderwidth=0)
        date_entry.grid(column=1, row=0)

        heads_variable = StringVar()
        heads_dropdown = ttk.Combobox(input_frame_box, font=('Arial', 16), state="normal", textvariable=heads_variable)
        heads_list = [i for i in data[button1.cget("text").title()]]
        heads_dropdown["value"] = (heads_list)
        heads_dropdown.set(heads_list[0])
        heads_dropdown.grid(column=1, row=1)
        heads_dropdown.bind("<<ComboboxSelected>>", combobox_conditions)
        dropdown()

        subheads_dropdown = ttk.Combobox(input_frame_box, font=('Arial', 16), state="normal")
        subheads_dropdown["value"] = ("")
        subheads_dropdown.grid(column=1, row=2)

        volume_unit_entry = ttk.Combobox(input_frame_box, font=('Arial', 16), state="normal")
        heads_list_unit = [i for i in data["Units"]]
        volume_unit_entry["value"] = (heads_list_unit)
        volume_unit_entry.current(0)
        volume_unit_entry.grid(column=1, row=3)

        quantity_entry = Entry(input_frame_box, font=('Arial', 17))
        quantity_entry.grid(column=1, row=4)

        rates_entry = Entry(input_frame_box, font=('Arial', 17))
        rates_entry.grid(column=1, row=5)

        amount_entry = Entry(input_frame_box, font=('Arial', 17))
        amount_entry.grid(column=1, row=6)

        supplier_entry = Entry(input_frame_box, font=('Arial', 17))
        supplier_entry.grid(column=1, row=7)

        calculate_button = Button(input_frame_box, text="Calculate", width=10, font=("Arial", 13, "bold"), bg="khaki1",
                                  command=calculate)
        calculate_button.grid(column=2, row=6)

        error_frame = LabelFrame(input_frame_box, text=f"Notice: {datetime.datetime.today().date()}", fg="red3",
                                 font=("Times New Roman", 16, "bold"), width=350, height=200, relief=RIDGE, bd=4,
                                 bg="#FAEAB1")
        error_frame.place(x=600, y=5)

        scrollbar = Scrollbar(error_frame, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y)

        notice_area = Text(error_frame, height=9, width=35, font=("Arial", 12, "bold"), yscrollcommand=scrollbar.set,
                           bg="cornsilk2")
        notice_area.pack()

        scrollbar.config(command=notice_area.yview)

        save_button = Button(input_frame_box, command=notice_save, bg="khaki1", text="Save", font=("Arial", 12, "bold"),
                             padx=58)
        save_button.place(x=603, y=208)

        clear_button = Button(input_frame_box, command=clear_notice_board, bg="khaki1", text="Clear",
                              font=("Arial", 12, "bold"),
                              padx=60)
        clear_button.place(x=770, y=208)

        # _______________button frame_____________________
        button_frame = Frame(self.root, bg="#FAEAB1")
        button_frame.place(x=300, y=360, width=1000, height=50)

        button_frame_box = LabelFrame(button_frame, relief=RIDGE, font=LABEL_FRAME_FONT, bd=4, bg="#FAEAB1")
        button_frame_box.place(x=0, y=0, width=1000, height=50)

        button_save = Button(button_frame_box, command=save, text="Save", cursor="hand2", font=BUTTONS_FONT,
                             bg=BUTTONS_COLOR,
                             width=19)
        button_save.grid(column=0, row=0)

        button_update = Button(button_frame_box, text="Update", cursor="hand2", command=update_data, font=BUTTONS_FONT,
                               bg=BUTTONS_COLOR,
                               width=18)
        button_update.grid(column=1, row=0)

        button_delete = Button(button_frame_box, text="Delete", cursor="hand2", command=delete_data, font=BUTTONS_FONT,
                               bg=BUTTONS_COLOR,
                               width=18)
        button_delete.grid(column=2, row=0)

        button_add = Button(button_frame_box, text="Add", cursor="hand2", command=add, font=BUTTONS_FONT,
                            bg=BUTTONS_COLOR,
                            width=18)
        button_add.grid(column=3, row=0)

        # ________________result_frame______________________
        main_frame = Frame(self.root, bg="#FFD384")
        main_frame.place(x=1300, y=60, width=300, height=350)

        main_frame_box = LabelFrame(main_frame, text="Featured", relief=RIDGE, font=LABEL_FRAME_FONT, bd=4,
                                    bg="#FFD384")
        main_frame_box.place(x=0, y=0, width=300, height=350)

        head_frame = Frame(main_frame_box, bg="#FFD384")
        head_frame.pack(pady=(6, 0))

        select_date = Label(head_frame, text="- Select Date", bg="#FFD384", font=("Arial", 14, "bold"))
        select_date.grid(column=1, row=0, sticky="w")

        date_search_featured = DateEntry(head_frame, align='left', locale='en_US', date_pattern='y/mm/dd',
                                         selectmode="day",
                                         font=('Arial', 11), borderwidth=0)
        date_search_featured.grid(column=0, row=0, sticky="w")

        select_head = Label(head_frame, text=" - Select Head", bg="#FFD384", font=("Arial", 14, "bold"))
        select_head.grid(column=1, row=1, sticky="w")

        # l1= Label()
        heads_variable_featured = StringVar()
        for l in data:
            heads_variable_featured.set(l)
            pass
        heads_dropdown_featured = ttk.Combobox(head_frame, textvariable=heads_variable_featured, font=('Arial', 12),
                                               width=14, state="readonly", )
        # heads_list1 = [i for i in data[button1.cget("text").title()]]
        button_list = ["Raw Material", "Goods Purchased", "Manufacturing", "Paint & Finishing", "Stationary & Supplies",
                       "Packing"]
        heads_dropdown_featured["value"] = (button_list)
        heads_dropdown_featured.set(button_list[0])
        heads_dropdown_featured.grid(column=0, row=1, sticky="w", pady=3)
        heads_dropdown_featured.bind("<<ComboboxSelected>>", result)

        text_frame = Frame(main_frame_box, bg="#FFD384")
        text_frame.pack(pady=(10, 0))
        scroll_x1 = Scrollbar(text_frame, orient=HORIZONTAL)
        scroll_y1 = Scrollbar(text_frame, orient=VERTICAL)

        self.table2 = ttk.Treeview(text_frame, columns=("Product", "Amount"), xscrollcommand=scroll_x1.set,
                                   yscrollcommand=scroll_y1.set, )

        self.table2.config(xscrollcommand=scroll_x1.set)
        scroll_x1.pack(side=BOTTOM, fill=X)
        scroll_y1.pack(side=RIGHT, fill=Y)

        scroll_x1.config(command=self.table2.xview)
        scroll_y1.config(command=self.table2.yview)

        self.table2.heading("Product", text="Product", anchor="w")
        self.table2.heading("Amount", text="Amount", anchor="w")

        self.table2["show"] = "headings"

        self.table2.column("Product", width=170, anchor="w")
        self.table2.column("Amount", width=130, anchor="w")

        self.table2.pack(fill=BOTH, expand=1)
        self.table2.bind("<ButtonRelease>", show_result)

        # __________________table frame_______________________
        table_frame = Frame(self.root, bg="#EEEEDF")
        table_frame.place(x=300, y=410, width=1300, height=470)

        table_frame_search_box = LabelFrame(table_frame, relief=RIDGE, font=LABEL_FRAME_FONT, bd=4, bg="#EEEE95",
                                            pady=7, padx=5)
        table_frame_search_box.place(x=0, y=0, width=1300, height=50)



        heads_variable_search = StringVar()
        heads_dropdown_search = ttk.Combobox(table_frame_search_box, font=('Arial', 14), width=14, state="readonly",
                                             textvariable=heads_variable_search)
        heads_list = [i for i in data[button1.cget("text").title()]]
        heads_dropdown_search["value"] = (heads_list)
        heads_dropdown_search.grid(column=0, row=0)
        heads_dropdown_search.bind("<<ComboboxSelected>>", combobox_conditions_search)
        dropdown_search2()



        subheads_search = ttk.Combobox(table_frame_search_box, font=('Arial', 14),width=13, state="readonly")
        subheads_search["value"] = ("")
        subheads_search.grid(column=1, row=0, padx=5)


        date_search = DateEntry(table_frame_search_box,locale='en_US', date_pattern='y/mm/dd', selectmode="day", font=('Arial', 13), borderwidth=0)
        date_search.grid(column=2, row=0,padx=6)

        date_search1 = DateEntry(table_frame_search_box, locale='en_US', date_pattern='y/mm/dd', selectmode="day",
                                font=('Arial', 13), borderwidth=0)
        date_search1.grid(column=3, row=0, padx=6)

        checked_state = IntVar()
        checkbox = Checkbutton(table_frame_search_box, bg="#EEEE95", variable=checked_state, onvalue=1, offvalue=0)
        checkbox.grid(column=4, row=0)

        search_button= Button(table_frame_search_box, text="Search", cursor="hand2", command=search_by_date,  bg="cadetblue3", font=('Arial', 12, "bold"), width=14)
        search_button.grid(column=5, row=0, padx=2)

        search_all = Button(table_frame_search_box, text="Show All", cursor="hand2", command=show_all, bg="cadetblue3", font=('Arial', 12, "bold"), width=14)
        search_all.grid(column=6, row=0, padx=3)

        print_button = Button(table_frame_search_box, text="Print", cursor="hand2",command=print_function, bg="pale green", font=('Arial', 12, "bold"), width=14)
        print_button.grid(column=7, row=0, padx=2)

        export_button = Button(table_frame_search_box, text="Export", cursor="hand2", command=export, bg="pale green", font=('Arial', 12, "bold"), width=14)
        export_button.grid(column=8, row=0)


        table_head = Label(table_frame, text="Table Head",bg="bisque2", fg="Black", font=("Times New Roman", 15, "bold"))
        table_head.place(x=0, y=50, width=1300, height=25)

        table_area = Frame(table_frame, bg="#EEEEDF")
        table_area.place(x=0, y=75, width=1300, height=350)

        scroll_x = Scrollbar(table_area, orient=HORIZONTAL)
        scroll_y = Scrollbar(table_area, orient=VERTICAL)


        self.table = ttk.Treeview(table_area, columns=("Date", "Head", "Sub-Head", "Volume Parameters", "Volume/Quantity",
                                                     "Rates", "Amount", "Supplier"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set, )
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.table.xview)
        scroll_y.config(command=self.table.yview)

        self.table.heading("Date", text="Date", anchor="w")
        self.table.heading("Head", text="Head",anchor="w")
        self.table.heading("Sub-Head", text="Sub-Head",anchor="w")
        self.table.heading("Volume Parameters", text="Volume Parameters",anchor="w")
        self.table.heading("Volume/Quantity", text="Volume/Quantity",anchor="w")
        self.table.heading("Rates", text="Rates",anchor="w")
        self.table.heading("Amount", text="Amount",anchor="w")
        self.table.heading("Supplier", text="Supplier",anchor="w")

        self.table["show"] = "headings"

        self.table.column("Date", width=70, anchor="w")
        self.table.column("Head", width=150,anchor="w")
        self.table.column("Sub-Head", width=150,anchor="w")
        self.table.column("Volume Parameters", width=120,anchor="w")
        self.table.column("Volume/Quantity", width=120,anchor="w")
        self.table.column("Rates", width=100,anchor="w")
        self.table.column("Amount", width=100,anchor="w")
        self.table.column("Supplier", width=100,anchor="w")

        self.table.pack(fill=BOTH, expand=1)
        self.table.bind("<ButtonRelease>", extract_data)

        table_design = ttk.Style()
        table_design.theme_use("alt")
        table_design.configure("Treeview.Heading", font=("Arial", 12, "bold"), background='burlywood3', foreground='black', borderwidth=0)
        table_design.configure("Treeview", font=("Arial", 12), foreground='black',)
        # table_design.configure("Treeview", font=("bold"), background="#EEEEDF", foreground='black')
        self.table.tag_configure("Head", font=("Arial", 16, "bold"))
        # print(self.table_data)
        button1_function()
        button1_function()
        button1_function()
        dropdown_search2()
        dropdown()



# creating window
if __name__ == "__main__":
    root = Tk()
    screen = Window(root)
    # global screen

    root.mainloop()







