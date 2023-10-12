import requests
import pandas as pd
import streamlit as st
from bs4 import BeautifulSoup

# Streamlit app title
st.title("New Castle County App")

# Create two columns for form components
left_column, right_column = st.columns(2)

# Text input boxes in the left column
with left_column:
    name_last = st.text_input("Last Name")
    name_middle = st.text_input("Middle Name")
    file_number = st.text_input("File Number")
    sort_order = st.selectbox("Sort Order", ["Date of Death", "Last Name", "First Name"])
    ascending_descending = st.selectbox("Ascending/Descending", ["Ascending", "Descending"])

# Dropdown lists in the right column
with right_column:
    name_first = st.text_input("First Name")
    year = st.text_input("Year")
    month = st.text_input("Month")
    day = st.text_input("Day")

if sort_order == "Date of Death":
    sort_order = '1'
elif sort_order == "Last Name":
    sort_order = '2'
else :
    sort_order = '3'

if ascending_descending == "Ascending":
    ascending_descending = '1'
else :
    ascending_descending = '2'

# Button to submit the form
submit_button = st.button("Search")

# Logic to handle form submission
if submit_button:
    data = {
    '__EVENTTARGET': '',
    '__EVENTARGUMENT': '',
    '__VIEWSTATE': '/wEPDwUJNjAwNzYxMTY5ZGRWDEY4LSrJwJcaapYGrZw4u71Qgd7BPmoSkP/ffiwrOA==',
    '__VIEWSTATEGENERATOR': '237C7B20',
    '__EVENTVALIDATION': '/wEdAA5wVMFNbsbR+nM5fHTWOrms7DE1A+42MZ5zicydYC+qYHftBWEvbQNFG6oSDsSyqm1bKooAGcuCfKX1hs4RCpq9bIxwvYBnKFJqUUkkFQ6IFqoZoJVBktYMXTqRkA6PwecPyy63FWK57XpXZSQAiOcPQi24uIPv787j9n1q8f/Bo7QDclGdh0exVOpDIPxW6PVQffS8Bz2rmRZCsOAcytTMSMalIvq7f1vkt4ZrGktGfdvF3ZFWtZpToNFsverWWP1srKu9zepYoFiqPNOYNVaQympO1xWBIk3RHP/6Jlu4/754tnzGYxMU+qKlhymo8+H8rO+6HGnagka6y7Y5OGoS',
    'ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder1$_TextBoxNameLast': name_last if name_last else '',
    'ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder1$_TextBoxNameFirst': name_first if name_first else '',
    'ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder1$_TextBoxNameMiddle': name_middle if name_middle else '',
    'ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder1$_TextBoxYear': year if year else '',
    'ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder1$_TextBoxMonth': month if month else '',
    'ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder1$_TextBoxDay': day if day else '',
    'ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder1$_TextBoxFileNumber': file_number if file_number else '',
    'ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder1$_DropDownListSortOrder': sort_order if sort_order else '',
    'ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder1$_DropDownListAscendingDescending': ascending_descending if ascending_descending else '',
    'ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder1$_ButtonSearch': 'Search',
    }

    response = requests.post('https://www3.newcastlede.gov/will/search/', data=data)

    # Parse the HTML content of the response
    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find("table", {"class":"grid"})

    # Extract table rows and cells
    table_rows = table.find_all("tr")
    data_list = []

    # Extract data from table rows and cells
    for row in table_rows:
        cols = row.find_all(['td', 'th'])  # td for data cells, th for header cells
        cols = [col.text.strip() for col in cols]
        data_list.append(cols)

    # Convert the list of lists into a DataFrame
    df = pd.DataFrame(data_list[1:], columns=data_list[0])
    # Drop the first column
    df = df.drop(df.columns[0], axis=1)

    # Display basic information about the DataFrame
    st.write(f"There are {df.shape[0]} items matching your search criteria.")

    # Display the DataFrame in the Streamlit app
    st.dataframe(df)