import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


filepath = 'https://github.com/DjSelorm/boilerplate-medical-data-visualizer/blob/main/medical_examination.csv'#'/content/medical_examination.csv'
# 1
df = pd.read_csv(filepath)

# 2. Adding an  overweight column???????????????????
df['overweight'] = (df['weight'] / (df['height']/100)**2 > 25).astype(int)


# 3  Normalize cholesterol and glucose (1 → 0,0 → 1 , >1 → 1)
df['cholesterol'] = (df['cholesterol'] > 1).astype(int)
df['gluc'] = (df['gluc'] > 1).astype(int)



#Draw the Categorical Plot
# 4. Define function for categorical plot

def draw_cat_plot():
    # 5. Melt the DataFrame to long format
    df_cat = pd.melt(df, 
                     id_vars=['cardio'], 
                     value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])
    
    # 6. Group and reformat: split by cardio and count each feature value
    df_cat = df_cat.groupby(['cardio', 'variable', 'value']).size().reset_index(name ='total')

    # 7.
    
    # 8. Draw the categorical plot
    fig = sns.catplot(x='variable', y='total', hue='value', col='cardio',
                      data=df_cat, kind='bar')
    fig.set_axis_labels("Feature", "Count")
    # 9 Save and return figure
    fig.savefig('catplot.png')
    return fig


# 10 Draw the Heat Map 
def draw_heat_map():
    # 11 Clean the data
    df_heat = df[(df['ap_lo'] <= df['ap_hi']) &
                 (df['height'] >= df['height'].quantile(0.025)) &
                 (df['height'] <= df['height'].quantile(0.975)) &
                 (df['weight'] >= df['weight'].quantile(0.025)) &
                 (df['weight'] <= df['weight'].quantile(0.975))]


    # 12 Calculate the correlation matrix and store it
    corr = df_heat.corr()
        

    # 13 Generate a mask for the upper triangle and store it 
    mask = np.triu(np.ones_like(corr, dtype=bool))


    # 14 set up figure
    fig, ax = plt.subplots(figsize=(12, 8))

    # 15
    sns.heatmap(corr, mask=mask, annot=True, fmt='.1f', center=0,
                cmap='coolwarm', square=True, linewidths=0.5)


    # 16
    fig.savefig('heatmap.png')
    return fig
