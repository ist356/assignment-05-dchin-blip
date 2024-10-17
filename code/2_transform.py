import pandas as pd
import streamlit as st
import pandaslib as pl

# TODO: Write your transformation code here
survey_df = pd.read_csv("cache/survey.csv")
years = survey_df["year"].unique()
for i in range(len(years)):
    if i == 0:
        year = years[0]
        COL_df = pd.read_csv(f"cache/col_{year}.csv")
    else:
        year = years[i]
        COL_df = pd.concat([COL_df, pd.read_csv(f"cache/col_{year}.csv")])
states_df = pd.read_csv("cache/states.csv")

survey_df["_country"] = survey_df["What country do you work in?"].apply(pl.clean_country_usa)
survey_states_combined_df = pd.merge(left = survey_df, right = states_df, left_on = "If you're in the U.S., what state do you work in?", right_on = "State", how = "inner")
survey_states_combined_df["_full_city"] = survey_states_combined_df["What city do you work in?"].str.title() + ", " + survey_states_combined_df["Abbreviation"] + ", " + survey_states_combined_df["_country"]

combined = pd.merge(left = survey_states_combined_df, right = COL_df, left_on = ["year", "_full_city"], right_on = ["year", "City"], how = "inner").drop("Rank", axis = 1)
combined["_annual_salary_cleaned"] = combined["What is your annual salary? (You'll indicate the currency in a later question. If you are part-time or hourly, please enter an annualized equivalent -- what you would earn if you worked the job 40 hours a week, 52 weeks a year.)"].apply(pl.clean_currency)
combined["_annual_salary_adjusted"] = combined["_annual_salary_cleaned"] * (100 / combined["Cost of Living Index"])

combined.to_csv("cache/survey_dataset.csv")
first_report = combined.pivot_table(index = "_full_city", columns = "How old are you?", values = "_annual_salary_adjusted", aggfunc = "mean")
first_report.to_csv("cache/annual_salary_adjusted_by_location_and_age.csv")
second_report = combined.pivot_table(index = "_full_city", columns = "What is your highest level of education completed?", values = "_annual_salary_adjusted", aggfunc = "mean")
second_report.to_csv("cache/annual_salary_adjusted_by_location_and_education.csv")
