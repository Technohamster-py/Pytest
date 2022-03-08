"""
--------------------------------------------------
Programm by: Technohamster

Python version:        Year:
        3.8            2020

Thank you for using my programm! Good luck)
---------------------------------------------------
"""

# TODO: Для следующих версий: Сделать возможность вывода в файл excel (задебажить то, что есть),
#  сделать проверку вывода в файл

from tkinter.filedialog import *
from tkinter import *
from  tkinter.messagebox import showerror, showinfo
import logic


dolog = None
testdata = None
outdata = None
table_path = None


def init_window(Display):
    '''Инициация стартового окна, его виджетов и т.д.'''
    main_frame = Frame(Display, bg='#DFDDDC')
    main_frame.pack(side=TOP, fill='both', expand=True)
    init_path_bar(main_frame)
    init_start_btn(main_frame)


def init_path_bar(frame):
    input_frame = Frame(frame,  bg='#DFDDDC')
    input_frame.place(rely=0.3, relx=0.05)

    output_frame = Frame(frame,  bg='#DFDDDC')
    output_frame.place(rely=0.5, relx=0.1)

    table_frame = Frame(frame, bg='#DFDDDC')
    table_frame.place(rely=0.05, relx=0.25)

    table_btn = Button(table_frame, font=13, text='Select excel file\nfor journal writing', command=ask_xlc, state=DISABLED)
    input_btn = Button(input_frame, font=13, text='Select the folder of the tested programs', command=ask_testdata)
    output_btn = Button(output_frame, font=13, text='Select an answer and criteria folder', command=ask_correctdata)

    table_btn.pack()
    input_btn.pack()
    output_btn.pack()


def init_start_btn(frame):
    start_frame = Frame(frame,  bg='#ADB2B3')
    start_frame.place(rely=0.85, relx=0, relheight=0.15, relwidth=1)
    init_log_check(start_frame)

    start_btn = Button(start_frame, font=13, text='Start testing', command=start_check)
    start_btn.pack(side=RIGHT, padx=3, pady=2)


def init_log_check(frame):
    global dolog
    check_frame = Frame(frame)
    check_frame.place(relx=0.02, rely=0.2)
    dolog = BooleanVar()
    log_check = Checkbutton(check_frame, text='Make a log', variable=dolog, bg='#DFDDDC')
    log_check.pack()
    log_check.select()


def ask_xlc():
    global table_path
    table_path = askopenfilename(filetypes=(('Excel files', '.xlsx'),('Excel 2003 or earlier', '.xls')))


def ask_testdata():
    global testdata
    testdata = askdirectory()


def ask_correctdata():
    global outdata
    outdata = askdirectory()


def check_poss():
    """
    Функция проверяет возможность запуска проверки
    :return:
    """
    errors = []
    if testdata is not None and outdata is not None:
        return True, 0
    else:
        '''if table_path is None:
            errors.append('t')'''

        if testdata is None:
            errors.append('i')

        if outdata is None:
            errors.append('o')

        return False, errors


def start_check():
    global dolog
    possible, errors = check_poss()
    try:
        dolog = dolog.get()
    except AttributeError:
        pass

    if possible:
        logic.start_checking(outdata, testdata, table_path)
        showinfo('Info', 'Testing completed successfully')
    else:
        if 't' in errors:
            showerror('ERROR', 'Excel file error, please select file.')
        if 'i' in errors:
            showerror('ERROR', 'Select the folder of the tested programs')
        if 'o' in errors:
            showerror('ERROR', 'Select an answer and criteria folder')


def init_gui():

    Display = Tk()

    Display.title('Technohamster pytest')

    window_hight = 300
    '''Высота окна = 400 пикселей'''
    window_width = 400
    '''Ширина окна = 300 пикселей'''

    x_pos = Display.winfo_screenwidth() // 2 - window_width // 2
    '''задается позиция верхнего левого угла по координате Х'''
    y_pos = Display.winfo_screenheight() // 2 - window_hight // 2
    '''задается позиция верхнего левого угла по координате Y'''
    Display.geometry(f'{window_width}x{window_hight}+{x_pos}+{y_pos}')
    '''Размещение окна'''
    Display.resizable(width=False, height=False)
    '''эти три строки помещают центр окна по центру монитора'''

    init_window(Display)

    Display.mainloop()


if __name__ == '__main__':
    init_gui()
