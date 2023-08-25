import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from time import gmtime, strftime
from PIL import Image


# Check if input is numeric
def is_number(s):
    try:
        float(s)
        return 1
    except ValueError:
        return 0


# Check if Account number exits
def check_acc_nmb(num):
    try:
        fpin = open(num + ".txt", 'r')
    except FileNotFoundError:
        CTkMessagebox(title="Error", message="Invalid Credentials\nPlease try again.", icon="warning")
        return 0
    fpin.close()
    return


def home_return(master):
    master.destroy()
    Main_Menu()


# Create user files
def write(master, name, oc, pin):
    # Validate the user input
    if (is_number(name)) or (is_number(oc) == 0) or (is_number(pin) == 0) or name == "":
        CTkMessagebox(title="Error", message="Invalid Credentials\nPlease try again.", icon="warning")
        master.destroy()
        return

    f1 = open("Account_Record.txt", 'r')
    account_no = int(f1.readline())
    account_no += 1
    f1.close()

    f1 = open("Account_Record.txt", 'w')
    f1.write(str(account_no))
    f1.close()

    fdet = open(str(account_no) + ".txt", "w")
    fdet.write(pin + "\n")
    fdet.write(oc + "\n")
    fdet.write(str(account_no) + "\n")
    fdet.write(name + "\n")
    fdet.close()

    frec = open(str(account_no) + "-rec.txt", 'w')
    frec.write("Date                             Transaction            Balance\n")
    frec.write(str(strftime("[%Y-%m-%d] [%H:%M:%S]  ", gmtime())) + "    " + oc + "                " + oc + "\n")
    frec.close()

    CTkMessagebox(title="Acc Details", message="Your Account Number is: " + str(account_no), icon="check")
    master.destroy()
    return


# Update Users Credit/Deposits
def crdt_write(master, amount, account):
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")

    if is_number(amount) == 0:
        CTkMessagebox(title="Error", message="Invalid Input!", icon="cancel")
        master.destroy()
        return

    fdet = open(account + ".txt", 'r')
    pin = fdet.readline()
    camt = int(fdet.readline())
    fdet.close()

    amti = int(amount)
    cd = amti + camt
    fdet = open(account + ".txt", 'w')
    fdet.write(pin)
    fdet.write(str(cd) + "\n")
    fdet.write(account + "\n")
    fdet.close()

    frec = open(str(account) + "-rec.txt", 'a+')
    frec.write(
        str(strftime("[%Y-%m-%d] [%H:%M:%S]  ", gmtime())) + "+" + str(amti) + "              " + str(cd) + "\n")
    frec.close()
    CTkMessagebox(message="Deposit Successful!", icon="check")
    master.destroy()
    return


# Update Users Debits/Withdrawal
def debit_write(master, amount, account):
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")

    if is_number(amount) == 0:
        CTkMessagebox(title="Error", message="Invalid Input!", icon="cancel")
        master.destroy()
        return

    fdet = open(account + ".txt", 'r')
    pin = fdet.readline()
    camt = int(fdet.readline())
    fdet.close()

    if int(amount) > camt:
        CTkMessagebox(title="Error", message="Insufficient Funds!", icon="cancel")
    else:
        amti = int(amount)
        cd = camt - amti
        fdet = open(account + ".txt", 'w')
        fdet.write(pin)
        fdet.write(str(cd) + "\n")
        fdet.write(account + "\n")
        fdet.close()

        frec = open(str(account) + "-rec.txt", 'a+')
        frec.write(str(strftime("[%Y-%m-%d] [%H:%M:%S]  ", gmtime())) + "-" + str(amti) + "              " +
                   str(cd) + "\n")
        frec.close()
        CTkMessagebox(message="Withdrawal Successful!", icon="check")
        master.destroy()
        return


# Make deposit window
def deposit_amt(account):
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")

    deposit_wind = ctk.CTkToplevel()
    deposit_wind.geometry("500x500")
    deposit_wind.title("Deposits")

    # Image frame
    icon = ctk.CTkImage(dark_image=Image.open("Images/deposit.png"), size=(200, 200))
    disply_icon = ctk.CTkLabel(deposit_wind, image=icon, text='').pack(padx=20, pady=20)

    l1 = ctk.CTkLabel(deposit_wind, text="Enter Amount to be deposited: ")
    e1 = ctk.CTkEntry(deposit_wind)
    l1.pack(pady=12, padx=10)
    e1.pack(pady=12, padx=10)

    # Deposit Button
    b = ctk.CTkButton(deposit_wind, text="Deposit", command=lambda: crdt_write(deposit_wind, e1.get(), account))
    b.pack(pady=12, padx=10)
    deposit_wind.bind("<Return>", lambda x: crdt_write(deposit_wind, e1.get(), account))

    # Cancel Button
    b1 = ctk.CTkButton(deposit_wind, text="Cancel", command=deposit_wind.destroy)
    b1.pack(pady=12, padx=10)


# Make Deposit window
def withdraw_amt(account):
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")

    withdraw_wind = ctk.CTkToplevel()
    withdraw_wind.geometry("500x500")
    withdraw_wind.title("Withdrawals")

    # Image frame
    icon = ctk.CTkImage(dark_image=Image.open("Images/withdraw.png"), size=(200, 200))
    disply_icon = ctk.CTkLabel(withdraw_wind, image=icon, text='').pack(padx=20, pady=20)

    l1 = ctk.CTkLabel(withdraw_wind, text="Enter Amount to be withdrawn: ")
    e1 = ctk.CTkEntry(withdraw_wind)
    l1.pack(pady=12, padx=10)
    e1.pack(pady=12, padx=10)

    # Withdraw Button
    b = ctk.CTkButton(withdraw_wind, text="Withdraw", command=lambda: debit_write(withdraw_wind, e1.get(), account))
    b.pack(pady=12, padx=10)
    withdraw_wind.bind("<Return>", lambda x: debit_write(withdraw_wind, e1.get(), account))

    # Cancel Button
    b1 = ctk.CTkButton(withdraw_wind, text="Cancel", command=withdraw_wind.destroy)
    b1.pack(pady=12, padx=10)


# Display Balance
def disp_bal(account):
    fdet = open(account + ".txt", 'r')
    fdet.readline()
    bal = fdet.readline()
    fdet.close()
    CTkMessagebox(title="Balance", message="Current Balance: R" + str(bal))


# Display transaction history
def disp_tr_hist(account):
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")

    transaction_wind = ctk.CTkToplevel()
    transaction_wind.geometry("500x680")
    transaction_wind.title("Transaction History")

    # Title/Heading
    l_title = ctk.CTkLabel(master=transaction_wind, text="UNCUT BANKING SYSTEM", font=('Times New Roman Bold', 20))
    l_title.pack(pady=20)

    # Image frame
    icon = ctk.CTkImage(dark_image=Image.open("Images/trans_history.png"), size=(200, 200))
    disply_icon = ctk.CTkLabel(transaction_wind, image=icon, text='').pack(padx=20, pady=20)

    l1 = ctk.CTkLabel(transaction_wind, text="Your Transaction History:",  padx=100, pady=20, width=1000)
    l1.pack(side="top")

    scrollable_frame = ctk.CTkScrollableFrame(master=transaction_wind, width=200, height=200)
    scrollable_frame.pack(side="top", pady=20, padx=40, fill='both', expand=True)

    frec = open(account + "-rec.txt", 'r')
    for line in frec:
        l = ctk.CTkLabel(scrollable_frame, text=line, padx=100, pady=20, width=1000)
        l.pack(side="top")

    b = ctk.CTkButton(transaction_wind, text="Quit", command=transaction_wind.destroy)
    b.pack(pady=12, padx=10)
    frec.close()


def logged_in_menu(account):
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")

    root_wind = ctk.CTkToplevel()
    root_wind.geometry("500x680")
    root_wind.title("UNCUT BANKING SYSTEM")

    # Title/Heading
    l_title = ctk.CTkLabel(master=root_wind, text="UNCUT BANKING SYSTEM", font=('Times New Roman Bold', 20))
    l_title.pack(pady=20)

    # Image frame
    icon = ctk.CTkImage(dark_image=Image.open("Images/Welcome_page_icon.png"), size=(200, 200))
    disply_icon = ctk.CTkLabel(root_wind, image=icon, text='').pack(padx=20, pady=20)

    label = ctk.CTkLabel(master=root_wind, text="Welcome Back")
    label.pack(side="top")

    # Deposit Button
    b2 = ctk.CTkButton(master=root_wind, text="Deposit", command=lambda: deposit_amt(account))
    b2.pack(pady=12, padx=10)

    # Withdraw Button
    b3 = ctk.CTkButton(master=root_wind, text="Withdraw", command=lambda: withdraw_amt(account))
    b3.pack(pady=12, padx=10)

    # View Balance Button
    b4 = ctk.CTkButton(master=root_wind, text="View Balance", command=lambda: disp_bal(account))
    b4.pack(pady=12, padx=10)

    # View Transaction History Button
    b5 = ctk.CTkButton(master=root_wind, text="Transaction History", command=lambda: disp_tr_hist(account))
    b5.pack(pady=12, padx=10)

    # Log Out Button
    b6 = ctk.CTkButton(master=root_wind, text="Logout", command=lambda: logout(root_wind))
    b6.pack(pady=12, padx=10)


# Log out the user
def logout(master):
    CTkMessagebox(title="Log Out", message="You Have Been Successfully Logged Out!!", icon="check")
    master.destroy()
    Main_Menu()


# Login Validation
def check_log_in(master, account_num, pin):
    if check_acc_nmb(account_num) == 0:
        # master.destroy()
        # Main_Menu()
        return

    if is_number(pin) == 0:
        CTkMessagebox(title="Error", message="Account Number does not exist.\nPlease try again.", icon="warning")
        # master.destroy()
        # Main_Menu()
    else:
        master.destroy()
        logged_in_menu(account_num)


# Login Window
def log_in(master):
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")

    master.destroy()

    login_wind = ctk.CTkToplevel()
    login_wind.geometry("500x680")
    login_wind.title("Log in")

    # Title/Heading
    l_title = ctk.CTkLabel(master=login_wind, text="UNCUT BANKING SYSTEM", font=('Times New Roman Bold', 20))
    l_title.pack(pady=20)

    # Image frame
    icon = ctk.CTkImage(dark_image=Image.open("Images/Login_Icon.png"), size=(200, 200))
    disply_icon = ctk.CTkLabel(login_wind, image=icon, text='').pack(padx=20, pady=20)

    # Details Frame
    frame = ctk.CTkFrame(master=login_wind)
    frame.pack(pady=20, padx=40, fill='both', expand=True)

    # Enter Account number
    l2 = ctk.CTkLabel(frame, text="Enter account number:")
    l2.pack(side="top")
    e2 = ctk.CTkEntry(frame)
    e2.pack(pady=12, padx=10)

    # Enter Account Pin
    l3 = ctk.CTkLabel(frame, text="Enter your PIN:")
    l3.pack(side="top")
    e3 = ctk.CTkEntry(frame, show="*")
    e3.pack(pady=12, padx=10)

    # Show and Hide Pin
    def show_and_hide():
        if e3.cget('show') == '*':
            e3.configure(show='')
        else:
            e3.configure(show='*')

    pin_checkbox = ctk.CTkCheckBox(frame, text="Show Password", fg_color='red', font=('verdana', 11),
                                   command=show_and_hide)
    pin_checkbox.pack(pady=12, padx=10)

    # login Button
    b = ctk.CTkButton(frame, text="Submit", command=lambda: check_log_in(login_wind, e2.get().strip(), e3.get().strip()))
    b.pack(pady=12, padx=10)

    # Back Button
    b1 = ctk.CTkButton(login_wind, text="Back", command=lambda: home_return(login_wind))
    b1.pack(pady=12, padx=10)
    login_wind.bind("<Return>", lambda x: check_log_in(login_wind, e2.get().strip(), e3.get().strip()))


# Register a new user window
def signup():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    signup_wind = ctk.CTkToplevel()
    signup_wind.geometry("500x780")
    signup_wind.title("Create Account")

    # Title/Heading
    l_title = ctk.CTkLabel(master=signup_wind, text="UNCUT BANKING SYSTEM", font=('Times New Roman Bold', 20))
    l_title.pack(pady=20)

    # Image frame
    icon = ctk.CTkImage(dark_image=Image.open("Images/Signup_icon.png"), size=(200, 200))
    disply_icon = ctk.CTkLabel(signup_wind, image=icon, text='').pack(padx=20, pady=20)

    # Details Frame
    frame = ctk.CTkFrame(master=signup_wind)
    frame.pack(pady=20, padx=40, fill='both', expand=True)

    # Enter Name
    l1 = ctk.CTkLabel(frame, text="Enter Name:")
    l1.pack(side="top")
    e1 = ctk.CTkEntry(frame)
    e1.pack(pady=12, padx=10)

    # Enter the opening amount
    l2 = ctk.CTkLabel(frame, text="Enter opening amount:")
    l2.pack(side="top")
    e2 = ctk.CTkEntry(frame)
    e2.pack(pady=12, padx=10)

    # Enter New Pin
    l3 = ctk.CTkLabel(frame, text="Enter desired PIN:")
    l3.pack(side="top")
    e3 = ctk.CTkEntry(frame, show="*")
    e3.pack(pady=12, padx=10)

    # Show and Hide Pin
    def show_and_hide():
        if e3.cget('show') == '*':
            e3.configure(show='')
        else:
            e3.configure(show='*')

    pin_checkbox = ctk.CTkCheckBox(frame, text="Show Password", fg_color='red', font=('verdana', 11),
                                   command=show_and_hide)
    pin_checkbox.pack(pady=12, padx=10)

    # Sign up Button
    b = ctk.CTkButton(frame, text="Submit", command=lambda: write(signup_wind, e1.get().strip(), e2.get().strip(), e3.get().strip()))
    b.pack(pady=12, padx=10)

    # Back Button
    b1 = ctk.CTkButton(signup_wind, text="Back", command=signup_wind.destroy)
    b1.pack(pady=12, padx=10)

    signup_wind.bind("<Return>", lambda x: write(signup_wind, e1.get().strip(), e2.get().strip(), e3.get().strip()))
    return


# Welcome/Main Window
def Main_Menu():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")

    rootwn = ctk.CTkToplevel()
    rootwn.geometry("500x500")
    rootwn.title("Uncut Banking System")

    # Title
    l_title = ctk.CTkLabel(master=rootwn, text="UNCUT BANKING SYSTEM", font=('Times New Roman Bold', 20))
    l_title.pack(pady=20)

    # Image frame
    icon = ctk.CTkImage(dark_image=Image.open("Images/Home_page.png"), size=(200, 200))
    disply_icon = ctk.CTkLabel(rootwn, image=icon, text='').pack(padx=20, pady=20)

    # Sign up button
    b1 = ctk.CTkButton(rootwn, text="Sign Up", command=signup)
    b1.pack(pady=12, padx=10)

    # Login Button
    b2 = ctk.CTkButton(rootwn, text="Login", command=lambda: log_in(rootwn))
    b2.pack(pady=12, padx=10)

    # Quite Button
    b6 = ctk.CTkButton(rootwn, text="Exit", command=rootwn.destroy)
    b6.pack(pady=12, padx=10)

    rootwn.mainloop()


Main_Menu()

