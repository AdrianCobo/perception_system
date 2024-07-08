import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np

def create_graph():
    contents = open("/home/adrianco/Desktop/ros2_ws/src/perception_system/data/FPS.txt", "r").read().split('\0')
    fps_text = contents[0].split('\n')
    fps_text = fps_text[:-1] # the last data is always empty i dont know why
    fps_int = []
    print(fps_text)

    x = np.arange(0, len(fps_text))

    for c in fps_text:
        fps_int.append(int(c))

    fig = plt.figure()

    plt.plot(x,fps_int, label="fps")
    plt.legend(loc=2)

    print("std_dev of cart bars dist",np.std(fps_int), "mean: ", np.mean(fps_int))

    plt.show()

create_graph()