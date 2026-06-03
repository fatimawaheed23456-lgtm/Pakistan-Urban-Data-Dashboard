import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# ── Global style ──────────────────────────────────────────
PALETTE = "Blues_d"
BG      = "#0f1117"
TEXT    = "#ffffff"
ACCENT  = ["#4C72B0","#55A868","#C44E52","#8172B2",
           "#CCB974","#64B5CD","#E07B39","#D65799",
           "#76C7C0","#F0A500"]

def style_fig(fig, title):
    fig.patch.set_facecolor(BG)
    for ax in fig.axes:
        ax.set_facecolor(BG)
        ax.title.set_color(TEXT)
        ax.xaxis.label.set_color(TEXT)
        ax.yaxis.label.set_color(TEXT)
        ax.tick_params(colors=TEXT)
        for spine in ax.spines.values():
            spine.set_edgecolor("#444444")
    fig.suptitle(title, color=TEXT, fontsize=14, fontweight="bold")
    return fig


# 1. PIE CHART ─────────────────────────────────────────────
def pie_chart(df):
    top = df["country"].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.pie(top.values, labels=top.index, autopct="%1.1f%%",
           colors=ACCENT, startangle=140,
           textprops={"color": TEXT})
    return style_fig(fig, "Top 10 Countries by Number of Cities")


# 2. HISTOGRAM ─────────────────────────────────────────────
def histogram(df):
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.histplot(df["population"], bins=50, color=ACCENT[0],
                 ax=ax, kde=True)
    ax.set_xlabel("Population")
    ax.set_ylabel("Frequency")
    return style_fig(fig, "Population Distribution")


# 3. LINE CHART ────────────────────────────────────────────
def line_chart(df):
    top10 = (df.groupby("country")["population"]
               .sum()
               .sort_values(ascending=False)
               .head(10)
               .reset_index())
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(top10["country"], top10["population"],
            marker="o", color=ACCENT[0], linewidth=2)
    ax.set_xlabel("Country")
    ax.set_ylabel("Total Population")
    plt.xticks(rotation=45, ha="right")
    return style_fig(fig, "Total Population by Top 10 Countries")


# 4. BAR CHART ─────────────────────────────────────────────
def bar_chart(df):
    top10 = (df.groupby("country")["population"]
               .sum()
               .sort_values(ascending=False)
               .head(10)
               .reset_index())
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.barplot(data=top10, x="country", y="population",
                palette=ACCENT, ax=ax)
    ax.set_xlabel("Country")
    ax.set_ylabel("Total Population")
    plt.xticks(rotation=45, ha="right")
    return style_fig(fig, "Top 10 Countries by Total Population")


# 5. SCATTER PLOT ──────────────────────────────────────────
def scatter_plot(df):
    sample = df.sample(min(1000, len(df)), random_state=42)
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.scatterplot(data=sample, x="lng", y="lat",
                    size="population", hue="population",
                    palette="Blues", sizes=(20, 400),
                    alpha=0.7, ax=ax, legend=False)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    return style_fig(fig, "City Locations by Population (Lat vs Lng)")


# 6. BOX PLOT ──────────────────────────────────────────────
def box_plot(df):
    top8 = (df.groupby("country")["population"]
              .sum()
              .sort_values(ascending=False)
              .head(8)
              .index.tolist())
    filtered = df[df["country"].isin(top8)]
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.boxplot(data=filtered, x="country", y="population",
                palette=ACCENT, ax=ax)
    ax.set_xlabel("Country")
    ax.set_ylabel("Population")
    plt.xticks(rotation=45, ha="right")
    return style_fig(fig, "Population Spread by Top 8 Countries")


# 7. HEATMAP ───────────────────────────────────────────────
def heatmap(df):
    numeric = df[["population", "lat", "lng"]].dropna()
    corr = numeric.corr()
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="Blues",
                ax=ax, linewidths=0.5,
                annot_kws={"color": TEXT})
    return style_fig(fig, "Correlation Heatmap")


# 8. AREA CHART ────────────────────────────────────────────
def area_chart(df):
    top10 = (df.groupby("country")["population"]
               .sum()
               .sort_values(ascending=False)
               .head(10)
               .reset_index())
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.fill_between(range(len(top10)), top10["population"],
                    alpha=0.4, color=ACCENT[0])
    ax.plot(range(len(top10)), top10["population"],
            color=ACCENT[0], linewidth=2)
    ax.set_xticks(range(len(top10)))
    ax.set_xticklabels(top10["country"], rotation=45, ha="right")
    ax.set_xlabel("Country")
    ax.set_ylabel("Total Population")
    return style_fig(fig, "Area Chart — Population by Top 10 Countries")


# 9. COUNT PLOT ────────────────────────────────────────────
def count_plot(df):
    top8 = df["country"].value_counts().head(8).index.tolist()
    filtered = df[df["country"].isin(top8)]
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.countplot(data=filtered, y="country",
                  order=top8, palette=ACCENT, ax=ax)
    ax.set_xlabel("Number of Cities")
    ax.set_ylabel("Country")
    return style_fig(fig, "Number of Cities per Country (Top 8)")


# 10. VIOLIN PLOT ──────────────────────────────────────────
def violin_plot(df):
    top5 = (df.groupby("country")["population"]
              .sum()
              .sort_values(ascending=False)
              .head(5)
              .index.tolist())
    filtered = df[df["country"].isin(top5)]
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.violinplot(data=filtered, x="country", y="population",
                   palette=ACCENT, ax=ax)
    ax.set_xlabel("Country")
    ax.set_ylabel("Population")
    plt.xticks(rotation=45, ha="right")
    return style_fig(fig, "Population Density Distribution (Top 5 Countries)")