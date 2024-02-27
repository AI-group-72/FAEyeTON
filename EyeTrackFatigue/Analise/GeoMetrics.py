# класс для хранения характеристик геомертического положения взгляда/головы
class GeoMetrics:

    def __init__(self):
        #x_mean,x_std,x_min,x_max,x_25,x_50,x_75,y_mean,y_std,y_min,y_max,y_25,y_50,y_75
        self.x_mean = self.x_std = self.x_min = self.y_mean = self.y_std = self.y_min = 0
        self.x_max = self.x_25 = self.x_50 = self.y_max = self.y_25 = self.y_50 = 0
