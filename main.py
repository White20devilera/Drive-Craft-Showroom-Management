import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import mysql.connector
from PIL import Image, ImageTk, ImageOps
import os
from tkinter import messagebox, filedialog
import shutil
import time
import hashlib

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors



#LIVE TIME FUNCTION
# ========================================================
def update_live_time(time_label):

    date_str = time.strftime("%Y-%m-%d")
    time_str = time.strftime("%I:%M:%S %p")
    full_string = f"📅 {date_str}  |  🕒 {time_str}"
    time_label.configure(text=full_string)


    time_label.after(1000, update_live_time, time_label)




####Role based login system....
##For staff some tabs are disabled...(vehicle_suppliers, business_analytics)
##For admin all the tabs are visible
def check_login():
    global login_frame

    username = ent_login_user.get().strip()
    password = ent_login_pass.get().strip()


    if not username or not password:
        messagebox.showwarning("Input Error", "Please enter both username and password!")
        return


    hashed_input = hash_password(password)

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="showroom_db"
        )
        cursor = conn.cursor()


        query = "SELECT username, role FROM users WHERE username = %s AND password_hash = %s AND status = 'Active'"
        cursor.execute(query, (username, hashed_input))
        user_match = cursor.fetchone()

        cursor.close()
        conn.close()

        if user_match:
            messagebox.showinfo("Success", f"Welcome back, {username}! 👋")


            lbl_user.configure(
                text=f"👤 User: {username.capitalize()}",
                fg_color=("#1f538d", "#2a6fb8")
            )


            login_frame.pack_forget()


            tabview._segmented_button.configure(state="normal")


            user_role = user_match[1]

            if user_role == "Sales_Staff":

                try:
                    tabview.delete("Vehicle Suppliers")
                    tabview.delete("Business Analytics")
                except:
                    pass


                try:
                    btn_delete.pack_forget()
                except:
                    pass
            else:

                try:
                    if "Vehicle Suppliers" not in tabview._tab_dict:
                        tabview.add("Vehicle Suppliers")
                        setup_suppliers_tab()
                except:
                    pass

                try:

                    btn_delete.pack(side="right", padx=10)
                except:
                    pass


            tabview.pack(padx=10, pady=10, fill="both", expand=True)


            tabview.set("Dashboard & Inventory")


            app.update_idletasks()


            app.unbind('<Return>')
        else:
            messagebox.showerror("Login Failed", "Invalid username or password! Please try again.")

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Authentication connection failed: {err}")








ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Vehicle Showroom & Inventory Manager v1.0")
app.geometry("1420x790")
app.resizable(False, False)




navbar_frame = ctk.CTkFrame(
    app,
    fg_color=("#e6e6e6", "#1e1e1e"),
    height=65,
    corner_radius=0
)
navbar_frame.pack(side="top", fill="x", pady=(0, 10))
navbar_frame.pack_propagate(False)


main_title_lbl = ctk.CTkLabel(
    navbar_frame,
    text="🏢  DRIVE CRAFT | SHOWROOM INVENTORY",
    font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"),
    text_color=("#1a252f", "#ffffff")
)
main_title_lbl.pack(side="left", padx=25, pady=12)



global lbl_user

lbl_user = ctk.CTkLabel(
    navbar_frame,
    text="👤 Please Login",
    font=ctk.CTkFont(family="Arial", size=13, weight="bold"),
    fg_color=("#e74c3c", "#c0392b"),
    text_color="white",
    corner_radius=6,
    height=30,
    padx=12
)
lbl_user.pack(side="right", padx=(10, 25), pady=15)


lbl_live_time = ctk.CTkLabel(
    navbar_frame,
    text="",
    font=ctk.CTkFont(family="Arial", size=13, weight="bold"),
    text_color=("#555555", "#aaaaaa"),
    height=30,
    padx=10
)
lbl_live_time.pack(side="right", padx=10, pady=15)


update_live_time(lbl_live_time)















tabview = ctk.CTkTabview(app, width=1380, height=740)





tabview.configure(
    segmented_button_fg_color=("#d0d5dd", "#2d3748"),
    segmented_button_selected_color=("#08BBFC", "#08BBFC"),
    segmented_button_selected_hover_color=("#08BAFC", "#08BAFC"),
    segmented_button_unselected_color=("#e4e7ec", "#1a202c"),
    segmented_button_unselected_hover_color=("#cfd4dc", "#2d3748"),
    text_color=("#101828", "#ffffff")
)

tabview.add("Dashboard & Inventory")
tabview.add("Add New Vehicle")
tabview.add("Sales & Billing")
tabview.add("Vehicle Suppliers")
tabview.add("Business Analytics")
tabview.add("Sales History")





def on_tab_changed():
    selected_tab = tabview.get()


    if selected_tab == "Vehicle Suppliers":
        if 'load_suppliers_data' in globals():
            load_suppliers_data()


    elif selected_tab == "Business Analytics":
        if 'trigger_analytics_refresh' in globals():
            trigger_analytics_refresh()



tabview.configure(command=on_tab_changed)





tabview._segmented_button.configure(state="disabled")

lbl_total_stock = None
lbl_available = None
lbl_sold = None
lbl_total_revenue = None














#### Login form




login_frame = ctk.CTkFrame(app, fg_color="transparent")
login_frame.pack(fill="both", expand=True)



login_card = ctk.CTkFrame(
    login_frame,
    width=420,
    height=480,
    corner_radius=16,
    fg_color=("#ffffff", "#242b35"),
    border_width=2,
    border_color=("#e2e8f0", "#334155")
)
login_card.place(relx=0.5, rely=0.48, anchor="center")
login_card.pack_propagate(False)

# --- BRANDING SECTION ---
lbl_brand = ctk.CTkLabel(
    login_card,
    text="DRIVE CRAFT",
    font=ctk.CTkFont(family="Segoe UI", size=28, weight="bold"),
    text_color=("#1f538d", "#64b5f6")
)
lbl_brand.pack(pady=(45, 2))

lbl_sub = ctk.CTkLabel(
    login_card,
    text="Showroom Management System v1.0",
    font=ctk.CTkFont(family="Segoe UI", size=12, weight="normal"),
    text_color=("#64748b", "#94a3b8")
)
lbl_sub.pack(pady=(0, 35))

# --- USERNAME FIELD ---
lbl_user_title = ctk.CTkLabel(
    login_card,
    text="Username",
    font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
    text_color=("#334155", "#cbd5e1")
)
lbl_user_title.pack(anchor="w", padx=45, pady=(5, 4))

global ent_login_user
ent_login_user = ctk.CTkEntry(
    login_card,
    width=330,
    height=38,
    placeholder_text="Enter your username",
    font=ctk.CTkFont(family="Segoe UI", size=13),
    fg_color=("#f8fafc", "#1e293b"),
    border_color=("#cbd5e1", "#475569"),
    border_width=1,
    corner_radius=8
)
ent_login_user.pack(padx=45, pady=(0, 18))

# --- PASSWORD FIELD ---
lbl_pass_title = ctk.CTkLabel(
    login_card,
    text="Password",
    font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
    text_color=("#334155", "#cbd5e1")
)
lbl_pass_title.pack(anchor="w", padx=45, pady=(5, 4))

global ent_login_pass
ent_login_pass = ctk.CTkEntry(
    login_card,
    width=330,
    height=38,
    placeholder_text="Enter your password",
    show="*",
    font=ctk.CTkFont(family="Segoe UI", size=13),
    fg_color=("#f8fafc", "#1e293b"),
    border_color=("#cbd5e1", "#475569"),
    border_width=1,
    corner_radius=8
)
ent_login_pass.pack(padx=45, pady=(0, 35))

# --- SECURE LOGIN BUTTON ---
btn_login = ctk.CTkButton(
    login_card,
    text="🔒  Secure Login",
    font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
    fg_color=("#1f538d", "#2a6fb8"),
    hover_color=("#1a4475", "#2460a1"),
    text_color="white",
    width=330,
    height=44,
    corner_radius=8
)
btn_login.pack(padx=45, pady=10)
btn_login.configure(command=check_login)


app.bind('<Return>', lambda event: check_login())

# PASSWORD HASHING FUNCTION (SHA-256)

### Login password is saved as a hash

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()











####Suppliers Tab

def setup_suppliers_tab():
    global supplier_table, ent_sup_name, ent_sup_company, cmb_sup_country, ent_sup_phone, ent_sup_email, ent_sup_comm


    supp_main_frame = ctk.CTkFrame(tabview.tab("Vehicle Suppliers"), fg_color='transparent')
    supp_main_frame.pack(fill="both", expand=True, padx=10, pady=10)


    left_form = ctk.CTkFrame(supp_main_frame, width=380)
    left_form.pack(side="left", fill="both", expand=False, padx=5, pady=15)
    left_form.pack_propagate(False)

    lbl_title = ctk.CTkLabel(
        left_form,
        text="➕ REGISTER NEW SUPPLIER / AGENT",
        font=ctk.CTkFont(family="Segoe UI", size=14, weight='bold'),
        text_color=("#1f538d", "#64b5f6")
    )
    lbl_title.pack(pady=20, padx=20, anchor="w")


    grid_form = ctk.CTkFrame(left_form, fg_color='transparent')
    grid_form.pack(pady=5, padx=15, fill='both', expand=True)
    grid_form.columnconfigure(0, weight=1)

    def add_form_field(label_text, placeholder, row_num, is_combo=False, combo_vals=None):
        ctk.CTkLabel(grid_form, text=label_text, font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold")).grid(
            row=row_num, column=0, sticky='w', pady=(3, 1), padx=10)
        if is_combo:
            cb = ctk.CTkComboBox(grid_form, values=combo_vals, width=320, font=ctk.CTkFont(family="Segoe UI", size=12),
                                 state="readonly")
            cb.grid(row=row_num + 1, column=0, pady=(0, 6), padx=10, sticky='w')
            return cb
        else:
            en = ctk.CTkEntry(grid_form, width=320, placeholder_text=placeholder,
                              font=ctk.CTkFont(family="Segoe UI", size=12))
            en.grid(row=row_num + 1, column=0, pady=(0, 6), padx=10, sticky='w')
            return en


    ent_sup_name = add_form_field("Supplier / Contact Name *", "e.g., Kenji Tanaka", 0)
    ent_sup_company = add_form_field("Company / Auction House Name", "e.g., USS Tokyo / Japan Auto Export", 2)
    cmb_sup_country = add_form_field("Source Country *", "", 4, is_combo=True,
                                     combo_vals=["Japan", "United Kingdom", "South Korea", "Sri Lanka", "Other"])
    cmb_sup_country.set("Japan")
    ent_sup_phone = add_form_field("Phone Number", "e.g., +81 90 1234 5678", 6)
    ent_sup_email = add_form_field("Email Address", "e.g., info@japanauto.com", 8)
    ent_sup_comm = add_form_field("Agent Commission (Rs.)", "e.g., 150000 (0 if none)", 10)

    # SUPPLIER SAVE BUTTON
    btn_save_supplier = ctk.CTkButton(
        left_form,
        text="💾 Save Supplier Record",
        font=ctk.CTkFont(family="Segoe UI", size=13, weight='bold'),
        fg_color="#26a65b",
        hover_color="#1e824c",
        height=38,
        command=save_supplier_logic
    )
    btn_save_supplier.pack(pady=20, padx=25, fill="x")


    right_table_frame = ctk.CTkFrame(
        supp_main_frame,
        fg_color=("#dbdbdb", "#212121"),
        border_width=1,
        border_color=("#b0b0b0", "#3a3a3a")
    )
    right_table_frame.pack(side="right", fill="both", expand=True, padx=5, pady=15)

    lbl_table_title = ctk.CTkLabel(
        right_table_frame,
        text="📋 REGISTERED SUPPLIERS & AGENTS DIRECTORY",
        font=ctk.CTkFont(family="Segoe UI", size=13, weight='bold')
    )
    lbl_table_title.pack(pady=15, padx=15, anchor="w")

    sup_buttons_frame = ctk.CTkFrame(right_table_frame, fg_color="transparent")
    sup_buttons_frame.pack(side="bottom", fill="x", pady=(10, 15), padx=15)


    columns = ('id', 'name', 'company', 'country', 'phone', 'email', 'commission')

    style = ttk.Style()
    style.theme_use('clam')
    bg_color = "#ffffff" if ctk.get_appearance_mode() == "Light" else "#2a2a2a"
    fg_color = "#000000" if ctk.get_appearance_mode() == "Light" else "white"
    heading_bg = "#eeeeee" if ctk.get_appearance_mode() == "Light" else "#333333"
    heading_fg = "#000000" if ctk.get_appearance_mode() == "Light" else "white"

    style.configure('Treeview', background=bg_color, foreground=fg_color, fieldbackground=bg_color, rowheight=30)
    style.configure('Treeview.Heading', background=heading_bg, foreground=heading_fg, font=('Arial', 10, 'bold'))


    supplier_table = ttk.Treeview(right_table_frame, columns=columns, show='headings')
    supplier_table.pack(side="top", fill='both', expand=True, padx=15, pady=(0, 5))


    supplier_table.heading('id', text='ID')
    supplier_table.heading('name', text='Supplier Name')
    supplier_table.heading('company', text='Company / Auction')
    supplier_table.heading('country', text='Country')
    supplier_table.heading('phone', text='Phone')
    supplier_table.heading('email', text='Email')
    supplier_table.heading('commission', text='Comm. (Rs.)')


    supplier_table.column('id', width=40, anchor='center')
    supplier_table.column('name', width=130)
    supplier_table.column('company', width=140)
    supplier_table.column('country', width=80, anchor='center')
    supplier_table.column('phone', width=110)
    supplier_table.column('email', width=130)
    supplier_table.column('commission', width=100, anchor='e')

    # SUPPLIER EDIT BUTTON
    btn_sup_edit = ctk.CTkButton(
        sup_buttons_frame,
        text="✏️ Edit Supplier",
        font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
        fg_color=("#2980b9", "#1f618d"),
        hover_color=("#1f618d", "#1a5276"),
        height=38,
        command=lambda: open_edit_supplier_window(supplier_table)
    )
    btn_sup_edit.pack(side="left", padx=(0, 5), expand=True, fill="x")

    # SUPPLIER DELETE BUTTON
    btn_sup_delete = ctk.CTkButton(
        sup_buttons_frame,
        text="❌ Remove Supplier",
        font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
        fg_color=("#c0392b", "#962d22"),
        hover_color=("#962d22", "#7b241c"),
        height=38,
        command=lambda: delete_supplier_logic(supplier_table)
    )
    btn_sup_delete.pack(side="right", padx=(5, 0), expand=True, fill="x")

    # Initial Data Load
    load_suppliers_data()












def save_supplier_logic():

    name = ent_sup_name.get().strip()
    company = ent_sup_company.get().strip()
    country = cmb_sup_country.get()
    phone = ent_sup_phone.get().strip()
    email = ent_sup_email.get().strip()

    try:
        commission = float(ent_sup_comm.get().strip()) if ent_sup_comm.get().strip() else 0.0
    except ValueError:
        messagebox.showerror("Input Error", "Commission must be a valid number!")
        return


    if not name or not country:
        messagebox.showwarning("Warning", "Supplier Name and Country fields are required!")
        return


    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="showroom_db"
        )
        cursor = conn.cursor()

        query = """INSERT INTO suppliers (supplier_name, company_name, country, phone_number, email, agent_commission) 
                   VALUES (%s, %s, %s, %s, %s, %s)"""
        values = (name, company, country, phone, email, commission)

        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()

        messagebox.showinfo("Success", f"🎯 Supplier '{name}' registered successfully!")


        ent_sup_name.delete(0, 'end')
        ent_sup_company.delete(0, 'end')
        ent_sup_phone.delete(0, 'end')
        ent_sup_email.delete(0, 'end')
        ent_sup_comm.delete(0, 'end')
        cmb_sup_country.set("Japan")

        load_suppliers_data()

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")


def delete_supplier_logic(table_widget):
    selected_item = table_widget.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select a supplier from the table to delete!")
        return

    item_data = table_widget.item(selected_item[0], 'values')
    sup_id = item_data[0]
    sup_name = item_data[1]


    confirm = messagebox.askyesno("Confirm Delete",
                                  f"Are you sure you want to permanently delete supplier '{sup_name}'?")
    if confirm:
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="showroom_db"
            )
            cursor = conn.cursor()

            cursor.execute("DELETE FROM suppliers WHERE supplier_id = %s", (sup_id,))
            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo("Deleted", "Supplier record removed successfully!")
            load_suppliers_data()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")



###Edit Supplier pop up window
def open_edit_supplier_window(table_widget):
    selected_item = table_widget.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select a supplier from the table to edit!")
        return


    item_data = table_widget.item(selected_item[0], 'values')
    sup_id = item_data[0]
    sup_name = item_data[1]
    sup_company = item_data[2]
    sup_country = item_data[3]
    sup_phone = item_data[4]
    sup_email = item_data[5]

    raw_comm = item_data[6].replace(',', '') if item_data[6] else "0"


    edit_win = ctk.CTkToplevel()
    edit_win.title(f"✏️ Edit Supplier - ID: {sup_id}")
    edit_win.geometry("400x580")
    edit_win.resizable(False, False)


    edit_win.grab_set()

    ctk.CTkLabel(
        edit_win,
        text=f"✏️ UPDATE SUPPLIER RECORD",
        font=ctk.CTkFont(family="Segoe UI", size=14, weight='bold'),
        text_color=("#1f538d", "#64b5f6")
    ).pack(pady=20, padx=20, anchor="w")

    form_frame = ctk.CTkFrame(edit_win, fg_color='transparent')
    form_frame.pack(pady=5, padx=20, fill='both', expand=True)

    def create_edit_field(lbl_text, default_val, row_num, is_combo=False, combo_vals=None):
        ctk.CTkLabel(form_frame, text=lbl_text, font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold")).grid(row=row_num, column=0, sticky='w', pady=(5, 2))
        if is_combo:
            cb = ctk.CTkComboBox(form_frame, values=combo_vals, width=350, font=ctk.CTkFont(family="Segoe UI", size=12),state="readonly")
            cb.grid(row=row_num + 1, column=0, pady=(0, 10), sticky='w')
            cb.set(default_val)
            return cb
        else:
            en = ctk.CTkEntry(form_frame, width=350, font=ctk.CTkFont(family="Segoe UI", size=12))
            en.grid(row=row_num + 1, column=0, pady=(0, 10), sticky='w')
            en.insert(0, default_val)
            return en


    edit_name = create_edit_field("Supplier / Contact Name *", sup_name, 0)
    edit_company = create_edit_field("Company / Auction House Name", sup_company, 2)
    edit_country = create_edit_field("Source Country *", sup_country, 4, is_combo=True,
                                     combo_vals=["Japan", "United Kingdom", "South Korea", "Sri Lanka", "Other"])
    edit_phone = create_edit_field("Phone Number", sup_phone, 6)
    edit_email = create_edit_field("Email Address", sup_email, 8)
    edit_comm = create_edit_field("Agent Commission (Rs.)", float(raw_comm), 10)

    #  UPDATE BUTTON LOGIC
    def update_logic():
        u_name = edit_name.get().strip()
        u_company = edit_company.get().strip()
        u_country = edit_country.get()
        u_phone = edit_phone.get().strip()
        u_email = edit_email.get().strip()

        try:
            u_comm = float(edit_comm.get().strip()) if edit_comm.get().strip() else 0.0
        except ValueError:
            messagebox.showerror("Input Error", "Commission must be a valid number!", parent=edit_win)
            return

        if not u_name or not u_country:
            messagebox.showwarning("Warning", "Name and Country fields cannot be empty!", parent=edit_win)
            return


        try:
            conn = mysql.connector.connect(host="localhost", user="root", password="", database="showroom_db")
            cursor = conn.cursor()

            query = """UPDATE suppliers 
                       SET supplier_name=%s, company_name=%s, country=%s, phone_number=%s, email=%s, agent_commission=%s 
                       WHERE supplier_id=%s"""
            cursor.execute(query, (u_name, u_company, u_country, u_phone, u_email, u_comm, sup_id))

            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo("Success", "Supplier record updated successfully!", parent=edit_win)
            edit_win.destroy()
            load_suppliers_data()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}", parent=edit_win)

    # Save Button
    ctk.CTkButton(
        edit_win,
        text="🔄 Update Supplier Details",
        font=ctk.CTkFont(family="Segoe UI", size=13, weight='bold'),
        fg_color="#2980b9",
        hover_color="#1f618d",
        height=40,
        command=update_logic
    ).pack(pady=20, padx=20, fill="x")



def load_suppliers_data():

    global load_suppliers_data

    for item in supplier_table.get_children():
        supplier_table.delete(item)


    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="showroom_db"
        )
        cursor = conn.cursor()
        cursor.execute(
            "SELECT supplier_id, supplier_name, company_name, country, phone_number, email, agent_commission FROM suppliers ORDER BY supplier_id DESC")
        rows = cursor.fetchall()

        for row in rows:

            formatted_comm = f"{row[6]:,.2f}"
            supplier_table.insert('', 'end', values=(row[0], row[1], row[2], row[3], row[4], row[5], formatted_comm))

        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error loading suppliers directory: {err}")












def reprint_invoice():
    try:

        selected_item = sales_table.selection()

        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a sale record from the table first! ⚠️")
            return

        row_data = sales_table.item(selected_item, "values")

        sale_id = row_data[0]  # Sale ID (Index 0)
        cust_name = row_data[1]  # Customer Name (Index 1)


        conn = mysql.connector.connect(
            host="localhost", user="root", password="", database="showroom_db"
        )
        cursor = conn.cursor()

        query = "SELECT vehicle_id FROM sales_history WHERE sale_id = %s"
        cursor.execute(query, (sale_id,))
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        if result and result[0]:
            v_id = result[0]
        else:
            v_id = sale_id


        clean_cust_name = cust_name.lower().strip()
        if clean_cust_name.endswith(".pdf"):
            clean_cust_name = clean_cust_name[:-4]

        clean_cust_name = clean_cust_name.replace(' ', '_')


        path_option_1 = os.path.abspath(f"invoices/invoice_{v_id}_{clean_cust_name}.pdf")
        path_option_2 = os.path.abspath(f"invoices/invoice_{v_id}_{clean_cust_name}.pdf.pdf")


        if os.path.exists(path_option_1):
            os.startfile(path_option_1)
            print(f"[SUCCESS]: Opened invoice PDF: {path_option_1}")
        elif os.path.exists(path_option_2):
            os.startfile(path_option_2)
            print(f"[SUCCESS]: Opened double-pdf invoice: {path_option_2}")
        else:
            messagebox.showerror(
                "File Not Found",
                f"Sorry, the invoice PDF could not be found! ❌\n\n"
                f"Tried Paths:\n1. {path_option_1}\n2. {path_option_2}\n\n"
                f"Please check your invoices folder."
            )

    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong while opening PDF: {e}")









#### Sales History Tab

def setup_sales_history_tab():
    global sales_table, ent_history_search


    history_main_frame = ctk.CTkFrame(tabview.tab("Sales History"), fg_color='transparent')
    history_main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # LIVE SEARCH BAR (Filter by ID or Name)
    search_bar_frame = ctk.CTkFrame(history_main_frame, fg_color='transparent')
    search_bar_frame.pack(side='top', fill='x', pady=(0, 10))

    ctk.CTkLabel(
        search_bar_frame,
        text='🔍 Search Customer / Invoice:',
        font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold")
    ).pack(side='left', padx=(5, 10))

    ent_history_search = ctk.CTkEntry(
        search_bar_frame,
        placeholder_text='Type Customer Name, NIC, or Sale ID...',
        width=380
    )
    ent_history_search.pack(side='left', padx=5)


    ent_history_search.bind("<KeyRelease>", lambda e: filter_sales_live())

    def clear_history_search():
        ent_history_search.delete(0, 'end')
        load_sales_history_data()

    btn_clear_history = ctk.CTkButton(
        search_bar_frame,
        text='Clear',
        width=70,
        fg_color="#555555",
        hover_color="#333333",
        command=clear_history_search
    )
    btn_clear_history.pack(side='left', padx=10)

    # QUICK PDF RE-PRINT BUTTON
    btn_reprint = ctk.CTkButton(
        search_bar_frame,
        text='🖨️ Re-print Receipt / View PDF',
        font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
        fg_color=("#1f538d", "#2a6fb8"),
        hover_color=("#1a4475", "#2460a1"),
        text_color="white",
        width=220,
        command=reprint_invoice
    )
    btn_reprint.pack(side='right', padx=5)


    table_container = ctk.CTkFrame(
        history_main_frame,
        fg_color=("#dbdbdb", "#212121"),
        border_width=1,
        border_color=("#b0b0b0", "#3a3a3a")
    )
    table_container.pack(side="bottom", fill="both", expand=True, pady=5)

    lbl_table_head = ctk.CTkLabel(
        table_container,
        text="📜 CUSTOMER PURCHASE & INVOICE HISTORY DIRECTORY",
        font=ctk.CTkFont(family="Segoe UI", size=13, weight='bold')
    )
    lbl_table_head.pack(pady=15, padx=15, anchor="w")


    columns = ('sale_id', 'cust_name', 'cust_phone', 'cust_nic', 'car_details', 'sale_date', 'amount', 'pay_mode')

    style = ttk.Style()
    style.theme_use('clam')
    bg_color = "#ffffff" if ctk.get_appearance_mode() == "Light" else "#2a2a2a"
    fg_color = "#000000" if ctk.get_appearance_mode() == "Light" else "white"
    heading_bg = "#eeeeee" if ctk.get_appearance_mode() == "Light" else "#333333"
    heading_fg = "#000000" if ctk.get_appearance_mode() == "Light" else "white"

    style.configure('Treeview', background=bg_color, foreground=fg_color, fieldbackground=bg_color, rowheight=30)
    style.configure('Treeview.Heading', background=heading_bg, foreground=heading_fg, font=('Arial', 10, 'bold'))

    sales_table = ttk.Treeview(table_container, columns=columns, show='headings')
    sales_table.pack(fill='both', expand=True, padx=15, pady=(0, 15))


    sales_table.heading('sale_id', text='Sale ID')
    sales_table.heading('cust_name', text='Customer Name')
    sales_table.heading('cust_phone', text='Phone Number')
    sales_table.heading('cust_nic', text='NIC No.')
    sales_table.heading('car_details', text='Purchased Vehicle (Brand/Model/Year)')
    sales_table.heading('sale_date', text='Sold Date')
    sales_table.heading('amount', text='Final Price (Rs.)')
    sales_table.heading('pay_mode', text='Payment Mode')


    sales_table.column('sale_id', width=60, anchor='center')
    sales_table.column('cust_name', width=140)
    sales_table.column('cust_phone', width=110)
    sales_table.column('cust_nic', width=100, anchor='center')
    sales_table.column('car_details', width=260)
    sales_table.column('sale_date', width=90, anchor='center')
    sales_table.column('amount', width=120, anchor='e')
    sales_table.column('pay_mode', width=100, anchor='center')

    # Initial Data Load
    load_sales_history_data()


def load_sales_history_data():
    for item in sales_table.get_children():
        sales_table.delete(item)

    try:
        conn = mysql.connector.connect(
            host="localhost", user="root", password="", database="showroom_db"
        )
        cursor = conn.cursor()


        query = """
                    SELECT s.sale_id, s.customer_name, s.customer_phone, s.customer_nic, 
                           CONCAT(v.brand, ' ', v.model, ' (', v.manufacture_year, ')') AS vehicle_info, 
                           s.sale_date, s.final_price, s.payment_mode 
                    FROM sales_history s
                    INNER JOIN vehicles v ON s.vehicle_id = v.vehicle_id
                    ORDER BY s.sale_id DESC
                """
        cursor.execute(query)
        rows = cursor.fetchall()

        for row in rows:
            formatted_price = f"{row[6]:,.2f}"
            sales_table.insert('', 'end',
                               values=(row[0], row[1], row[2], row[3], row[4], row[5], formatted_price, row[7]))

        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error loading sales history: {err}")



def filter_sales_live(event=None):
    search_text = ent_history_search.get().strip()

    for item in sales_table.get_children():
        sales_table.delete(item)

    try:
        conn = mysql.connector.connect(
            host="localhost", user="root", password="", database="showroom_db"
        )
        cursor = conn.cursor()


        query = """
            SELECT s.sale_id, s.customer_name, s.customer_phone, s.customer_nic, 
                   CONCAT(v.brand, ' ', v.model, ' (', v.manufacture_year, ')') AS vehicle_info, 
                   s.sale_date, s.final_price, s.payment_mode 
            FROM sales_history s
            INNER JOIN vehicles v ON s.vehicle_id = v.vehicle_id
            WHERE s.customer_name LIKE %s OR s.customer_nic LIKE %s OR s.sale_id LIKE %s
            ORDER BY s.sale_id DESC
        """
        search_param = f"%{search_text}%"
        cursor.execute(query, (search_param, search_param, search_param))
        rows = cursor.fetchall()

        for row in rows:
            formatted_price = f"{row[6]:,.2f}"
            sales_table.insert('', 'end',
                               values=(row[0], row[1], row[2], row[3], row[4], row[5], formatted_price, row[7]))

        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error filtering sales history: {err}")













### Main Window Dashboard Tab

def setup_dashboard_tab():
    global btn_delete
    global vehicle_table
    global lbl_total_stock, lbl_available, lbl_sold, lbl_total_revenue
    global lbl_stock_alert
    global cards_frame



    main_frame = ctk.CTkFrame(tabview.tab("Dashboard & Inventory"), fg_color='transparent')
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    lbl_stock_alert = ctk.CTkLabel(
        main_frame,
        text="",
        font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
        corner_radius=6,
        height=35
    )


    cards_frame = ctk.CTkFrame(main_frame, fg_color='transparent')
    cards_frame.pack(side='top', fill='x', pady=(0, 15))
    cards_frame.columnconfigure((0, 1, 2, 3), weight=1, uniform='column')


    c1 = ctk.CTkFrame(cards_frame, fg_color=("#2c3e50", "#1a252f"), height=48, corner_radius=8)
    c1.grid(row=0, column=0, padx=6, sticky="nsew")
    c1.pack_propagate(False)
    lbl_t1 = ctk.CTkLabel(c1, text='📊  Total Inventory', font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),text_color="white")
    lbl_t1.pack(side='left', padx=15, pady=5)
    lbl_total_stock = ctk.CTkLabel(c1, text="0", font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),text_color="white")
    lbl_total_stock.pack(side='right', padx=15, pady=5)

    c2 = ctk.CTkFrame(cards_frame, fg_color=("#1e7e34", "#114d20"), height=48, corner_radius=8)
    c2.grid(row=0, column=1, padx=6, sticky="nsew")
    c2.pack_propagate(False)
    lbl_t2 = ctk.CTkLabel(c2, text="🟢  Available For Sale", font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),text_color="white")
    lbl_t2.pack(side="left", padx=15, pady=5)
    lbl_available = ctk.CTkLabel(c2, text="0", font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),text_color="white")
    lbl_available.pack(side="right", padx=15, pady=5)





    c3 = ctk.CTkFrame(cards_frame, fg_color=("#bd2130", "#73141d"), height=48, corner_radius=8)
    c3.grid(row=0, column=2, padx=6, sticky="nsew")
    c3.pack_propagate(False)
    lbl_t3 = ctk.CTkLabel(c3, text="🔴  Total Vehicles Sold",font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"), text_color="white")
    lbl_t3.pack(side="left", padx=15, pady=5)
    lbl_sold = ctk.CTkLabel(c3, text="0", font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),text_color="white")
    lbl_sold.pack(side="right", padx=15, pady=5)






    c4 = ctk.CTkFrame(cards_frame, fg_color=("#117a8b", "#0a4b55"), height=48, corner_radius=8)
    c4.grid(row=0, column=3, padx=6, sticky="nsew")
    c4.pack_propagate(False)
    lbl_t4 = ctk.CTkLabel(c4, text="💰  Total Revenue", font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),text_color="white")
    lbl_t4.pack(side="left", padx=15, pady=5)
    lbl_total_revenue = ctk.CTkLabel(c4, text="Rs. 0.00", font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),text_color="white")
    lbl_total_revenue.pack(side="right", padx=15, pady=5)


    #SEARCH BAR

    search_frame = ctk.CTkFrame(main_frame, fg_color='transparent')
    search_frame.pack(side='top', fill='x', pady=(5, 5))

    entry_search = ctk.CTkEntry(search_frame, placeholder_text='🔍 Search by Brand or Model...', width=350)
    entry_search.pack(side='left', padx=(5, 10))

    entry_search.bind("<KeyRelease>", lambda e: filter_inventory_live(entry_search, combo_filter))


    ctk.CTkLabel(search_frame, text='Filter by Status: ', font=ctk.CTkFont(size=13)).pack(side='left', padx=5)
    combo_filter = ctk.CTkComboBox(search_frame, values=["All", "Available", "Sold"], width=130, state="readonly")
    combo_filter.set("All")
    combo_filter.pack(side="left", padx=5)

    combo_filter.configure(command=lambda v: filter_inventory_live(entry_search, combo_filter))


    def clear_search():
        entry_search.delete(0, 'end')
        combo_filter.set('All')
        load_table_data(vehicle_table)

    btn_clear_search = ctk.CTkButton(search_frame, text='Clear', width=70, fg_color="#555555", hover_color="#333333", command=clear_search)
    btn_clear_search.pack(side='left', padx=10)


    content_frame = ctk.CTkFrame(main_frame, fg_color='transparent')
    content_frame.pack(fill='both', expand=True)

    left_frame = ctk.CTkFrame(content_frame)
    left_frame.pack(side='left', fill='both', expand=True, padx=(5, 10), pady=5)
    columns = ('id', 'brand', 'model', 'year', 'mileage', 'price', 'status')

    style = ttk.Style()
    style.theme_use('clam')

    current_mode = ctk.get_appearance_mode()

    if current_mode == "Light":
        bg_color = "#ffffff"
        fg_color = "#000000"
        heading_bg = "#eeeeee"
        heading_fg = "#000000"
    else:
        bg_color = "#2a2a2a"
        fg_color = "white"
        heading_bg = "#333333"
        heading_fg = "white"

    style.configure('Treeview', background=bg_color, foreground=fg_color, fieldbackground=bg_color, rowheight=30)
    style.configure('Treeview.Heading', background=heading_bg, foreground=heading_fg, font=('Arial', 10, 'bold'))
    style.map('Treeview', background=[('selected', '#1f538d')])

    global vehicle_table


    vehicle_table = ttk.Treeview(left_frame, columns=columns, show='headings')
    vehicle_table.pack(fill='both', expand=True, padx=10, pady=10)


    vehicle_table.heading('id', text='ID')
    vehicle_table.heading('brand', text='Brand')
    vehicle_table.heading('model', text='Model')
    vehicle_table.heading('year', text='Year')
    vehicle_table.heading('mileage', text='Mileage (km)')
    vehicle_table.heading('price', text='Price (Rs.)')
    vehicle_table.heading('status', text='Status')


    vehicle_table.column('id', width=40, anchor='center')
    vehicle_table.column('brand', width=100)
    vehicle_table.column('model', width=100)
    vehicle_table.column('year', width=70, anchor='center')
    vehicle_table.column('mileage', width=90, anchor='center')
    vehicle_table.column('price', width=110)
    vehicle_table.column('status', width=90, anchor='center')


    right_frame = ctk.CTkFrame(content_frame, width=480, height=450, fg_color=("#dbdbdb", "#212121"), border_width=2,border_color=("#b0b0b0", "#3a3a3a"))
    right_frame.pack(side="right", fill="both", expand=False, padx=5, pady=15)
    right_frame.pack_propagate(False)

    buttons_row_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
    buttons_row_frame.pack(side="bottom", fill="x", pady=(10, 15), padx=15)


    top_container = ctk.CTkFrame(right_frame, fg_color="transparent")
    top_container.pack(side="top", fill="x", padx=20, pady=(15, 5))


    lbl_fixed_car_title = ctk.CTkLabel(
        top_container,
        text='🚗 Vehicle Preview',
        font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold")
    )
    lbl_fixed_car_title.pack(pady=(0, 5), anchor="w")

    image_display_box = ctk.CTkFrame(top_container, width=340, height=180, fg_color=("#dbdbdb", "#212121"))
    image_display_box.pack(pady=5)
    image_display_box.pack_propagate(False)

    global image_preview_label

    image_preview_label = ctk.CTkLabel(image_display_box, text='No Vehicle Selected', text_color='gray',font=ctk.CTkFont(family="Segoe UI", size=13))
    image_preview_label.place(relx=0.5, rely=0.5, anchor="center")
    image_preview_label.configure(width=340, height=180)


    dynamic_info_frame = ctk.CTkScrollableFrame(right_frame, fg_color="transparent", label_text="")
    dynamic_info_frame.pack(side="top", fill="both", expand=True, pady=(5, 0), padx=15)

    # UPDATE BUTTON
    btn_update = ctk.CTkButton(
        buttons_row_frame,
        text="✏️ Edit Details",
        font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
        fg_color=("#2980b9", "#1f618d"),
        hover_color=("#1f618d", "#1a5276"),
        width=150,
        height=40,
        command=lambda: open_update_window(vehicle_table)
    )
    btn_update.pack(side="left", padx=(0, 5), expand=True, fill="x")

    # DELETE BUTTON
    btn_delete = ctk.CTkButton(
        buttons_row_frame,
        text="❌ Delete Vehicle Record",
        font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
        fg_color=("#c0392b", "#962d22"),
        hover_color=("#962d22", "#7b241c"),
        width=150,
        height=40,
        command=lambda: delete_vehicle(vehicle_table, image_preview_label, dynamic_info_frame, lbl_fixed_car_title)
    )
    btn_delete.pack(side="right", padx=(5, 0), expand=True, fill="x")


    vehicle_table.bind(
        "<<TreeviewSelect>>",
        lambda event: on_vehicle_select(event, vehicle_table, image_preview_label, dynamic_info_frame,
                                        lbl_fixed_car_title)
    )

    load_table_data(vehicle_table)






def on_vehicle_select(event, table_widget, dummy_label, info_container, fixed_title_label):
    global image_preview_label

    selected_item = table_widget.selection()
    if not selected_item:
        return

    item_data = table_widget.item(selected_item[0], 'values')

    v_id = item_data[0]
    brand = item_data[1]
    model = item_data[2]
    year = item_data[3]
    mileage = item_data[4]
    price = item_data[5]
    status = item_data[6]

    image_path = 'no_image.png'
    fuel_type = "N/A"
    engine_cc = "N/A"
    transmission = "N/A"
    active_features = []

    try:
        conn = mysql.connector.connect(
            host='localhost', user='root', password='', database='showroom_db'
        )
        cursor = conn.cursor()
        cursor.execute(
            """SELECT image_path, leather_seats, sunroof, push_start, alloy_wheels, reverse_camera, 
                      fuel_type, engine_cc, transmission 
               FROM vehicles WHERE vehicle_id = %s""", (v_id,))
        result = cursor.fetchone()

        if result:
            image_path = result[0] if result[0] else 'no_image.png'
            if result[1] and result[1].strip().lower() == "yes": active_features.append("Leather")
            if result[2] and result[2].strip().lower() == "yes": active_features.append("Sunroof")
            if result[3] and result[3].strip().lower() == "yes": active_features.append("Push Start")
            if result[4] and result[4].strip().lower() == "yes": active_features.append("Alloys")
            if result[5] and result[5].strip().lower() == "yes": active_features.append("Reverse Cam")
            fuel_type = result[6] if result[6] else "N/A"
            engine_cc = result[7] if result[7] else "N/A"
            transmission = result[8] if result[8] else "N/A"

        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Database image/info fetch error: {err}")

    fixed_title_label.configure(text=f"🚗 {brand} {model} ({year})", text_color=("#1a252f", "#ffffff"))

    for widget in info_container.winfo_children():
        widget.destroy()

    spec_table = ctk.CTkFrame(info_container, fg_color=("#f0f0f0", "#2b2b2b"), corner_radius=6)
    spec_table.pack(fill="x", pady=5, expand=False)
    spec_table.columnconfigure(0, weight=1)
    spec_table.columnconfigure(1, weight=2)

    def create_row(label_txt, value_txt, row_num, val_color=None):
        ctk.CTkLabel(spec_table, text=label_txt, font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),text_color=("#555555", "#aaaaaa")).grid(row=row_num, column=0, sticky="w", padx=15, pady=6)
        ctk.CTkLabel(spec_table, text=value_txt, font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),text_color=val_color if val_color else ("#1a252f", "#ffffff")).grid(row=row_num, column=1,sticky="w", padx=15, pady=6)

    create_row("📍 Mileage", f":  {mileage} km", 0)
    create_row("💰 Price", f":  Rs. {price}", 1)
    create_row("⛽ Fuel Type", f":  {fuel_type}", 2)
    create_row("⚙️ Displacement", f":  {engine_cc} CC", 3)
    create_row("🕹 Transmission", f":  {transmission}", 4)

    status_color = "#27ae60" if status.lower() == "available" else "#c0392b"
    create_row("📌 Status", f":  {status}", 5, val_color=status_color)

    if active_features:
        lbl_f_title = ctk.CTkLabel(info_container, text="✨ Premium Features Included:",font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"))
        lbl_f_title.pack(anchor="w", pady=(12, 5))
        feat_box = ctk.CTkFrame(info_container, fg_color="transparent")
        feat_box.pack(fill="x", expand=False, pady=2)
        for feat in active_features:
            badge = ctk.CTkLabel(feat_box, text=f"✓ {feat}",font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),fg_color=("#e0e0e0", "#2c3e50"), text_color=("#2c3e50", "#ffffff"), corner_radius=4,padx=8, height=24)
            badge.pack(side="left", padx=3)
    else:
        lbl_no_f = ctk.CTkLabel(info_container, text="ℹ️ No custom features selected.",font=ctk.CTkFont(family="Segoe UI", size=12, slant="italic"), text_color="gray")
        lbl_no_f.pack(anchor="w", pady=(10, 0))


    current_mode = ctk.get_appearance_mode()
    bg_pad_color = "#dbdbdb" if current_mode == "Light" else "#212121"


    if 'image_preview_label' in globals() and image_preview_label.winfo_exists():

        parent_frame = image_preview_label.master
        image_preview_label.destroy()
    else:

        parent_frame = dummy_label.master


    image_preview_label = ctk.CTkLabel(parent_frame, text="")
    image_preview_label.place(relx=0.5, rely=0.5, anchor="center")


    final_img_path = image_path if os.path.exists(image_path) else 'no_image.png'


    try:
        if os.path.exists(final_img_path):
            img = Image.open(final_img_path)
            padded_img = ImageOps.pad(img, (340, 180), color=bg_pad_color)
            img_ctk = ctk.CTkImage(light_image=padded_img, dark_image=padded_img, size=(340, 180))
            image_preview_label.configure(image=img_ctk, text="", fg_color=bg_pad_color)


            image_preview_label.image = img_ctk

        else:
            image_preview_label.configure(text="Image Not Found")
    except Exception as e:
        print(f"[IMAGE LOAD ERROR RESOLVED]: {str(e)}")
        image_preview_label.configure(text="Error Loading Image")




def delete_vehicle(table_widget, image_label, info_container, fixed_title_label):
    selected_item = table_widget.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "Select a vehicle to delete!")
        return

    item_data = table_widget.item(selected_item[0], 'values')
    v_id = item_data[0]
    brand = item_data[1]
    model = item_data[2]


    confirm = messagebox.askyesno("Confirm Delete", f"Are you sure? {brand} {model} (ID: {v_id}) record will be deleted !!!")
    if confirm:
        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='showroom_db'
            )
            cursor = conn.cursor()
            cursor.execute("DELETE FROM vehicles WHERE vehicle_id = %s", (v_id,))
            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo("Success", "🎯 Vehicle record deleted successfully!")
            load_table_data(table_widget)


            fixed_title_label.configure(text="Select a vehicle to view details", text_color="gray")


            for widget in info_container.winfo_children():
                widget.destroy()

            image_label.configure(image=None, text='No Vehicle Selected')
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")


def open_update_window(table_widget):
    selected_item = table_widget.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "Select a vehicle to update!")
        return

    item_data = table_widget.item(selected_item[0], 'values')
    v_id = item_data[0]


    current_features = ["No", "No", "No", "No", "No"]
    try:
        conn = mysql.connector.connect(host='localhost', user='root', password='', database='showroom_db')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT leather_seats, sunroof, push_start, alloy_wheels, reverse_camera FROM vehicles WHERE vehicle_id = %s",
            (v_id,))
        res = cursor.fetchone()
        if res:
            current_features = [res[0], res[1], res[2], res[3], res[4]]
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error fetching current features: {e}")


    update_win = ctk.CTkToplevel()
    update_win.title("✏️ Update Vehicle Details")
    update_win.geometry("520x520")
    update_win.grab_set()

    ctk.CTkLabel(update_win, text="✏️ EDIT VEHICLE DETAILS & OPTIONS", font=ctk.CTkFont(size=16, weight="bold")).pack(
        pady=10)

    #TEXT FIELDS SECTION (Brand, Model, etc.)
    f_frame = ctk.CTkFrame(update_win, fg_color="transparent")
    f_frame.pack(padx=20, pady=5, fill="x")

    fields = ["Brand", "Model", "Year", "Mileage", "Price"]
    entries = {}

    for idx, field in enumerate(fields):
        ctk.CTkLabel(f_frame, text=f"{field} :", font=ctk.CTkFont(size=13)).grid(row=idx, column=0, sticky="w", pady=6,padx=10)
        entry = ctk.CTkEntry(f_frame, width=220)
        entry.grid(row=idx, column=1, pady=6, padx=10, sticky="w")
        entry.insert(0, item_data[idx + 1])
        entries[field.lower()] = entry

    #CHECKBOXES SECTION
    features_up_frame = ctk.CTkFrame(update_win, fg_color=("#dbdbdb", "#212121"))
    features_up_frame.pack(padx=30, pady=10, fill="x")

    ctk.CTkLabel(features_up_frame, text="⚙️ Edit Key Options:", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=15, pady=5)


    var_leather = ctk.StringVar(value=current_features[0])
    var_sunroof = ctk.StringVar(value=current_features[1])
    var_push = ctk.StringVar(value=current_features[2])
    var_alloy = ctk.StringVar(value=current_features[3])
    var_cam = ctk.StringVar(value=current_features[4])

    cb_grid = ctk.CTkFrame(features_up_frame, fg_color="transparent")
    cb_grid.pack(padx=15, pady=5, fill="x")

    ctk.CTkCheckBox(cb_grid, text="Leather Seats", font=ctk.CTkFont(size=12), variable=var_leather, onvalue="Yes",offvalue="No").grid(row=0, column=0, sticky="w", pady=6, padx=10)
    ctk.CTkCheckBox(cb_grid, text="Sunroof", font=ctk.CTkFont(size=12), variable=var_sunroof, onvalue="Yes",offvalue="No").grid(row=0, column=1, sticky="w", pady=6, padx=10)
    ctk.CTkCheckBox(cb_grid, text="Push Start", font=ctk.CTkFont(size=12), variable=var_push, onvalue="Yes",offvalue="No").grid(row=0, column=2, sticky="w", pady=6, padx=10)
    ctk.CTkCheckBox(cb_grid, text="Alloy Wheels", font=ctk.CTkFont(size=12), variable=var_alloy, onvalue="Yes",offvalue="No").grid(row=1, column=0, sticky="w", pady=6, padx=10)
    ctk.CTkCheckBox(cb_grid, text="Reverse Cam", font=ctk.CTkFont(size=12), variable=var_cam, onvalue="Yes",offvalue="No").grid(row=1, column=1, sticky="w", pady=6, padx=10)


    #SAVE LOGIC
    def save_updates():
        try:
            conn = mysql.connector.connect(host='localhost', user='root', password='', database='showroom_db')
            cursor = conn.cursor()


            q = """UPDATE vehicles 
                   SET brand=%s, model=%s, manufacture_year=%s, mileage=%s, price=%s,
                       leather_seats=%s, sunroof=%s, push_start=%s, alloy_wheels=%s, reverse_camera=%s 
                   WHERE vehicle_id=%s"""

            val = (
                entries['brand'].get().strip(),
                entries['model'].get().strip(),
                entries['year'].get().strip(),
                entries['mileage'].get().strip(),
                entries['price'].get().strip(),
                var_leather.get(),
                var_sunroof.get(),
                var_push.get(),
                var_alloy.get(),
                var_cam.get(),
                v_id
            )

            cursor.execute(q, val)
            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo("Success", "🎯 Vehicle details & features updated successfully!")
            update_win.destroy()
            load_table_data(table_widget)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Update failed: {err}")

    ctk.CTkButton(update_win, text="💾 Save Changes", fg_color="#26a65b", hover_color="#1e824c", width=220, height=38,
                  command=save_updates).pack(pady=15)


footer_frame = ctk.CTkFrame(
    app,
    fg_color=("#e0e0e0", "#1a1a1a"),
    height=30,
    corner_radius=0
)
footer_frame.pack(side="bottom", fill="x")
footer_frame.pack_propagate(False)


footer_lbl = ctk.CTkLabel(
    footer_frame,
    text="⚙️ Connected to Database: showroom_db  |  System Status: Operational",
    font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
    text_color=("#555555", "#b0b0b0")
)
footer_lbl.pack(side="left", padx=20, pady=3)


version_lbl = ctk.CTkLabel(
    footer_frame,
    text="🚀 v1.0.0 Stable",
    font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
    text_color=("#555555", "#b0b0b0")
)
version_lbl.pack(side="right", padx=20, pady=3)

selected_image_path = ""


def browse_image(label_widget, preview_label_widget):
    global selected_image_path

    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.jpg *.jpeg *.png")]
    )
    if file_path:
        selected_image_path = file_path

        file_name = os.path.basename(file_path)
        label_widget.configure(text=f"Selected: {file_name}", text_color="green")

        try:
            from PIL import ImageOps
            img = Image.open(file_path)

            padded_img = ImageOps.pad(img, (320, 200),
                                      color=("#f0f0f0" if ctk.get_appearance_mode() == "Light" else "#2b2b2b"))
            img_ctk = ctk.CTkImage(light_image=padded_img, dark_image=padded_img, size=(320, 200))
            preview_label_widget.configure(image=img_ctk, text="")
            preview_label_widget.image = img_ctk

        except Exception as e:
            print(f"Form image preview error: {e}")






#####ADD VEHICLE SETUP


def save_vehicle_data(e_brand, e_model, e_year, e_mileage, e_price, v_table, label_widget, v_leather, v_sunroof, v_push, v_alloy, v_cam, fuel_combo, entry_cc, trans_combo):
    global selected_image_path

    brand = e_brand.get().strip()
    model = e_model.get().strip()
    year = e_year.get().strip()
    mileage = e_mileage.get().strip()
    price = e_price.get().strip()
    leather = v_leather.get()
    sunroof = v_sunroof.get()
    push_start = v_push.get()
    alloy = v_alloy.get()
    camera = v_cam.get()
    fuel = fuel_combo.get()
    cc = entry_cc.get()
    trans = trans_combo.get()

    if not brand or not model or not year or not mileage or not price or not selected_image_path:
        messagebox.showwarning("Warning", "All the fields must be filled !!!")
        return


    final_image_path = "no_image.png"

    if selected_image_path:

        filename = os.path.basename(selected_image_path)
        final_image_path = f"cars/{filename}".lower()

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="showroom_db"
        )
        cursor = conn.cursor()

        query = """INSERT INTO vehicles 
                       (brand, model, manufacture_year, mileage, price, status, image_path, 
                        leather_seats, sunroof, push_start, alloy_wheels, reverse_camera,
                        fuel_type, engine_cc, transmission) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""


        values = (
            brand,
            model,
            int(year),
            int(mileage),
            float(price),
            'Available',
            final_image_path,
            leather,
            sunroof,
            push_start,
            alloy,
            camera,
            fuel,
            entry_cc.get(),
            trans
        )

        cursor.execute(query, values)
        conn.commit()

        cursor.close()
        conn.close()

        messagebox.showinfo("Success", "🎯 Vehicle Data inserted successfully !!!")


        e_brand.delete(0, 'end')
        e_model.delete(0, 'end')
        e_year.delete(0, 'end')
        e_mileage.delete(0, 'end')
        e_price.delete(0, 'end')
        label_widget.configure(text="No file chosen", text_color="gray")
        selected_image_path = ""


        if 'form_preview_label' in globals() or 'form_preview_label' in locals():
            try:
                form_preview_label.configure(image=None, text="No Vehicle Image Selected")
                form_preview_label.image = None
            except:
                pass

        load_table_data(v_table)

    except ValueError:
        messagebox.showerror("Error", "Year, Mileage, and Price must contain only numbers!!!")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")


form_preview_label = None



def setup_add_vehicle_tab():
    global form_preview_label

    form_frame = ctk.CTkFrame(tabview.tab("Add New Vehicle"), fg_color='transparent')
    form_frame.pack(fill='both', expand=True, padx=40, pady=20)
    title_label = ctk.CTkLabel(
        form_frame,
        text="➕ ENTER NEW VEHICLE DETAILS",

        font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
        text_color=("#1f538d", "#64b5f6")
    )
    title_label.pack(pady=(10, 20), anchor="w")

    grid_frame = ctk.CTkFrame(form_frame, width=1150, height=320)
    grid_frame.pack(fill="x", pady=10)
    grid_frame.pack_propagate(False)

    #Three Columns
    grid_frame.columnconfigure(0, weight=1)
    grid_frame.columnconfigure(1, weight=1)
    grid_frame.columnconfigure(2, weight=1)

    #COLUMN 0

    left_fields_frame = ctk.CTkFrame(grid_frame, fg_color="transparent")
    left_fields_frame.grid(row=0, column=0, rowspan=5, padx=15, pady=15, sticky="nsew")

    # Brand
    lbl_brand = ctk.CTkLabel(left_fields_frame, text='Brand : ', font=ctk.CTkFont(size=14))
    lbl_brand.grid(row=0, column=0, sticky='w', pady=8, padx=10)
    entry_brand = ctk.CTkEntry(left_fields_frame, width=220, placeholder_text='e.g., Toyota')
    entry_brand.grid(row=0, column=1, pady=8, padx=10, sticky='w')

    # Model
    lbl_model = ctk.CTkLabel(left_fields_frame, text='Model : ', font=ctk.CTkFont(size=14))
    lbl_model.grid(row=1, column=0, sticky='w', pady=8, padx=10)
    entry_model = ctk.CTkEntry(left_fields_frame, width=220, placeholder_text='e.g., Prius')
    entry_model.grid(row=1, column=1, pady=8, padx=10, sticky='w')

    # Manufacture Year
    lbl_year = ctk.CTkLabel(left_fields_frame, text='Manufacture Year : ', font=ctk.CTkFont(size=14))
    lbl_year.grid(row=2, column=0, sticky='w', pady=8, padx=10)
    entry_year = ctk.CTkEntry(left_fields_frame, width=220, placeholder_text='e.g., 2018')
    entry_year.grid(row=2, column=1, pady=8, padx=10, sticky='w')

    # Mileage
    lbl_mileage = ctk.CTkLabel(left_fields_frame, text='Mileage : ', font=ctk.CTkFont(size=14))
    lbl_mileage.grid(row=3, column=0, sticky='w', pady=8, padx=10)
    entry_mileage = ctk.CTkEntry(left_fields_frame, width=220, placeholder_text='e.g., 45000')
    entry_mileage.grid(row=3, column=1, pady=8, padx=10, sticky='w')

    # Price
    lbl_price = ctk.CTkLabel(left_fields_frame, text='Price : ', font=ctk.CTkFont(size=14))
    lbl_price.grid(row=4, column=0, sticky='w', pady=8, padx=10)
    entry_price = ctk.CTkEntry(left_fields_frame, width=220, placeholder_text='e.g., 7200000')
    entry_price.grid(row=4, column=1, pady=8, padx=10, sticky='w')




    lbl_fuel = ctk.CTkLabel(left_fields_frame, text="Fuel Type :",font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"))
    lbl_fuel.grid(row=5, column=0, sticky='w', pady=8, padx=10)
    fuel_combo = ctk.CTkComboBox(left_fields_frame, values=["Petrol", "Hybrid", "Diesel", "Electric"],font=ctk.CTkFont(family="Segoe UI", size=12), width=220)
    fuel_combo.grid(row=5, column=1, pady=8, padx=10, sticky='w')


    lbl_cc = ctk.CTkLabel(left_fields_frame, text="Engine Capacity (CC) :",font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"))
    lbl_cc.grid(row=6, column=0, sticky='w', pady=8, padx=10)
    entry_cc = ctk.CTkEntry(left_fields_frame, width=220, placeholder_text="e.g., 1500")
    entry_cc.grid(row=6, column=1, pady=8, padx=10, sticky='w')


    lbl_trans = ctk.CTkLabel(left_fields_frame, text="Transmission :",font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"))
    lbl_trans.grid(row=7, column=0, sticky='w', pady=8, padx=10)
    trans_combo = ctk.CTkComboBox(left_fields_frame, values=["Automatic", "Manual", "Tiptronic"],font=ctk.CTkFont(family="Segoe UI", size=12), width=220)
    trans_combo.grid(row=7, column=1, pady=8, padx=10, sticky='w')

    #COLUMN 1
    features_frame = ctk.CTkFrame(grid_frame, fg_color="transparent")
    features_frame.grid(row=0, column=1, rowspan=5, padx=20, pady=15, sticky="nsew")

    ctk.CTkLabel(features_frame, text="⚙️ Vehicle Key Options", font=ctk.CTkFont(size=14, weight="bold"),text_color=("#1f538d", "#64b5f6")).pack(anchor="w", pady=(0, 8))

    var_leather = ctk.StringVar(value="No")
    var_sunroof = ctk.StringVar(value="No")
    var_push = ctk.StringVar(value="No")
    var_alloy = ctk.StringVar(value="No")
    var_cam = ctk.StringVar(value="No")


    ctk.CTkCheckBox(features_frame, text="Leather Seats", font=ctk.CTkFont(size=12), variable=var_leather,onvalue="Yes", offvalue="No").pack(anchor="w", pady=4)
    ctk.CTkCheckBox(features_frame, text="Sunroof / Moonroof", font=ctk.CTkFont(size=12), variable=var_sunroof,onvalue="Yes", offvalue="No").pack(anchor="w", pady=4)
    ctk.CTkCheckBox(features_frame, text="Push Start / Smart Key", font=ctk.CTkFont(size=12), variable=var_push,onvalue="Yes", offvalue="No").pack(anchor="w", pady=4)
    ctk.CTkCheckBox(features_frame, text="Alloy Wheels", font=ctk.CTkFont(size=12), variable=var_alloy, onvalue="Yes",offvalue="No").pack(anchor="w", pady=4)
    ctk.CTkCheckBox(features_frame, text="Reverse Camera", font=ctk.CTkFont(size=12), variable=var_cam, onvalue="Yes",offvalue="No").pack(anchor="w", pady=4)


    #COLUMN 2
    right_preview_frame = ctk.CTkFrame(grid_frame, width=400, fg_color=("#dbdbdb", "#212121"))
    right_preview_frame.grid(row=0, column=2, rowspan=5, padx=15, pady=15, sticky="nsew")
    right_preview_frame.pack_propagate(True)

    ctk.CTkLabel(right_preview_frame, text='📸 Vehicle Image Preview', font=ctk.CTkFont(size=13, weight="bold")).pack(pady=(10, 2))

    image_display_box = ctk.CTkFrame(right_preview_frame, width=320, height=160, fg_color=("#f0f0f0", "#2b2b2b"))
    image_display_box.pack(pady=5, padx=15)
    image_display_box.pack_propagate(False)

    form_preview_label = ctk.CTkLabel(image_display_box, text='No Image Selected', text_color='gray')
    form_preview_label.place(relx=0.5, rely=0.5, anchor="center")

    lbl_file_status = ctk.CTkLabel(right_preview_frame, text="No file chosen", text_color="gray", font=ctk.CTkFont(size=11))
    lbl_file_status.pack(pady=2)

    btn_browse = ctk.CTkButton(
        right_preview_frame,
        text="📁 Choose Image",
        width=140,
        height=28,
        fg_color="#5c6bc0",
        hover_color="#3f51b5",
        command=lambda: browse_image(lbl_file_status, form_preview_label)
    )
    btn_browse.pack(pady=(2, 8))


    btn_save = ctk.CTkButton(
        form_frame,
        text="💾 Save Vehicle to Database",
        font=ctk.CTkFont(family="Segoe UI", size=15, weight='bold'),
        fg_color="#26a65b",
        hover_color="#1e824c",
        width=350,
        height=42,

        command=lambda: save_vehicle_data(
            entry_brand, entry_model, entry_year, entry_mileage, entry_price,
            vehicle_table, lbl_file_status,
            var_leather, var_sunroof, var_push, var_alloy, var_cam,
            fuel_combo, entry_cc, trans_combo
        )
    )
    btn_save.pack(pady=(25, 10))












###########SALES SETUP

import re
from datetime import date


def validate_srilankan_phone(phone_str):
    # cheks 3 formats 0771234567, 771234567, +94771234567
    phone_pattern = r"^(?:\+94|0)?7[0-1,2,4-8]\d{7}$"
    return bool(re.match(phone_pattern, phone_str.strip()))

def validate_srilankan_nic(nic_str):
    nic_str = nic_str.strip().upper()
    old_nic_pattern = r"^\d{9}[VX]$"    # OLD with 9 numbers and letter V
    new_nic_pattern = r"^\d{12}$"       # New 12 Numbers
    return bool(re.match(old_nic_pattern, nic_str) or re.match(new_nic_pattern, nic_str))



def confirm_sale(ent_v_id, ent_name, ent_phone, ent_nic, ent_sell_price, cmb_pay_method, cmb_leasing_co, ent_advance, bill_preview, vehicle_table):
    v_id = ent_v_id.get().strip()
    cust_name = ent_name.get().strip()
    cust_phone = ent_phone.get().strip()
    cust_nic = ent_nic.get().strip()

    pay_method = cmb_pay_method.get()
    leasing_company = cmb_leasing_co.get()


    if not v_id or not cust_name or not cust_phone or not cust_nic or not ent_sell_price.get().strip():
        messagebox.showwarning("Warning", "All required fields must be filled !!!")
        return

    # Phone Number Validation
    if not validate_srilankan_phone(cust_phone):
        messagebox.showerror("Input Error", "⚠️ Please enter a valid Sri Lankan Phone Number!\n(e.g., 0771234567 or +94771234567)")
        return

    #NIC Number Validation
    if not validate_srilankan_nic(cust_nic):
        messagebox.showerror("Input Error", "⚠️ Please enter a valid Sri Lankan NIC Number!\n(e.g., 123456789V or 200012345678)")
        return


    try:
        actual_selling_price = float(ent_sell_price.get().strip())
        advance_paid = float(ent_advance.get().strip()) if ent_advance.get().strip() else 0.0
    except ValueError:
        messagebox.showerror("Input Error", "Price and Advance must be valid numbers!")
        return

    balance_due = actual_selling_price - advance_paid

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="showroom_db"
        )
        cursor = conn.cursor()

        cursor.execute("SELECT brand, model, status FROM vehicles WHERE vehicle_id = %s", (v_id,))
        vehicle = cursor.fetchone()

        if not vehicle:
            messagebox.showerror("Error", "There is no such vehicle ID in the database !!!")
            cursor.close()
            conn.close()
            return
        elif vehicle[2] == 'Sold':
            messagebox.showwarning("Warning", "This vehicle is already sold !!!")
            cursor.close()
            conn.close()
            return

        v_brand, v_model = vehicle[0], vehicle[1]

        cursor.execute("UPDATE vehicles SET status = 'Sold' WHERE vehicle_id = %s", (v_id,))

        today_date = date.today().strftime('%Y-%m-%d')

        history_query = """
                    INSERT INTO sales_history (customer_name, customer_phone, customer_nic, vehicle_id, sale_date, final_price, payment_mode)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """

        history_values = (cust_name, cust_phone, cust_nic.upper(), v_id, today_date, actual_selling_price, pay_method)
        cursor.execute(history_query, history_values)

        generated_sale_id = cursor.lastrowid

        conn.commit()
        cursor.close()
        conn.close()

        # --- TEXT PREVIEW GENERATION ---
        bill_preview.configure(state="normal")
        bill_preview.delete("1.0", "end")

        invoice_template = f"""
==================================================
             DRIVE CRAFT MOTOR INVOICE            
==================================================
 Invoice / Sale ID: {generated_sale_id}
 Customer Name  : {cust_name}
 Phone Number   : {cust_phone}
 NIC Number     : {cust_nic.upper()}
 -------------------------------------------------
 VEHICLE DETAILS:
 Vehicle ID     : {v_id}
 Brand & Model  : {v_brand} {v_model}
 -------------------------------------------------
 FINANCIAL SUMMARY:
 Final Price    : Rs. {actual_selling_price:,.2f}
 Payment Method : {pay_method}
 Leasing Co     : {leasing_company if pay_method == "Leasing / Finance" else "N/A"}
 Advance Paid   : Rs. {advance_paid:,.2f}
 -------------------------------------------------
 TOTAL DUE      : Rs. {balance_due:,.2f}
 =================================================
 STATUS         : PAID & COMPLETED ✅
 =================================================
 Thank you for doing business with us!
        """
        bill_preview.insert("1.0", invoice_template)
        bill_preview.configure(state="disabled")

        if not os.path.exists("invoices"):
            os.makedirs("invoices")

        clean_cust_name = cust_name.lower().replace(' ', '_')
        pdf_filename = f"invoices/invoice_{v_id}_{clean_cust_name}.pdf"

        # --- REPORTLAB PDF GENERATION ---
        doc = SimpleDocTemplate(pdf_filename, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
        story = []
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=22, leading=26, textColor=colors.HexColor("#1f538d"), alignment=1)
        sub_style = ParagraphStyle('SubStyle', parent=styles['Normal'], fontSize=10, leading=14, textColor=colors.gray, alignment=1)
        section_style = ParagraphStyle('SectionStyle', parent=styles['Heading2'], fontSize=14, leading=18, textColor=colors.HexColor("#2b2b2b"), spaceBefore=12, spaceAfter=8)
        text_style = ParagraphStyle('TextStyle', parent=styles['Normal'], fontSize=11, leading=16, textColor=colors.HexColor("#333333"))
        header_text_style = ParagraphStyle('HeaderTextStyle', parent=styles['Normal'], fontSize=11, leading=16, textColor=colors.white, fontName="Helvetica-Bold")

        story.append(Paragraph("<b>DRIVE CRAFT SHOWROOM</b>", title_style))
        story.append(Paragraph(f"Official Customer Transaction Receipt / Invoice # {generated_sale_id}", sub_style))
        story.append(Spacer(1, 20))

        story.append(Paragraph("<b>Customer Details</b>", section_style))
        cust_data = [
            [Paragraph("<b>Customer Name:</b>", text_style), Paragraph(cust_name, text_style)],
            [Paragraph("<b>Phone Number:</b>", text_style), Paragraph(cust_phone, text_style)],
            [Paragraph("<b>NIC Number:</b>", text_style), Paragraph(cust_nic.upper(), text_style)]
        ]
        t_cust = Table(cust_data, colWidths=[130, 370])
        t_cust.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f9f9f9")),
            ('PADDING', (0, 0), (-1, -1), 6),
            ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.HexColor("#e0e0e0")),
        ]))
        story.append(t_cust)
        story.append(Spacer(1, 15))

        story.append(Paragraph("<b>Vehicle & Transaction Details</b>", section_style))
        veh_data = [
            [Paragraph("Item Description", header_text_style), Paragraph("Details", header_text_style)],
            [Paragraph("Vehicle ID", text_style), Paragraph(str(v_id), text_style)],
            [Paragraph("Brand & Model", text_style), Paragraph(f"{v_brand} {v_model}", text_style)],
            [Paragraph("Payment Framework", text_style), Paragraph(
                f"Method: {pay_method} | Leasing: {leasing_company if pay_method == 'Leasing / Finance' else 'N/A'}",
                text_style)],
            [Paragraph("Agreed Selling Price", text_style), Paragraph(f"Rs. {actual_selling_price:,.2f}", text_style)],
            [Paragraph("Advance Commitment", text_style), Paragraph(f"- Rs. {advance_paid:,.2f}", text_style)],
            [Paragraph("<b>Total Due Balance</b>", text_style), Paragraph(f"<b>Rs. {balance_due:,.2f}</b>", text_style)]
        ]

        t_veh = Table(veh_data, colWidths=[160, 340])
        t_veh.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (1, 0), colors.HexColor("#1f538d")),
            ('PADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#dddddd")),
            ('BACKGROUND', (0, -1), (1, -1), colors.HexColor("#e8f5e9")),
        ]))
        story.append(t_veh)
        story.append(Spacer(1, 35))

        footer_style = ParagraphStyle('FooterStyle', parent=styles['Normal'], fontSize=11, textColor=colors.HexColor("#2e7d32"), alignment=1)
        story.append(Paragraph("<b>✔ STATUS: PAID & COMPLETED</b>", footer_style))
        story.append(Spacer(1, 10))
        story.append(Paragraph("Thank you for doing business with us! Come again.", sub_style))

        doc.build(story)

        messagebox.showinfo("Success", f"🎯 Invoice generated successfully!\n\nPDF saved at: {pdf_filename}")
        bill_preview.configure(state="normal")
        bill_preview.delete("1.0", "end")
        bill_preview.insert("1.0", "\n\n\n\tNo Active Invoice Preview Available.")
        bill_preview.configure(state="disabled")

        load_table_data(vehicle_table)

        if 'load_sales_history_data' in globals():
            load_sales_history_data()


        ent_v_id.delete(0, 'end')
        ent_name.delete(0, 'end')
        ent_phone.delete(0, 'end')
        ent_nic.delete(0, 'end')
        ent_sell_price.delete(0, 'end')
        ent_advance.delete(0, 'end')

        if 'trigger_analytics_refresh' in globals():
            trigger_analytics_refresh()

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")




def setup_sales_tab():
    sales_main_frame = ctk.CTkFrame(tabview.tab("Sales & Billing"), fg_color='transparent')
    sales_main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    left_form = ctk.CTkFrame(sales_main_frame, width=650)
    left_form.pack(side="left", fill="both", expand=True, padx=5, pady=5)

    lbl_title = ctk.CTkLabel(
        left_form,
        text="📝 BILLING & CUSTOMER MANAGEMENT",
        font=ctk.CTkFont(family="Segoe UI", size=15, weight='bold'),
        text_color=("#1f538d", "#64b5f6")
    )
    lbl_title.pack(pady=(20, 10), anchor="w", padx=30)

    grid_inside = ctk.CTkFrame(left_form, fg_color='transparent')
    grid_inside.pack(pady=5, padx=20, fill='x', expand=False)

    grid_inside.columnconfigure(0, weight=1)
    grid_inside.columnconfigure(1, weight=1)
    grid_inside.columnconfigure(2, weight=1)
    grid_inside.columnconfigure(3, weight=1)

    # Row 0: Vehicle ID & Price
    ctk.CTkLabel(grid_inside, text="Vehicle ID to Sell :", font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold")).grid(row=0, column=0, sticky='w', pady=8, padx=10)
    ent_v_id = ctk.CTkEntry(grid_inside, width=200, placeholder_text='e.g., 1', font=ctk.CTkFont(family="Segoe UI", size=12))
    ent_v_id.grid(row=0, column=1, pady=8, padx=10, sticky='w')

    ctk.CTkLabel(grid_inside, text="Final Price (Rs.) :", font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold")).grid(row=0, column=2, sticky='w', pady=8, padx=10)
    ent_sell_price = ctk.CTkEntry(grid_inside, width=200, placeholder_text='e.g., 7150000', font=ctk.CTkFont(family="Segoe UI", size=12))
    ent_sell_price.grid(row=0, column=3, pady=8, padx=10, sticky='w')

    # Row 1: Customer Name & Payment Method
    ctk.CTkLabel(grid_inside, text="Customer Name :", font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold")).grid(row=1, column=0, sticky='w', pady=8, padx=10)
    ent_name = ctk.CTkEntry(grid_inside, width=200, placeholder_text='e.g., Kamal Perera', font=ctk.CTkFont(family="Segoe UI", size=12))
    ent_name.grid(row=1, column=1, pady=8, padx=10, sticky='w')

    ctk.CTkLabel(grid_inside, text="Payment Method :", font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold")).grid(row=1, column=2, sticky='w', pady=8, padx=10)
    cmb_pay_method = ctk.CTkComboBox(grid_inside, values=["Cash", "Bank Transfer", "Cheque", "Leasing / Finance"], width=200, font=ctk.CTkFont(family="Segoe UI", size=12))
    cmb_pay_method.grid(row=1, column=3, pady=8, padx=10, sticky='w')

    # Row 2: Phone Number & Leasing Co
    ctk.CTkLabel(grid_inside, text="Phone Number :", font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold")).grid(row=2, column=0, sticky='w', pady=8, padx=10)
    ent_phone = ctk.CTkEntry(grid_inside, width=200, placeholder_text='e.g., 0771234567', font=ctk.CTkFont(family="Segoe UI", size=12))
    ent_phone.grid(row=2, column=1, pady=8, padx=10, sticky='w')

    ctk.CTkLabel(grid_inside, text="Leasing Company :", font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold")).grid(row=2, column=2, sticky='w', pady=8, padx=10)
    cmb_leasing_co = ctk.CTkComboBox(grid_inside, values=["N/A", "LB Finance", "Peoples Leasing", "Commercial Bank", "HNB Finance", "LOLC"], width=200, font=ctk.CTkFont(family="Segoe UI", size=12))
    cmb_leasing_co.grid(row=2, column=3, pady=8, padx=10, sticky='w')

    # Row 3: NIC Number & Advance Paid
    ctk.CTkLabel(grid_inside, text="NIC Number :", font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold")).grid(row=3, column=0, sticky='w', pady=8, padx=10)
    ent_nic = ctk.CTkEntry(grid_inside, width=200, placeholder_text='e.g., 199912345V', font=ctk.CTkFont(family="Segoe UI", size=12))
    ent_nic.grid(row=3, column=1, pady=8, padx=10, sticky='w')

    ctk.CTkLabel(grid_inside, text="Advance Paid (Rs.) :", font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold")).grid(row=3, column=2, sticky='w', pady=8, padx=10)
    ent_advance = ctk.CTkEntry(grid_inside, width=200, placeholder_text='e.g., 500000 (0 if none)', font=ctk.CTkFont(family="Segoe UI", size=12))
    ent_advance.grid(row=3, column=3, pady=8, padx=10, sticky='w')



    summary_card = ctk.CTkFrame(
        left_form,
        fg_color=("#f1f5f9", "#1e293b"),
        corner_radius=12,
        border_width=1,
        border_color=("#cbd5e1", "#334155")
    )
    summary_card.pack(pady=(45, 15), padx=30, fill="x")

    lbl_sum_title = ctk.CTkLabel(
        summary_card,
        text="📊 Live Payment Breakdown (Real-time)",
        font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
        text_color=("#475569", "#94a3b8")
    )
    lbl_sum_title.pack(anchor="w", padx=15, pady=(10, 4))

    row_layout = ctk.CTkFrame(summary_card, fg_color="transparent")
    row_layout.pack(fill="x", padx=15, pady=(0, 15))
    row_layout.columnconfigure((0, 1, 2), weight=1)


    def create_calc_box(parent, title, val_color, col_idx):
        box = ctk.CTkFrame(parent, fg_color=("#ffffff", "#243347"), corner_radius=8, height=85)
        box.grid(row=0, column=col_idx, padx=6, sticky="nsew")
        box.pack_propagate(False)
        ctk.CTkLabel(box, text=title, font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"), text_color="gray").pack(pady=(10, 0))

        v_lbl = ctk.CTkLabel(box, text="Rs. 0.00", font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"), text_color=val_color)
        v_lbl.pack(pady=(4, 10))
        return v_lbl

    lbl_live_price = create_calc_box(row_layout, "Agreed Selling Price", ("#1f538d", "#64b5f6"), 0)
    lbl_live_advance = create_calc_box(row_layout, "Advance Commitment", ("#27ae60", "#2ecc71"), 1)
    lbl_live_due = create_calc_box(row_layout, "Total Due Balance", ("#c0392b", "#ff7675"), 2)

    # Real-time update logic
    def update_live_calculations(event=None):
        try:
            price = float(ent_sell_price.get().strip()) if ent_sell_price.get().strip() else 0.0
            lbl_live_price.configure(text=f"Rs. {price:,.2f}")
        except ValueError:
            lbl_live_price.configure(text="Invalid Price")
            price = 0.0

        try:
            advance = float(ent_advance.get().strip()) if ent_advance.get().strip() else 0.0
            lbl_live_advance.configure(text=f"Rs. {advance:,.2f}")
        except ValueError:
            lbl_live_advance.configure(text="Invalid Advance")
            advance = 0.0

        due = price - advance
        lbl_live_due.configure(text=f"Rs. {due:,.2f}")


    ent_sell_price.bind("<KeyRelease>", update_live_calculations)
    ent_advance.bind("<KeyRelease>", update_live_calculations)


    right_bill = ctk.CTkFrame(sales_main_frame, width=450, fg_color=("#1e1e1e", "#1a1a1a"))
    right_bill.pack(side='right', fill="both", padx=10, pady=10)

    lbl_bill_title = ctk.CTkLabel(right_bill, text="📄 INVOICE PREVIEW", font=ctk.CTkFont(family="Segoe UI", size=14, weight='bold'))
    lbl_bill_title.pack(pady=10)

    bill_preview = ctk.CTkTextbox(right_bill, width=400, height=380, font=ctk.CTkFont(family='Courier', size=12))
    bill_preview.pack(pady=10, padx=15)
    bill_preview.insert("1.0", "\n\n      No invoice generated yet.")
    bill_preview.configure(state="disabled")


    btn_sell = ctk.CTkButton(
        left_form,
        text="💰 Generate Invoice & Sell",
        font=ctk.CTkFont(family="Segoe UI", size=15, weight='bold'),
        fg_color="#26a65b",
        hover_color="#1e824c",
        width=320,
        height=46,
    )
    btn_sell.pack(pady=(35, 25))
    btn_sell.configure(command=lambda: confirm_sale(
            ent_v_id, ent_name, ent_phone, ent_nic,
            ent_sell_price, cmb_pay_method, cmb_leasing_co, ent_advance,
            bill_preview, vehicle_table
        ))








def load_table_data(table_widget, search_query="", status_filter='All'):
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='showroom_db'
        )
        cursor = conn.cursor()

        for item in table_widget.get_children():
            table_widget.delete(item)


        base_query = 'SELECT vehicle_id, brand, model, manufacture_year, mileage, price, status FROM vehicles WHERE 1=1'
        query_values = []


        if search_query:
            base_query += " AND (brand LIKE %s OR model LIKE %s)"
            query_values.extend([f"%{search_query}%", f"%{search_query}%"])

        if status_filter != "All":
            base_query += " AND status = %s"
            query_values.append(status_filter)

        cursor.execute(base_query, tuple(query_values))
        records = cursor.fetchall()

        for row in records:
            formatted_price = f"{row[5]:,.2f}"
            table_widget.insert("", "end", values=(row[0], row[1], row[2], row[3], row[4], formatted_price, row[6]))

        cursor.execute("SELECT COUNT(*) FROM vehicles")
        total_stock = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM vehicles WHERE status='Available'")
        available_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM vehicles WHERE status='Sold'")
        sold_count = cursor.fetchone()[0]

        cursor.execute("SELECT SUM(price) FROM vehicles WHERE status='Sold'")
        revenue_res = cursor.fetchone()[0]
        total_revenue = revenue_res if revenue_res else 0.0

        if lbl_total_stock:
            lbl_total_stock.configure(text=str(total_stock))
        if lbl_available:
            lbl_available.configure(text=str(available_count))
        if lbl_sold:
            lbl_sold.configure(text=str(sold_count))
        if lbl_total_revenue:
            lbl_total_revenue.configure(text=f"Rs. {total_revenue:,.2f}")

        global cards_frame

        # AUTOMATED LOW STOCK ALERT LOGIC
        if 'lbl_stock_alert' in globals() and lbl_stock_alert:
            if available_count < 2:

                lbl_stock_alert.configure(
                    text=f"⚠️ WARNING: LOW STOCK! Only {available_count} vehicle available for sale." if available_count == 1 else "⚠️ WARNING: OUT OF STOCK! No vehicles available for sale.",
                    fg_color=("#f9d5d5", "#5c1d1d"),
                    text_color=("#c0392b", "#ff9999")
                )
                lbl_stock_alert.pack(side="top", fill="x", padx=10, pady=(0, 10),before=cards_frame)
            else:

                lbl_stock_alert.pack_forget()


        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error updating inventory and analytics: {err}")





def filter_inventory_live(search_entry, filter_combo):
    query = search_entry.get().strip()
    status = filter_combo.get()
    load_table_data(vehicle_table, search_query=query, status_filter=status)


def setup_analytics_tab():
    analytics_tab = tabview.tab("Business Analytics")


    def refresh_analytics():

        for widget in analytics_tab.winfo_children():
            widget.destroy()

        plt.close('all')


        try:
            conn = mysql.connector.connect(host="localhost", user="root", password="", database="showroom_db")
            cursor = conn.cursor()

            cursor.execute("""
                SELECT v.brand, COUNT(*) AS count 
                FROM sales_history s
                INNER JOIN vehicles v ON s.vehicle_id = v.vehicle_id
                GROUP BY v.brand
            """)
            pie_data = cursor.fetchall()

            cursor.execute("""
                SELECT DATE_FORMAT(s.sale_date, '%Y-%m') AS month, SUM(s.final_price) AS monthly_revenue 
                FROM sales_history s
                GROUP BY month 
                ORDER BY month ASC
            """)
            line_data = cursor.fetchall()

            cursor.execute("SELECT COUNT(*), SUM(final_price), AVG(final_price) FROM sales_history")
            metrics_res = cursor.fetchone()

            total_sales = metrics_res[0] if metrics_res[0] else 0
            total_revenue = metrics_res[1] if metrics_res[1] else 0.0
            avg_sale_value = metrics_res[2] if metrics_res[2] else 0.0

            cursor.close()
            conn.close()

        except Exception as e:
            print(f"Analytics Data Fetch Error: {e}")
            pie_data = []
            line_data = []
            total_sales, total_revenue, avg_sale_value = 0, 0.0, 0.0


        top_metrics_container = ctk.CTkFrame(analytics_tab, fg_color="transparent")
        top_metrics_container.pack(side="top", fill="x", padx=15, pady=(15, 5))
        top_metrics_container.columnconfigure((0, 1, 2), weight=1)

        def create_metric_card(parent, title, value_txt, val_color, col_idx):
            card = ctk.CTkFrame(
                parent, fg_color=("#ffffff", "#1e293b"), corner_radius=10,
                border_width=1, border_color=("#e2e8f0", "#334155"), height=85
            )
            card.grid(row=0, column=col_idx, padx=6, sticky="nsew")
            card.pack_propagate(False)

            ctk.CTkLabel(card, text=title, font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
                         text_color=("#64748b", "#94a3b8")).pack(pady=(12, 2))
            ctk.CTkLabel(card, text=value_txt, font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
                         text_color=val_color).pack(pady=(2, 12))

        create_metric_card(top_metrics_container, "📈 Total Sales Transacted", str(total_sales), ("#3b82f6", "#93c5fd"),
                           0)
        create_metric_card(top_metrics_container, "💰 Gross Revenue Generated", f"Rs. {total_revenue:,.2f}",
                           ("#1f538d", "#64b5f6"), 1)
        create_metric_card(top_metrics_container, "📊 Average Value Per Sale", f"Rs. {avg_sale_value:,.2f}",
                           ("#0f172a", "#cbd5e1"), 2)

        # --- 3. CHARTS CONTAINER ---
        bottom_charts_container = ctk.CTkFrame(analytics_tab, fg_color="transparent")
        bottom_charts_container.pack(side="bottom", fill="both", expand=True, padx=15, pady=(5, 15))

        charts_card_frame = ctk.CTkFrame(
            bottom_charts_container, fg_color=("#ffffff", "#1e293b"),
            corner_radius=12, border_width=1, border_color=("#e2e8f0", "#334155")
        )
        charts_card_frame.pack(fill="both", expand=True)

        current_mode = ctk.get_appearance_mode()
        fig_bg = '#ffffff' if current_mode == "Light" else '#1e293b'
        text_color = '#334155' if current_mode == "Light" else '#cbd5e1'
        grid_color = '#f1f5f9' if current_mode == "Light" else '#334155'
        spine_color = '#e2e8f0' if current_mode == "Light" else '#475569'

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4.3), facecolor=fig_bg)
        fig.tight_layout(pad=4.5)

        # Pie Chart Logic
        if pie_data:
            brands = [x[0] for x in pie_data]
            counts = [x[1] for x in pie_data]
            chart_colors = ['#3b82f6', '#60a5fa', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6']
            ax1.pie(counts, labels=brands, autopct='%1.1f%%', startangle=140, colors=chart_colors,
                    textprops={'fontsize': 10, 'weight': 'bold', 'color': text_color})
            ax1.set_title("Top Selling Vehicle Brands", fontsize=12, weight='bold', pad=10, color=text_color)
            ax1.set_facecolor(fig_bg)
        else:
            ax1.text(0.5, 0.5, "No Real Sales Data Available!", ha='center', va='center', fontsize=11, color='#ef4444',
                     weight='bold')
            ax1.set_title("Top Selling Vehicle Brands", fontsize=12, weight='bold', pad=10, color=text_color)

        # Line Chart Logic
        if line_data:
            months = [x[0] for x in line_data]
            revenues = [float(x[1]) for x in line_data]
            ax2.set_facecolor(fig_bg)
            ax2.plot(months, revenues, marker='o', color='#3b82f6', linewidth=2, markersize=7)
            ax2.fill_between(months, revenues, color='#3b82f6', alpha=0.08)
            ax2.set_title("Monthly Revenue Growth (Rs.)", fontsize=12, weight='bold', pad=10, color=text_color)
            ax2.grid(True, linestyle='-', alpha=1, color=grid_color)
            ax2.tick_params(axis='x', rotation=15, colors=text_color, labelsize=9)
            ax2.tick_params(axis='y', colors=text_color, labelsize=9)
            ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
            for spine in ax2.spines.values():
                spine.set_color(spine_color)
                spine.set_linewidth(1)
        else:
            ax2.text(0.5, 0.5, "No Real Revenue Data Available!", ha='center', va='center', fontsize=11,
                     color='#ef4444', weight='bold')
            ax2.set_title("Monthly Revenue Growth (Rs.)", fontsize=12, weight='bold', pad=10, color=text_color)

        canvas = FigureCanvasTkAgg(fig, master=charts_card_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)



    refresh_analytics()



    global trigger_analytics_refresh
    trigger_analytics_refresh = refresh_analytics



setup_dashboard_tab()
setup_add_vehicle_tab()
setup_sales_tab()
setup_suppliers_tab()
setup_sales_history_tab()
setup_analytics_tab()


app.mainloop()



