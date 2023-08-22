#main.py
import streamlit as st
import pandas as pd

# Importing From Files
from data_format import gather_data, create_report_data, report_data_calc
from content_format import fetch_headlines, create_report_content, generate_newsletter

st.markdown("## Welcome To The Secerct Satoshis Newsletter App")
st.markdown(
  "Simply input the newsletter date and content below. The Coin Metrics Bitcoin API data will be downloaded and formatted for ChatGPT which will then write the newsletter automatically."
)
st.markdown(
  "If you have no content to input simply run the application by pressing 'Submit Inputs' at the bottom of the form."
)

# Set Report Date
date = st.date_input(
  "Enter the report date. Format: (YYYY/MM/DD) | Date must be 1 Day behind current date as data is only available T-1"
)

# All Inputs in Single Form
input_form = st.form(key='input_form')

default_support_prices = ""
default_support_contexts = ""
default_resistance_prices = ""
default_resistance_contexts = ""

support_prices = input_form.text_area(
  "Enter support prices (comma separated): ", default_support_prices)
support_contexts = input_form.text_area(
  "Enter support contexts (comma separated): ", default_support_contexts)
resistance_prices = input_form.text_area(
  "Enter resistance prices (comma separated): ", default_resistance_prices)
resistance_contexts = input_form.text_area(
  "Enter resistance contexts (comma separated): ", default_resistance_contexts)

content_types = [
  "News Stories", "Podcast", "Tweets", "Books", "Not Gonna Make It Events"
]
content_lists = []

for content_type in content_types:
  urls = input_form.text_area(
    f"Enter URLs for {content_type} (comma separated): ")
  content_lists.append({'name': content_type, 'urls': urls.split(',')})

input_submit = input_form.form_submit_button("Submit Inputs")

# On form submission, perform operations
if input_submit:
  # Convert input to correct format
  date = pd.to_datetime(date)
  support_levels = {
    'price':
    list(map(float, support_prices.split(','))) if support_prices else [],
    'context':
    support_contexts.split(',') if support_contexts else []
  }
  resistance_levels = {
    'price':
    list(map(float, resistance_prices.split(',')))
    if resistance_prices else [],
    'context':
    resistance_contexts.split(',') if resistance_contexts else []
  }

  # --- Gather Data --- #
  coinmetrics_data = gather_data()

  # --- Create / Filter Report Data --- #
  selected_metrics = create_report_data(coinmetrics_data)

  # Check if the selected date is in the data range
  if date in selected_metrics['time'].values:
    # --- Create Report Data --- #
    report_data = report_data_calc(date, selected_metrics)

    # --- Create Report Content --- #
    report_txt_output = create_report_content(report_data, support_levels,
                                              resistance_levels)

    # --- Get Content Headlines --- #
    curated_content = fetch_headlines(content_lists)

    # --- Print Report Content --- #
    st.markdown("## Report Content")
    st.markdown("This is the data provided to ChatGPT to write the newsletter.")
    st.write(report_txt_output)

    # Print the newsletter
    st.markdown("## Formatted Newsletter Links")
    st.write(curated_content)
    st.markdown("## Writting Newsletter")
    st.markdown("ChatGPT has begun writting the newsletter please wait 1 min.")

    # Generate the newsletter
    newsletter = generate_newsletter(report_txt_output)
    st.markdown("## Newsletter Content Complete")
    st.write(newsletter)
  else:
    st.write("Selected date is not in the data range.")