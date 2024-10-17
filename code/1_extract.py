import pandas as pd
import numpy as np
import streamlit as st
import pandaslib as pl
  
#TODO Write your extraction code here
web_survey_df = pd.read_csv("https://docs.google.com/spreadsheets/d/1IPS5dBSGtwYVbjsfbaMCYIWnOuRmJcbequohNxCyGVw/export?resourcekey=&gid=1625408792&format=csv")
web_survey_df["year"] = web_survey_df["Timestamp"].apply(pl.extract_year_mdy)
years = web_survey_df["year"].unique()
for year in years:
    web_COL = pd.read_html(f"https://www.numbeo.com/cost-of-living/rankings.jsp?title={year}&displayColumn=0")
    web_COL_df = web_COL[1]
    web_COL_df["year"] = year
    web_COL_df.to_csv(f"cache/col_{year}.csv", index = False)
web_survey_df.to_csv("cache/survey.csv", index = False)

web_states_df = pd.read_csv("https://docs.google.com/spreadsheets/d/14wvnQygIX1eCVo7H5B7a96W1v5VCg6Q9yeRoESF6epw/export?format=csv")
web_states_df.to_csv("cache/states.csv", index = False)
