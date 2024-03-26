import sys
import EyeTrackFatigue.UI.EvalApp as ea
#import EyeTrackFatigue.UI.DataGather as dg
from PyQt6.QtWidgets import QApplication
app = QApplication(sys.argv)
ex = ea.EvalApp()
#ex = dg.Example()
sys.exit(app.exec())

'''


#pip install EyeTrackFatigue
import sys
import EyeTrackFatigue as etf 
#from EyeTrackFatigue.UI.EvalApp import EvalApp
#from EyeTrackFatigue.UI.DataGather import Example
from PyQt6.QtWidgets import QApplication
app = QApplication(sys.argv)
#ex = EvalApp()
print(etf)

ex = etf.UI.DataGather.Example()
sys.exit(app.exec())

'''
