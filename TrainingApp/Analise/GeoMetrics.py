import math

class GeoMetrics:

    def __init__(self):
        #x_mean,x_std,x_min,x_max,x_25,x_50,x_75,y_mean,y_std,y_min,y_max,y_25,y_50,y_75
        self.x_mean = self.x_std = self.x_min = self.y_mean = self.y_std = self.y_min = 0
        self.x_max = self.x_25 = self.x_50 = self.y_max = self.y_25 = self.y_50 = 0


'''
# -----------------#
x = np.array(df['norm_pos_x'])
x_mean = np.mean(x).reshape(1, 1)
x_std = np.std(x).reshape(1, 1)
x_min = np.min(x).reshape(1, 1)
x_max = np.max(x).reshape(1, 1)
x_25 = np.percentile(x, 25).reshape(1, 1)
x_50 = np.percentile(x, 50).reshape(1, 1)
x_75 = np.percentile(x, 75).reshape(1, 1)
# -----------------#
y = np.array(df['norm_pos_y'])
y_mean = np.mean(y).reshape(1, 1)
y_std = np.std(y).reshape(1, 1)
y_min = np.min(y).reshape(1, 1)
y_max = np.max(y).reshape(1, 1)
y_25 = np.percentile(y, 25).reshape(1, 1)
y_50 = np.percentile(y, 50).reshape(1, 1)
y_75 = np.percentile(y, 75).reshape(1, 1)
'''