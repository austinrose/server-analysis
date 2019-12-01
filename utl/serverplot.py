# plotting results
import pandas
import numpy as np
import matplotlib.pyplot as plt


def plot(data, title, plot_path):
    plt.style.use('ggplot')
    n = 4
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
    ax.set_xticklabels(('dev-fused-02','dev-fused-03','prod-fused-04','prod-fused-06'
        ))
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
