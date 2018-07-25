import io

import matplotlib.pyplot as plt
import numpy as np


def get_graph():
    nums = np.random.normal(0, 1, 1000)

    fig = plt.figure()
    fig.suptitle('Ptydash Plot')
    ax = fig.subplots()
    ax.hist(nums)

    buffer = io.BytesIO()
    fig.savefig(buffer, format='png')
    plt.close(fig)
    buffer.seek(0)

    return buffer.read()
