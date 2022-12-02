from TapChinhta import HocChinhTa
from hocToan import HocToan
from vuaTiengViet import VuaTiengViet
from tkinter import *


def ClickBtnHocChinhTa():
    HocChinhTa("")


def ClickBtnHocToan():
    HocToan("")


def ClickBtnVuaTiengViet():
    VuaTiengViet("")


window = Tk()
window.title("Welcome to LikeGeeks app")
window.geometry('350x200')
btn = Button(window, text="HocChinhTa", command=ClickBtnHocChinhTa)
btn.grid(column=1, row=0)
btn = Button(window, text="HocToan", command=ClickBtnHocToan)
btn.grid(column=2, row=0)
btn = Button(window, text="VuaTiengViet", command=ClickBtnVuaTiengViet)
btn.grid(column=3, row=0)
window.mainloop()
