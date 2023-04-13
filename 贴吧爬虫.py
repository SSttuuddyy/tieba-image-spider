from utils import Spieder
from gui import Gui

if __name__=='__main__':
    gui = Gui()
    sp = Spieder()
    gui.sp = sp
    sp.gui = gui
    gui.gene()