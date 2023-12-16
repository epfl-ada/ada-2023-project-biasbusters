import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba_array
import matplotlib.cm as cm

# @Function piechart-subplot for community
def plot_community_piechart(genre_community, top_n):
    # Aggregate the total movie count for each community
    community_movie_counts = genre_community.groupby('community')['count'].sum()

    # Create a color map for communities
    cmap = cm.get_cmap('Blues', max(community_movie_counts.index) + 1)
    community_colors = cmap(range(max(community_movie_counts.index) + 1))

    # Filter to the top N genres by count
    top_genres = genre_community.nlargest(top_n, 'count')

    # Create subplots for the pie charts
    fig, axs = plt.subplots(1, 2, figsize=(20, 8))

    # Left pie chart - Community sizes
    community_labels = [f'Community {comm}' for comm in community_movie_counts.index]
    community_sizes = community_movie_counts.values
    axs[0].pie(community_sizes, labels=community_labels, colors=community_colors, autopct='%1.1f%%')
    axs[0].set_title('Sizes of Communities')

    # Right pie chart - Genres colored by community
    genre_community['color'] = genre_community['community'].apply(lambda x: to_rgba_array(community_colors[x]))
    axs[1].pie(top_genres['count'], labels=top_genres['genres'], colors=top_genres['color'], autopct='%1.1f%%', startangle=90)
    axs[1].set_title(f'Top {top_n} Genres within Communities')

    # Show the plot
    plt.tight_layout()
    plt.show()

    # Calculate the percentage of the total movie count represented by the top N genres
    sum_top_n = top_genres['count'].sum()
    total_sum = genre_community['count'].sum()
    percentage_top_n = (sum_top_n / total_sum) * 100
    print(f"The top {top_n} genres represent {percentage_top_n:.2f}% of the total count.")
