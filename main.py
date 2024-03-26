import sys
import EyeTrackFatigue.UI.EvalApp as ea # импорт визуального интерфейса для приложения оценки
#import EyeTrackFatigue.UI.DataGather as dg # импорт визуального интерфейса для приложения рассчёта характеристик
from PyQt6.QtWidgets import QApplication
app = QApplication(sys.argv)
ex = ea.EvalApp() # запуск приложения оценки
#ex = dg.Example() # запуск приложения рассчёта характеристик
sys.exit(app.exec())
