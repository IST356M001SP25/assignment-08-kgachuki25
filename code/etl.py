import pandas as pd
import streamlit as st 


def top_locations(violations_df : pd.DataFrame, threshold=1000) -> pd.DataFrame:
    # Key dataframe to make each row a location (pivot)
    violations_pivot = pd.pivot_table(violations_df, values = "amount", index = "location", aggfunc = "sum")
    violations_pivot["location"] = violations_pivot.index # making index into column
    violations_pivot.reset_index(drop = True, inplace= True) # removing index
    
    # Filtering by amount >= threshold, returning df
    violations_final = violations_pivot[violations_pivot["amount"] >= threshold]

    return pd.DataFrame(violations_final)

def top_locations_mappable(violations_df : pd.DataFrame, threshold=1000) -> pd.DataFrame:
    # Key dataframe to make each row a location (pivot)
    violations_pivot = pd.pivot_table(violations_df, values = "amount", index = "location", aggfunc = "sum")
    violations_pivot["location"] = violations_pivot.index # making index into column
    violations_pivot.reset_index(drop = True, inplace= True) # removing index

    # Joining lat and lon data from original
    violations_mappable = violations_pivot.merge(violations_df, how = "left", on = "location")
    filter_cols = ["location", "lat", "lon", "amount_x"]
    violations_mappable = violations_mappable[filter_cols]
    violations_mappable.rename(columns = {"amount_x":"amount"}, inplace = True)

    # Filtering by amount >= threshold, return
    violations_mappable = violations_mappable[violations_mappable["amount"] >= threshold]
    violations_mappable.drop_duplicates(subset = "location", inplace = True) # removes duplicates made from merge
    
    return pd.DataFrame(violations_mappable)

def tickets_in_top_locations(violations_df : pd.DataFrame, threshold=1000) -> pd.DataFrame:
    # Key dataframe to make each row a location (pivot)
    violations_pivot = pd.pivot_table(violations_df, values = "amount", index = "location", aggfunc = "sum")
    violations_pivot["location"] = violations_pivot.index # making index into column
    violations_pivot.reset_index(drop = True, inplace= True) # removing index
    
    # Filtering by amount >= threshold
    violations_top = violations_pivot[violations_pivot["amount"] >= threshold]
    top_loc_list = violations_top["location"].to_list()

    # Filter orginal df by list of top locations
    tickets_df = violations_df[violations_df["location"].isin(top_loc_list)]
    return pd.DataFrame(tickets_df)

if __name__ == '__main__':
    '''
    Main ETL job. 
    '''
    violations_df = pd.read_csv("cache/final_cuse_parking_violations.csv")
    
    top_df = top_locations(violations_df = violations_df)
    top_df.to_csv("cache/top_locations.csv", index = False)

    mappable_df = top_locations_mappable(violations_df = violations_df)
    mappable_df.to_csv("cache/top_locations_mappable.csv", index = False)

    tickets_df = tickets_in_top_locations(violations_df= violations_df)
    tickets_df.to_csv("cache/tickets_in_top_locations.csv", index=False)