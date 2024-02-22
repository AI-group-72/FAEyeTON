import math

class EyeMovement:
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
            print(' error ')
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
            print('error')
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


class HeadMovement(EyeMovement):
    def __init__(self, movement_type):
        super.__init__(movement_type)
        self.angles = []
        self.angle_distances = []
        self.angle_velocities = []
        self.angle_accelerations = []

    def add_point_angle(self, angle):
        
        self.angles.append(angle)
        if len(self.angles) < 2:
            return
        self.angle_distances.append(abs(self.angles[-1] - self.angles[-2]))
        self.angle_velocities.append(self.angle_distances[-1] / (self.points[-1].time - self.points[-2].time))
        if len(self.angle_velocities) < 2:
            return
        self.accelerations.append(
            abs(self.angle_velocities[-1] - self.angle_velocities[-2]) / (self.points[-1].time - self.points[-2].time))

    def get_avr_angle_speed(self):
        return sum(self.angle_distances) / self.time

    def get_med_angle_speed(self):
        return sum(self.angle_velocities) / len(self.angle_velocities)

    def get_min_angle_speed(self):
        return min(self.angle_velocities)

    def get_max_angle_speed(self):
        return max(self.angle_velocities)

    def get_avr_angle_acceleration(self):
        acc = 0
        for i in range(2, len(self.angles)):
            acc += self.angle_accelerations[i-2] * (self.points[i].time - self.points[i-1].time)
        return acc / self.time

    def get_min_angle_acceleration(self):
        if len(self.angle_accelerations) > 0:
            return min(self.angle_accelerations)
        else:
            return 1000000

    def get_max_angle_acceleration(self):
        if len(self.angle_accelerations) > 0:
            return max(self.angle_accelerations)
        else:
            return 0

    def get_abs_angle_distance(self):
        if len(self.points) < 2:
            print(' error ')
            return 1
        return abs(self.angles[-1] - self.angles[0])

    def get_angle_distance(self):
        return sum(self.angle_distances)