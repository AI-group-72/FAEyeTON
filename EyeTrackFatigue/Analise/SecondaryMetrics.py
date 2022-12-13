import math

class SecondaryMetrics:

    def __init__(self):
        self.fix_distance = self.sacc_distance = 0
        self.fix_time = self.sacc_time = 0.00000001
        self.min_f_speed = self.min_s_speed = self.min_s_length = self.min_s_time = 1000000
        self.max_f_speed = self.max_s_speed = self.max_s_length = self.max_s_time = 0

        self.min_curve = self.min_acc = 100000
        self.max_curve = self.max_acc = 0
        self.avr_curve = self.avr_acc = 0
        self.sacc_length = 0
        self.long_sacc = self.short_sacc = 0
        self.short_fix_time = self.long_fix_time = self.med_fix_time = 0
        self.short_fix_count = self.long_fix_count = self.med_fix_count = 0
        self.fix_l_80 = self.fix_g_1000 = self.fix_l_180 = self.fix_g_180 = 0

        self.avr_freq = self.max_freq = self.min_freq = 0
        self.avr_i_speed = self.max_i_speed = 0
        self.avr_i_acc = self.max_i_acc = 0
        self.min_i_speed = self.min_i_acc = 1000000
