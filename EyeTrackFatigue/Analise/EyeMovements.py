import math

class Movement:
    FOV = 82 * math.sqrt(2)

    def __init__(self, movement_type):
        self.movementType = movement_type
        self.points = []
        self.distances = []
        self.time = 0
        self.velocities = []
        self.accelerations = []

    def add_point(self, point):
        self.points.append(point)
        if len(self.points) < 2:
            return
        self.time = point.time - self.points[0].time
        self.distances.append(self.points[-1].get_distance(self.points[-2]))
        self.velocities.append(self.distances[-1] / (self.points[-1].time - self.points[-2].time))
        if len(self.velocities) < 2:
            return
        self.accelerations.append(
            abs(self.velocities[-1] - self.velocities[-2]) / (self.points[-1].time - self.points[-2].time))

    def get_avr_speed(self):
        return sum(self.distances) / self.time

    def get_med_speed(self):
        return sum(self.velocities) / len(self.velocities)

    def get_min_speed(self):
        return min(self.velocities)

    def get_max_speed(self):
        return max(self.velocities)

    def get_avr_acceleration(self):
        acc = 0
        for i in range(2, len(self.points)):
            acc += self.accelerations[i-2] * (self.points[i].time - self.points[i-1].time)
        return acc / self.time

    def get_min_acceleration(self):
        if len(self.accelerations) > 0:
            return min(self.accelerations)
        else:
            return 1000000

    def get_max_acceleration(self):
        if len(self.accelerations) > 0:
            return max(self.accelerations)
        else:
            return 0

    def get_abs_distance(self):
        if len(self.points) < 2:
            print(' er ')
            return 1
        return self.points[-1].get_distance(self.points[0])

    def get_distance(self):
        return sum(self.distances)

    def in_center(self, center_radius):
        x = y = 0
        for p in self.points:
            x += p.x
            y += p.y
        x /= len(self.points)
        y /= len(self.points)
        return math.sqrt(pow((self.FOV / 2) - x, 2) + pow((self.FOV / 2) - y, 2)) < center_radius

    def get_curve(self):
        if self.get_abs_distance() == 0:
            print('double er')
            return 1
        return sum(self.distances) / self.get_abs_distance()

    def get_max_dist(self):
        max_x = min_x = self.points[0].x
        max_y = min_y = self.points[0].y
        for point in self.points:
            max_x = max(max_x, point.x)
            min_x = min(min_x, point.x)
            max_y = max(max_y, point.y)
            min_y = min(min_y, point.y)
        return max(max_y - min_y, max_x - min_x)

    def get_area_dist(self):
        start = self.points[0]
        end = self.points[-1]
        return pow(pow(end.x - start.x, 2) + pow(end.y - start.y, 2), 0.5)
