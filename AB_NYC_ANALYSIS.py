import pandas as pd
import numpy as np
import matplotlib.pyplot as plt     
import seaborn as sns
from matplotlib.patches import Patch 

df = pd.read_csv("AB_NYC_2019.csv", on_bad_lines='skip')

valid_groups = ['Manhattan', 'Brooklyn', 'Queens', 'Staten Island','Bronx']
df_clean = df[df['neighbourhood_group'].isin(valid_groups)]

avg_price_per_group = df_clean.groupby('neighbourhood_group')['price'].mean().round(0).astype(int).sort_values(ascending=False)

sns.set_style('whitegrid')


palette = sns.color_palette('pastel')


plt.figure(figsize=(8,5))
sns.barplot(x=avg_price_per_group.index, y=avg_price_per_group.values, palette=palette)

plt.title('Prosečna cena noćenja po kvartovima', fontsize=16)
plt.ylabel('Cena ($)', fontsize=16)
plt.xlabel('')
plt.ylim(0, max(avg_price_per_group) + 50)


for index, value in enumerate(avg_price_per_group):
    plt.text(index, value + 5, str(value), ha='center', fontsize=18, color='gray')

plt.xticks(fontsize=16)
plt.tight_layout()
plt.savefig("avg_price_per_group.png",dpi=300)
plt.show()

df_clean = df[df['neighbourhood_group'].isin(valid_groups)]

# Filtriramo kvartove koji imaju barem 30 oglasa
neigh_counts = df_clean['neighbourhood'].value_counts()
valid_neighs = neigh_counts[neigh_counts >= 30].index
filtered_df = df_clean[df_clean['neighbourhood'].isin(valid_neighs)]

# Top 10 kvartova sa najvišom prosečnom cenom
top10_filtered = (
    filtered_df.groupby('neighbourhood')
    .agg({'price': 'mean', 'neighbourhood_group': 'first'})
    .sort_values('price', ascending=False)
    .head(10)
    .round(0)
    .astype({'price': 'int'})
)


group_colors = {
    'Manhattan': '#2ca02c',        
    'Brooklyn': '#1f77b4',         
    'Queens': '#ff7f0e',          
    'Staten Island': '#d62728',   
    'Bronx': '#9467bd'             
}
bar_colors = top10_filtered['neighbourhood_group'].map(group_colors)


sns.set_style('whitegrid')
plt.figure(figsize=(10, 6))

bars = sns.barplot(
    x=top10_filtered.index,
    y=top10_filtered['price'],
    palette=bar_colors.tolist()
)


plt.title('Top 10 kvartova po prosečnoj ceni noćenja (min 30 oglasa)', fontsize=16)
plt.ylabel('Cena ($)', fontsize=14)
plt.xlabel('')
plt.xticks(rotation=30, fontsize=12)
plt.yticks(fontsize=12)
plt.ylim(0, top10_filtered['price'].max() + 50)


for i, value in enumerate(top10_filtered['price']):
    plt.text(i, value + 5, str(value), ha='center', fontsize=12, color='gray')


legend_elements = [Patch(facecolor=color, label=group) for group, color in group_colors.items()]
plt.legend(handles=legend_elements, title='Neighbourhood Group', fontsize=11, title_fontsize=12)

plt.tight_layout()
plt.savefig("top10_expensive_neighbourhoods.png",dpi=300)
plt.show()


price_heatmap = (
    filtered_df.groupby(['neighbourhood_group', 'room_type'])['price']
    .mean()
    .round(0)
    .unstack()
    .fillna(0)
    .astype(int)
)

plt.figure(figsize=(10, 6))
sns.heatmap(price_heatmap, annot=True, fmt='d', cmap='YlGnBu')

plt.title('Prosečna cena po tipu sobe i kvartovima', fontsize=16)
plt.ylabel('Neighbourhood Group', fontsize=14)
plt.xlabel('Tip sobe', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()
plt.savefig("avg_price_per_room_type.png",dpi=300)
plt.show()