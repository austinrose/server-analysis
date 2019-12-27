# plotting results
import pandas
import numpy as np
import matplotlib.pyplot as plt


def plot(data, plot_data, name_list):
    title = plot_data[1]
    plot_path = plot_data[0]
    
    plt.style.use('ggplot')
    n = len(name_list)
    on_time = data[0]
    detect = data[1]
    fig, ax = plt.subplots()
    index = np.arange(n)
    bar_width = 0.35
    opacity = 0.9
    rect1 = ax.bar(index, on_time, bar_width, alpha=opacity, color='b',
                    label='On-Time Accuracy')
    rect2 = ax.bar(index+bar_width, detect, bar_width, alpha=opacity, color='orange',
                    label='Detection Accuracy')
    ax.set_xlabel('Servers')
    ax.set_ylabel('%')
    ax.set_title(title)
    ax.set_xticks(index + bar_width / 2)
    ax.set_xticklabels(name_list)
    ax.legend()

    def autolabel(rects):
    # """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')
    
    autolabel(rect1)
    autolabel(rect2)

    fig.savefig(plot_path)
    plt.close('all')
