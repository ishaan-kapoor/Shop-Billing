from tkcalendar import DateEntry
from tkinter import Button, Entry, Label, StringVar, Tk, messagebox

class CustomEntry(Entry):
    def __init__(self, master=None, textvariable=None, background="#121212"):
        super().__init__(
            master,
            bd=0,
            fg="white",
            justify="center",
            font=("Times", 18),
            highlightthickness=0,
            background=background,
            selectbackground="white",
            textvariable=textvariable,
            selectforeground="#464646",
        )

    def grid(self, row=0, column=0, pad=2):
        super().grid(row=row, column=column, padx=pad, pady=pad)


class CustomButton(Button):
    def __init__(self, master=None, text="", command=None):
        super().__init__(
            master,
            text=text,
            fg="white",
            command=command,
            background="#a6a6a6".replace("a", "4"),
        )

    def grid(self, row=0, column=0, pad=2):
        super().grid(row=row, column=column, padx=pad, pady=pad)


class CustomLabel(Label):
    def __init__(self, master=None, text=None, textvariable=None):
        super().__init__(
            master,
            bd=0,
            text=text,
            fg="white",
            justify="center",
            font=("Times", 18),
            background="#121212",
            highlightthickness=0,
            highlightcolor="#464646",
            textvariable=textvariable,
            highlightbackground="white",
        )

    def grid(self, row=0, column=0, pad=2):
        super().grid(row=row, column=column, padx=pad, pady=pad)


def close():
    global running
    if not running: return

    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        running = False
        root.destroy()

def getReceipts(key: str='Dealer'):
    import os
    temp = date.get().split('-')
    match temp[1]:
        case '01':month = 'January'
        case '02': month = 'February'
        case '03': month = 'March'
        case '04': month = 'April'
        case '05': month = 'May'
        case '06': month = 'June'
        case '07': month = 'July'
        case '08': month = 'August'
        case '09': month = 'September'
        case '10': month = 'October'
        case '11': month = 'November'
        case '12': month = 'December'
        case _: month = 'Month'
    path = ''
    for folder in ('Receipts', temp[-1], month, temp[0]):
        path = os.path.join(path, folder)
        if not os.path.exists(path):
            messagebox.showerror(title='No Receipts', message='No Receipts Exist for the chosen date.')
            return
    root.update()
    temp = filterVal.get().strip().lower()
    total = count = 0
    for receipt in os.listdir(path):
        receipt = os.path.join(path, receipt)
        with open(receipt) as file:
            data = file.read().strip().split('\n')
        for line in data[-2:]:
            line = line.strip()
            if line.startswith(key) and line.replace(key, '').strip().lower().startswith(temp):
                valid = True
                break
            valid = False
        if not valid: continue
        for line in data[-4:]:
            line = line.strip()
            if line.startswith('Grand Total'):
                total += int(line.split(' ')[-1])
                break
        os.startfile(receipt)
        count += 1

    if count: messagebox.showinfo('Receipts Opened', f'{count} receipts shown!\nTotal: {total} (Probably)')
    else: messagebox.showwarning('Incorrect Filter', 'No Receipts Match the Filter')



commission = lambda: getReceipts(key='Dealer')


payment = lambda: getReceipts(key='Payment Mode')


running = True

root = Tk()
root.title("UTSAV Settlement - By Ishaan")
root.config(bg="#121212")
root.resizable(width=True, height=True)
root.protocol("WM_DELETE_WINDOW", close)

CustomLabel(root, text='Selected Date').grid(row=1, column=1)
date = DateEntry(root, date_pattern='dd-mm-y', justify="center", width=15)#, style='s.TEntry')
date.grid(row=1, column=2)
CustomLabel(root, text='Filter Value').grid(row=2, column=1)
filterVal = StringVar(value='-')
CustomEntry(root, textvariable=filterVal).grid(row=2, column=2)
CustomButton(root, text="Staff Commission", command=getReceipts).grid(row=1, column=3)
CustomButton(root, text="Payment Mode", command=payment).grid(row=2, column=3)


root.mainloop()
exit()