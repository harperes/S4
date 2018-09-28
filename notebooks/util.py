def mpl_plot(x_arrs, y_arrs, label_arr, xlabel, ylabel, plt_title=None):
    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=(6,6))
    ax = fig.add_subplot(111)
    for x, y, l in zip(x_arrs, y_arrs, label_arr):
        ax.plot(x, y, label=l)
    ax.set_xlabel(xlabel, fontsize=16)
    ax.set_ylabel(ylabel, fontsize=16)
    ax.tick_params(labelsize=14)
    ax.set_xlim((0, 90))
    ax.set_ylim((0, 1))
    ax.legend()
    if plt_title is not None:
        ax.set_title(plt_title, fontsize=18)
    return fig, ax

def log_progress(sequence, every=None, size=None, name='Items'):
    """ Function to create a jupyter notebook progress bar

    Args:
        sequence (list or generator):
        every (int):frequency to update the progress bar
        size (int): size of progress bar if not known from sequence
        name (str): label to put on the progress bar

    Returns:
        progress bar
    """
    from ipywidgets import IntProgress, HTML, VBox
    from IPython.display import display

    is_iterator = False
    if size is None:
        try:
            size = len(sequence)
        except TypeError:
            is_iterator = True
    if size is not None:
        if every is None:
            if size <= 200:
                every = 1
            else:
                every = int(size / 200)     # every 0.5%
    else:
        assert every is not None, 'sequence is iterator, set every'

    if is_iterator:
        progress = IntProgress(min=0, max=1, value=1)
        progress.bar_style = 'info'
    else:
        progress = IntProgress(min=0, max=size, value=0)
    label = HTML()
    box = VBox(children=[label, progress])
    display(box)

    index = 0
    try:
        for index, record in enumerate(sequence, 1):
            if index == 1 or index % every == 0:
                if is_iterator:
                    label.value = '{name}: {index} / ?'.format(
                        name=name,
                        index=index
                    )
                else:
                    progress.value = index
                    label.value = u'{name}: {index} / {size}'.format(
                        name=name,
                        index=index,
                        size=size
                    )
            yield record
    except:
        progress.bar_style = 'danger'
        raise
    else:
        progress.bar_style = 'success'
        progress.value = index
        label.value = "{name}: {index}".format(
            name=name,
            index=str(index or '?')
        )
