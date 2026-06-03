import pandas as pd

def load_data():
   df = pd.read_csv("worldcities.csv", encoding="utf-8")
    
    df.columns = df.columns.str.strip().str.lower()
    
    df.dropna(subset=["city", "country"], inplace=True)
    
    df["population"] = pd.to_numeric(df["population"], errors="coerce")
    
    df["lat"] = pd.to_numeric(df["lat"], errors="coerce")
    df["lng"] = pd.to_numeric(df["lng"], errors="coerce")
    
    df.dropna(subset=["population"], inplace=True)
    
    df.reset_index(drop=True, inplace=True)
    
    return df

def apply_filters(df, selected_countries, selected_capitals, pop_range, search_text):
    
    if selected_countries:
        df = df[df["country"].isin(selected_countries)]
    
    if selected_capitals:
        df = df[df["capital"].isin(selected_capitals)]
    
    df = df[(df["population"] >= pop_range[0]) & (df["population"] <= pop_range[1])]
    
    if search_text:
        df = df[df["city"].str.contains(search_text, case=False, na=False)]
    
    return df
