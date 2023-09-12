import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


data = pd.read_csv("medical_examination.csv")


data['bmi'] = data['weight'] / ((data['height'] / 100) ** 2)
data['overweight'] = (data['bmi'] > 25).astype(int)


data['cholesterol'] = (data['cholesterol'] > 1).astype(int)
data['gluc'] = (data['gluc'] > 1).astype(int)


data = data[(data['ap_lo'] <= data['ap_hi']) &
            (data['height'] >= data['height'].quantile(0.025)) &
            (data['height'] <= data['height'].quantile(0.975)) &
            (data['weight'] >= data['weight'].quantile(0.025)) &
            (data['weight'] <= data['weight'].quantile(0.975))]


def draw_cat_plot():
    
    cat_data = pd.melt(data, id_vars="cardio", value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active'])
    cat_data['total'] = 1
    cat_data = cat_data.groupby(['variable', 'value', 'cardio'], as_index=False).count()

   
    g = sns.catplot(x='variable', y='total', hue='value', col='cardio', data=cat_data, kind='bar')
    g.set_axis_labels("Variable", "Total")
    g.set_titles("{col_name} = {col_var}")
    g.set(yscale="log")
    
    
    plt.savefig("cat_plot.png")


draw_cat_plot()


def draw_heat_map():
    corr_matrix = data.corr()
    mask = np.triu(corr_matrix)

    
    plt.figure(figsize=(12, 8))
    sns.heatmap(corr_matrix, annot=True, fmt=".1f", linewidths=0.5, mask=mask, cmap="coolwarm")

    
    plt.savefig("heat_map.png")


draw_heat_map()