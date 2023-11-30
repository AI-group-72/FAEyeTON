from random import *
import matplotlib.pyplot as plt
from typing import List, Dict
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


class Bedbug:

    def __init__(self, age=None, day_of_born=0):
        self.id = 0
        self.day = 0
        self.day_to_born = day_of_born
        self.day_to = 0
        self.day_of_death = randint(365, 548)
        self.male = choice(['male', 'female'])
        if age is None:
            self.age = choice(['egg', 'bug'])
        else:
            self.age = age
        if self.age == 'egg':
            self.day_to_born = randint(6, 17)
            self.day_to = self.day_to_born
        else:
            self.day_to = 0

    def death_rate(self):
        if self.day <= 50:
            return 0.01
        if 50 < self.day <= 100:
            return 0.1
        if 100 < self.day <= 200:
            return 0.2
        return 0.3

    def run(self, had_food):
        if self.day_to != 0:
            self.day_to -= 1
        if self.day_to == 0:
            self.age = 'bug'
        if self.age == 'egg':
            return
        self.day += 1
        if self.day == self.day_of_death or (random() < (self.death_rate() * (1 if had_food else 2))):
            self.age = 'dead'

    def consume(self):
        return 0 if self.age == 'egg' else 1

    def spawn(self, bugs: List['Bedbug']) -> None:
        if self.male == 'female' and self.age == 'bug':
            n = randint(1, 12)
            new_bugs = [Bedbug('egg', self.day) for _ in range(n)]
            bugs.extend(new_bugs)

    def count(self, counts: Dict[str, int]) -> None:
        if self.age == 'egg':
            counts['eggs'] += 1
        elif self.age == 'bug':
            counts['bugs'] += 1
        elif self.age == 'dead':
            counts['dead'] += 1


class Simulation:
    def __init__(self, days: int, n: int, **kwargs):
        self.days = days
        self.n = n
        self.params = kwargs  # Сохраняем параметры в атрибуте params
        self.bugs = [Bedbug() for _ in range(n)]
        self.counts = {'eggs': 0, 'bugs': n, 'dead': 0}
        self.total_dead = 0

    def run(self) -> List[List[int]]:
        K = self.params.get('K', 100)
        r = self.params.get('r', 50)
        g_option = self.params.get('g_option', "constant")
        g_constant = self.params.get('g_constant', 0)
        g_k = self.params.get('g_k', 10)
        g_c = self.params.get('g_c', 3)

        x1 = [self.counts['eggs']]
        x2 = [self.counts['bugs']]
        x3 = [self.counts['dead']]
        y = [0]

        for day in range(1, self.days + 1):
            self.counts = {'eggs': 0, 'bugs': 0, 'dead': 0}
            food = 100
            shuffle(self.bugs)
            for cur_bug in self.bugs:
                if food > 0:
                    cur_bug.run(True)
                    cur_bug.spawn(self.bugs)
                    food -= cur_bug.consume()
                else:
                    cur_bug.run(False)
                if cur_bug.age == 'dead':
                    self.bugs.remove(cur_bug)
                cur_bug.count(self.counts)

            self.total_dead += self.counts['dead']
            x1.append(self.counts['eggs'])
            x2.append(self.counts['bugs'])
            x3.append(self.counts['dead'])
            y.append(day)

        return [x1, x2, x3, y]


class Graphs:
    def __init__(self, master):
        self.master = master
        self.master.geometry('1000x1000')
        self.master.title('Моделирование жизни постельного клопа')
        self.N = None
        self.DAYS = None

        self.left_frame = tk.Frame(self.master)
        self.left_frame.pack(side=tk.LEFT, padx=10, pady=10)
        self.left_frame.config(width=500, height=500)

        self.label1 = tk.Label(self.left_frame, text='Введите начальное количество клопов', font=('Arial', 16))
        self.label1.pack(pady=5)

        self.entry1 = tk.Entry(self.left_frame, width=10)
        self.entry1.pack(pady=5)

        self.label2 = tk.Label(self.left_frame, text='Введите рассматриваемый временной промежуток', font=('Arial', 16))
        self.label2.pack(pady=5)

        self.entry2 = tk.Entry(self.left_frame, width=10)
        self.entry2.pack(pady=5)

        self.constant_r_label = tk.Label(self.left_frame, text='Введите константу для r:', font=('Arial', 16))
        self.constant_r_label.pack(pady=5)

        self.constant_r_entry = tk.Entry(self.left_frame, width=10)
        self.constant_r_entry.pack(pady=5)

        self.constant_K_label = tk.Label(self.left_frame, text='Введите константу для K:', font=('Arial', 16))
        self.constant_K_label.pack(pady=5)

        self.constant_K_entry = tk.Entry(self.left_frame, width=10)
        self.constant_K_entry.pack(pady=5)

        self.g_choice_label = tk.Label(self.left_frame, text='Выберите способ задания g:', font=('Arial', 16))
        self.g_choice_label.pack(pady=5)
        self.g_choice = tk.StringVar(value="constant")
        self.g_choice_listbox = tk.Listbox(self.left_frame, selectmode='single', exportselection=0, height=3)
        self.g_choice_listbox.pack(pady=5)
        self.g_choice_listbox.insert(0, "Константа")
        self.g_choice_listbox.insert(1, "Линейная функция")
        self.g_choice_listbox.insert(2, "Сложная функция")

        self.g_constant_label = tk.Label(self.left_frame, text='Введите константу для g:', font=('Arial', 16))
        self.g_constant_label.pack(pady=5)

        self.g_constant_entry = tk.Entry(self.left_frame, width=10)
        self.g_constant_entry.pack(pady=5)

        self.button = tk.Button(self.left_frame, text='Запустить симуляцию', font=('Arial', 20), command=self.run_simulation)
        self.button.pack(pady=10)

        self.right_frame = tk.Frame(self.master)
        self.right_frame.pack(side=tk.RIGHT, padx=10, pady=10)
        self.right_frame.config(width=500, height=500)

        self.fig = plt.figure(figsize=(12, 7))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def run_simulation(self):
        self.N = int(self.entry1.get())
        self.DAYS = int(self.entry2.get())
        K = float(self.constant_K_entry.get())
        r = float(self.constant_r_entry.get())
        g_option = self.g_choice_listbox.get(self.g_choice_listbox.curselection())
        g_constant = 0
        g_k = 10
        g_c = 3

        if g_option == "Константа":
            g_constant = float(self.g_constant_entry.get())
            K += g_constant
            r -= g_constant
        elif g_option == "Линейная функция":
            g = g_k * self.DAYS + g_c
            K += g
            r -= g
        else:
            g = 0
            K += g
            r -= g

        P0 = self.N
        def logistic_curve(x, K, r):
            return (K * P0 * np.exp(r * x)) / (K + P0 * (np.exp(r * x) - 1))

        params = {'K': K, 'r': r, 'g_constant': g_constant, 'g_k': g_k, 'g_c': g_c}

        sim = Simulation(self.DAYS, self.N, **params)
        x1, x2, x3, y = sim.run()
        x4 = [logistic_curve(day, K, r) for day in y]
        self.draw_graph(x1, x2, x3, y, x4)

    def draw_graph(self, x1, x2, x3, y, x4):
        self.fig.clf()

        plt.plot(y, x1, 'o-r', alpha=0.7, label='График количества яиц', lw=5, mec='b', mew=2, ms=10)
        plt.plot(y, x2, 'v-.g', alpha=0.7, label='График количества взрослых особей', lw=5, mec='b', mew=2, ms=10)
        plt.plot(y, x3, 'c', alpha=0.7, label='График количества умерших особей за день', lw=5, mec='b', mew=2, ms=10)

        plt.plot(y, x4, '--b', alpha=0.7, label='Модель логистической кривой', lw=5, mec='r', mew=2, ms=10)

        plt.legend()
        plt.grid(True)
        self.canvas.draw()


root = tk.Tk()
graph = Graphs(root)
root.mainloop()
