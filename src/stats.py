import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set()


def plot(stats, solver_config, f_path):
    min_scores, avg_scores, max_scores = list(map(list, zip(*stats)))

    df = pd.DataFrame({
        "generation": range(len(stats)),
        "min_score": min_scores,
        "avg_score": avg_scores,
        "max_score": max_scores
    })

    # plot = sns.lineplot(data=df, markers=True, dashes=False)
    # plot.set_title("Genetic Algorithm Fitness Scores by Generation")
    # plot.text(2000, 2000, f'{solver_config}', fontsize=9)
    # plot.subplots_adjust(left=0.25)
    # fig = plot.get_figure()
    # fig.savefig(f_path)

    plt.plot('generation', 'min_score', data=df, marker='.', color='skyblue', linewidth=2)
    plt.plot('generation', 'avg_score', data=df, marker='.', color='darkorange', linewidth=2)
    plt.plot('generation', 'max_score', data=df, marker='.', color='forestgreen', linewidth=2)

    plt.legend()
    plt.gcf().text(0.1, 0.00, f"{solver_config}", fontsize=9)
    plt.subplots_adjust(bottom=0.27)
    plt.savefig(f_path)

    plt.cla()
    plt.clf()
    plt.close()
