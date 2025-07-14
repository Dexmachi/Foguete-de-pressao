import matplotlib.pyplot as plt


def plot_distance_vs_time(times, distances):

    # Create the plot
    plt.plot(
        times,
        distances,
        linestyle="-",
        color="teal",
        markersize=6,
        linewidth=2,
        label="Distância",
    )  # Customize color and line

    # Add labels and title with custom fonts and size
    plt.xlabel("Tempo (s)", fontsize=12, fontweight="bold")
    plt.ylabel("Distância (m)", fontsize=12, fontweight="bold")
    plt.title("Distância Horizontal em Função do Tempo", fontsize=14, fontweight="bold")

    # Add grid with more contrast and style
    plt.grid(True, linestyle="--", color="gray", alpha=0.7)

    # Customize the background color of the plot
    plt.gcf().set_facecolor("white")

    # Add a legend
    plt.legend(loc="upper left")

    # Set x and y axis limits for a better view
    plt.xlim(0, 60)
    plt.ylim(0, max(distances) + 50)

    # Display the plot
    plt.show()
