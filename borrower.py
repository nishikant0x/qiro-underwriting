import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import date, timedelta
from io import StringIO
import requests
import csv
import sqlite3
import os
import uuid
from io import BytesIO
import json
from datetime import datetime
import subprocess
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import plotly.graph_objects as go
import sweetviz as sv


       
def app():
    with st.sidebar:
        opt=st.radio("Select Option",('Add Company Data','Add Financial Data','Connect APIs','Borrower Profile','Important Ratios','Generate Imp Ratios','Create Pool'))
  

    if opt == "Add Company Data":
        st.title("Add company data")
        with st.form("Company Info"):
            # Create two columns for the form
            col1, col2 = st.columns(2)
            # Define the form inputs for the first column
            company_name = col1.text_input("Company name", "")
            company_website = col1.text_input("Company website", "")
            company_linkedin = col1.text_input("Company LinkedIn page", "")
            company_description = col1.text_input("Tell us a bit more about your company", "")
            company_founded = col1.text_input("In what year was the company founded?", "")
            team_size = col1.text_input("What's the size of the team?", "")
            funding_stage = col1.text_input("What's the equity funding stage? (Seed, Series A, Series B, etc)", "")
            location = col1.selectbox("In which locations do you currently have operations in?", (
                "Brazil",
                "Colombia",
                "Mexico",
                "Argentina",
                "Other LatAm Countries",
                "Africa",
                "Asia",
                "Europe",
                "North America"
            ))

            # Define the form inputs for the second column
            credit_rating = col2.text_input("Credit Rating", "")
            credit_score = col2.text_input("Credit Score", "")
            asset_type = col1.selectbox("Select the Asset Type", (
                "Agro loans",
                "Buy-now-pay-later consumers",
                "Buy-now-pay-later SMEs",
                "Car financing",
                "Credit card",
                "Credit card receivables advancing",
                "Educational/student loans",
                "FGTS loans",
                "Government-backed loans",
                "Hard-asset backed loans",
                "INSS loans",
                "Machinery/equipment leasing",
                "Payroll loans",
                "Real estate loans",
                "Receivables advancing (with recourse)",
                "Receivables advancing (without recourse)",
                "Revenue-based financing",
                "Secured consumer loans",
                "Secured SME working capital loans",
                "Solar panels financing",
                "Supply chain financing",
                "Trade financing",
                "Unsecured consumer loans",
                "Unsecured SME working capital loans",
                "Vehicle leasing"
            ))
            total_volume_originated = col2.text_input("What's the total volume originated to date?", "")
            volume_last_12_months = col2.text_input("What was the volume originated in the last 12 months?", "")
            avg_loan_size_last_12_months = col2.text_input("What was the average loan size in the last 12 months?", "")
            avg_interest_rate_last_12_months = col2.text_input("What was the average interest rate of the loan portfolio in the last 12 months?", "")
            avg_loan_term_last_12_months = col2.text_input("What was the average loan term of the loan portfolio in the last 12 months?", "")
            avg_npl_90_last_12_months = col2.text_input("What was the average NPL 90 of the last 12 months?", "")
            institutional_deck = col2.text_input("Link to Institutional Deck", "")

            form_submitted = st.form_submit_button("Submit Form")

            if form_submitted:
                # Create a dictionary to store form data
                form_data = {
                    "Company Name": company_name,
                    "Company Website": company_website,
                    "Company LinkedIn Page": company_linkedin,
                    "Company Description": company_description,
                    "Year Founded": company_founded,
                    "Team Size": team_size,
                    "Funding Stage": funding_stage,
                    "Location": location,
                    "Credit Rating": credit_rating,
                    "Credit Score": credit_score,
                    "Asset Type": asset_type,
                    "Total Volume Originated": total_volume_originated,
                    "Volume Last 12 Months": volume_last_12_months,
                    "Avg Loan Size Last 12 Months": avg_loan_size_last_12_months,
                    "Avg Interest Rate Last 12 Months": avg_interest_rate_last_12_months,
                    "Avg Loan Term Last 12 Months": avg_loan_term_last_12_months,
                    "Avg NPL 90 Last 12 Months": avg_npl_90_last_12_months,
                    "Institutional Deck Link": institutional_deck
                }

                form_data_df = pd.DataFrame([form_data])
                # form_data_df["id"]=1
                # form_data_df.to_csv("company_det.csv")
                df = pd.read_csv("company_det.csv")
                form_data_df["id"]=len(df)+1
                df = pd.concat([df, form_data_df], ignore_index=True)

                df.to_csv("company_det.csv")
                st.write("Details saved uccesfully")

                # Append the data to the CSV file
                # append_to_csv(form_data,"cn")

                # Clear the form fields after submission
                st.session_state.clear()

    if opt == "Add Financial Data":
        # def save_to_csv(data, filename):
        #     headers = data.keys()
        #     rows = zip(*data.values())
        #     with open(filename, 'w', newline='') as csvfile:
        #         writer = csv.writer(csvfile)
        #         writer.writerow(headers)
        #         writer.writerows(rows)

        conn = sqlite3.connect('my_db.db')
        cursor = conn.cursor()
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS docs (
                        id INTEGER PRIMARY KEY,
                        incorporation_docs TEXT,
                        subsidiary_docs TEXT,
                        licenses TEXT,
                        agreements TEXT,
                        financial_projections TEXT,
                        expenses_revenue_breakdown TEXT,
                        unit_economics TEXT,
                        debt_agreements TEXT,
                        investor_deck TEXT,
                        go_to_market_strategy TEXT,
                        customer_segments TEXT,
                        acquisition_funnel TEXT,
                        underwriting_policy TEXT,
                        credit_scorecard TEXT,
                        credit_lines_policy TEXT,
                        credit_risk_rating TEXT,
                        origination_data TEXT,
                        monthly_data TEXT,
                        gtv_data TEXT,
                        invoice_data TEXT,
                        additional_info TEXT,
                        constraints TEXT
                    )
                ''')

        def upload_to_google_drive(drive,file_obj):
            file = drive.CreateFile()
            file.SetContentFile(file_obj.name)
            file['title'] = file_obj.name
            file.Upload()

            return file['alternateLink'] 
                

        

        def main():
            st.title('Data Collection App')

            clm1,clm2=st.columns(2)

            # gauth = GoogleAuth()
            # gauth.LocalWebserverAuth()  # Authenticate with Google Drive API
            # drive = GoogleDrive(gauth)
            
            # Legal Documents
            with clm1:
                st.header('Legal Documents')
                incorporation_docs = st.file_uploader('Incorporation documents')
                subsidiary_docs = st.file_uploader('Subsidiary registration and ownership')
                licenses = st.file_uploader('Licenses where applicable')
                agreements = st.file_uploader('Agreements with partners, customers, etc.')
            
            # Financials
            with clm2:
                st.header('Financials')
                financial_projections = st.file_uploader('Financial Projections')
                expenses_revenue_breakdown = st.file_uploader('Current expenses and revenue breakdown')
                unit_economics = st.file_uploader('Unit Economics')
                debt_agreements = st.file_uploader('Existing debt facility/lender agreements')
            
            # Investor Presentation
            with clm1:
                st.header('Investor Presentation')
                investor_deck = st.file_uploader('Investor Deck with business strategy and performance')
                go_to_market_strategy = st.file_uploader('Go to market strategy')
                customer_segments = st.file_uploader('Key customer segments')
                acquisition_funnel = st.file_uploader('Detailed acquisition funnel')
            
            # Credit documentation
            with clm2:
                st.header('Credit Documentation')
                underwriting_policy = st.file_uploader('Underwriting policy')
                credit_scorecard = st.file_uploader('Credit Scorecard')
                credit_lines_policy = st.file_uploader('Credit Lines & Credit line increase policy')
                credit_risk_rating = st.file_uploader('Credit Risk rating for the portfolio')
            
            # Loan Tapes
            with clm1:
                st.header('Loan Tapes')
                origination_data = st.file_uploader('Raw Origination data')
                monthly_data = st.file_uploader('Monthly data of active and delinquent A/C')
                gtv_data = st.file_uploader('GTV of underwritten data')
                invoice_data = st.file_uploader('Total invoice outstanding/repaid invoices')
                
            # Other
            with clm2:
                st.header('Other')
                additional_info = st.text_area('Additional information specific to your business/industry')
                constraints = st.text_area('Constraints and considerations you would like lenders to consider')


            submitted = st.button('Save to Google Drive and Database')
            if submitted:
                # Loop through all the uploaded files and upload them to Google Drive
                gauth = GoogleAuth()
                gauth.LocalWebserverAuth() # Authenticate with Google Drive API
                drive = GoogleDrive(gauth) 

                file_links = {}
                for field_name, file_obj in {
                    'Incorporation Documents': incorporation_docs,
                    'Subsidiary Registration and Ownership': subsidiary_docs,
                    'Licenses': licenses,
                    'Agreements': agreements,
                    'Financial Projections': financial_projections,
                    'Current expenses and revenue breakdown': expenses_revenue_breakdown,
                    'Unit Economics': unit_economics,
                    'Existing debt facility/lender agreements': debt_agreements,
                    'Investor Deck with business strategy and performance': investor_deck,
                    'Go to market strategy': go_to_market_strategy,
                    'Key customer segments': customer_segments,
                    'Detailed acquisition funnel': acquisition_funnel,
                    'Underwriting policy': underwriting_policy,
                    'Credit Scorecard': credit_scorecard,
                    'Credit Lines & Credit line increase policy': credit_lines_policy,
                    'Credit Risk rating for the portfolio': credit_risk_rating,
                    'Raw Origination data': origination_data,
                    'Monthly data of active and delinquent A/C': monthly_data,
                    'GTV of underwritten data': gtv_data,
                    'Total invoice outstanding/repaid invoices': invoice_data,
                }.items():
                    if file_obj:
                        # file_name = os.path.basename(file_obj.name)
                        file_link = upload_to_google_drive(drive,file_obj)
                        file_links[field_name] = file_link
                        # file_link = upload_to_google_drive(file_obj.name, file_name)
                        # file_links[field_name] = file_link
                st.write(file_links.get('Incorporation Documents', ''))
                # Save the links in the database
                # Assuming `cursor` is a valid database cursor
                cursor.execute('''
                    INSERT INTO docs (
                        incorporation_docs,
                        subsidiary_docs,
                        licenses,
                        agreements,
                        financial_projections,
                        expenses_revenue_breakdown,
                        unit_economics,
                        debt_agreements,
                        investor_deck,
                        go_to_market_strategy,
                        customer_segments,
                        acquisition_funnel,
                        underwriting_policy,
                        credit_scorecard,
                        credit_lines_policy,
                        credit_risk_rating,
                        origination_data,
                        monthly_data,
                        gtv_data,
                        invoice_data,
                        additional_info,
                        constraints
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    file_links.get('Incorporation Documents', ''),
                    file_links.get('Subsidiary Registration and Ownership', ''),
                    file_links.get('Licenses', ''),
                    file_links.get('Agreements', ''),
                    file_links.get('Financial Projections', ''),
                    file_links.get('Current expenses and revenue breakdown', ''),
                    file_links.get('Unit Economics', ''),
                    file_links.get('Existing debt facility/lender agreements', ''),
                    file_links.get('Investor Deck with business strategy and performance', ''),
                    file_links.get('Go to market strategy', ''),
                    file_links.get('Key customer segments', ''),
                    file_links.get('Detailed acquisition funnel', ''),
                    file_links.get('Underwriting policy', ''),
                    file_links.get('Credit Scorecard', ''),
                    file_links.get('Credit Lines & Credit line increase policy', ''),
                    file_links.get('Credit Risk rating for the portfolio', ''),
                    file_links.get('Raw Origination data', ''),
                    file_links.get('Monthly data of active and delinquent A/C', ''),
                    file_links.get('GTV of underwritten data', ''),
                    file_links.get('Total invoice outstanding/repaid invoices', ''),
                    additional_info,
                    constraints,
                ))

                conn.commit()

                st.success('Data saved to Google Drive and database')

                # Display the table in DataFrame format
                st.header('Saved Data from the Database')
                df = pd.read_sql('SELECT * FROM docs', conn)
                st.dataframe(df)



            
            # submitted = st.button('Save to CSV')
            # if submitted:
            #     data = {
            #         'Incorporation Documents': os.path.basename(incorporation_docs.name) if incorporation_docs else '',
            #         'Subsidiary Registration and Ownership': os.path.basename(subsidiary_docs.name) if subsidiary_docs else '',
            #         'Licenses': os.path.basename(licenses.name) if licenses else '',
            #         'Agreements': os.path.basename(agreements.name) if agreements else '',
            #         'Financial Projections': os.path.basename(financial_projections.name) if financial_projections else '',
            #         'Expenses and Revenue Breakdown': os.path.basename(expenses_revenue_breakdown.name) if expenses_revenue_breakdown else '',
            #         'Unit Economics': os.path.basename(unit_economics.name) if unit_economics else '',
            #         'Debt Agreements': os.path.basename(debt_agreements.name) if debt_agreements else '',
            #         'Investor Deck': os.path.basename(investor_deck.name) if investor_deck else '',
            #         'Go to Market Strategy': os.path.basename(go_to_market_strategy.name) if go_to_market_strategy else '',
            #         'Customer Segments': os.path.basename(customer_segments.name) if customer_segments else '',
            #         'Acquisition Funnel': os.path.basename(acquisition_funnel.name) if acquisition_funnel else '',
            #         'Underwriting Policy': os.path.basename(underwriting_policy.name) if underwriting_policy else '',
            #         'Credit Scorecard': os.path.basename(credit_scorecard.name) if credit_scorecard else '',
            #         'Credit Lines Policy': os.path.basename(credit_lines_policy.name) if credit_lines_policy else '',
            #         'Credit Risk Rating': os.path.basename(credit_risk_rating.name) if credit_risk_rating else '',
            #         'Origination Data': os.path.basename(origination_data.name) if origination_data else '',
            #         'Monthly Data': os.path.basename(monthly_data.name) if monthly_data else '',
            #         'GTV Data': os.path.basename(gtv_data.name) if gtv_data else '',
            #         'Invoice Data': os.path.basename(invoice_data.name) if invoice_data else '',
            #         'Additional Info': additional_info,
            #         'Constraints': constraints
            #     }
            #     save_to_csv(data, 'data.csv')
            #     st.success('Data saved to data.csv')

            #     st.header('Saved Data from CSV')
            #     csv_data = pd.read_csv('data.csv')
            #     st.dataframe(csv_data)

            #     cursor.execute('''
            #         INSERT INTO documents (
            #             incorporation_docs,
            #             subsidiary_docs,
            #             licenses,
            #             agreements,
            #             financial_projections,
            #             expenses_revenue_breakdown,
            #             unit_economics,
            #             debt_agreements,
            #             investor_deck,
            #             go_to_market_strategy,
            #             customer_segments,
            #             acquisition_funnel,
            #             underwriting_policy,
            #             credit_scorecard,
            #             credit_lines_policy,
            #             credit_risk_rating,
            #             origination_data,
            #             monthly_data,
            #             gtv_data,
            #             invoice_data,
            #             additional_info,
            #             constraints
            #         ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            #     ''', (
            #         incorporation_docs.read(),
            #         subsidiary_docs.read(),
            #         licenses.read(),
            #         agreements.read(),
            #         financial_projections.read(),
            #         expenses_revenue_breakdown.read(),
            #         unit_economics.read(),
            #         debt_agreements.read(),
            #         investor_deck.read(),
            #         go_to_market_strategy.read(),
            #         customer_segments.read(),
            #         acquisition_funnel.read(),
            #         underwriting_policy.read(),
            #         credit_scorecard.read(),
            #         credit_lines_policy.read(),
            #         credit_risk_rating.read(),
            #         origination_data.read(),
            #         monthly_data.read(),
            #         gtv_data.read(),
            #         invoice_data.read(),
            #         additional_info,
            #         constraints
            #     ))

            #     conn.commit()

        
        main()
            
    if opt == "Borrower Profile":
        conn = sqlite3.connect('my_db.db')

        # Load borrower's document links from the database
        df = pd.read_sql('SELECT * FROM docs', conn)
    
        # Function to get the selected borrower data based on ID
        def get_selected_borrower_data(selected_id):
            selected_data = df[df['id'] == selected_id]
            return selected_data



        # ID selector
        st.sidebar.header('Select Borrower ID')
        selected_id = st.sidebar.selectbox('Select ID:', df['id'])

        # Get selected borrower data based on ID
        selected_data = get_selected_borrower_data(selected_id)
        

        bd_df = pd.read_csv("company_det.csv")
        bd_columns = bd_df.columns.tolist()
        bd_df = bd_df.iloc[int(selected_id)]
        bd_num_cols_per_set = 5

        # Assuming you have a DataFrame named "bd_df" with columns in "bd_columns"
        # bd_df = pd.read_csv("company_det.csv")
        # bd_df = bd_df.iloc[0]
        # bd_num_cols_per_set = 5

 

        # Define CSS styles for the blocks
        block1_style = """
            padding: 20px;
            border: 1px solid #ccc;
            border-radius: 5px;
            margin-right: 10px;
            background-color: #f2f2f2;
        """

        block2_style = """
            padding: 20px;
            border: 1px solid #ccc;
            border-radius: 5px;
            margin-left: 10px;
            background-color: #f7f7f7;
        """

        # Create the layout using columns
        kp1,kp2,kp3=st.columns(3)
        block1, block2 = st.columns(2)

        
        kp1.markdown(f"""
            <div style="padding: 20px;
            border: 1px solid #ccc;
            border-radius: 5px;
            margin-left: 0px;
            background-color: #f7f7f7;"><h3>Company Name: {bd_df.iloc[3]}</h1></div>
            <p>""",unsafe_allow_html=True)
        kp2.markdown(f"""
            <div style="{block2_style}"><h3>Credit Rating: {bd_df.iloc[11]}</h1></div>
            <p>""",unsafe_allow_html=True)
        kp3.markdown(f"""
            <div style="{block2_style}"><h3>Credit Score: {bd_df.iloc[12]}</h1></div>
            <p>""",unsafe_allow_html=True)

        # Generate HTML content with embedded data using .iloc
        block1_content = f"""
            <div style="{block1_style}">
                """
        # Fetch column names and values dynamically
        for i in range(4, 11):
            col_name = bd_df.index[i]
            col_value = bd_df.iloc[i]
            block1_content += f"<p><strong>{col_name}:</strong> {col_value}</p>\n"

        block1_content += "</div>"

        block2_content = f"""
            <div style="{block2_style}">
                """
        # Fetch column names and values dynamically
        for i in range(13, 20):
            col_name = bd_df.index[i]
            col_value = bd_df.iloc[i]
            block2_content += f"<p><strong>{col_name}:</strong> {col_value}</p>\n"

        block2_content += "</div>"

        # Render the HTML content using Streamlit's st.markdown() function
        block1.markdown(block1_content, unsafe_allow_html=True)
        block2.markdown(block2_content, unsafe_allow_html=True)



        st.header('Borrower Documents')
        columns = df.columns.tolist()
        columns.remove('id')  # Remove the 'id' column from the list of columns
        columns.remove('additional_info')
        columns.remove('constraints')
        # Split the columns into four sets for displaying in four columns
        num_cols_per_set = 4
        column_sets = [columns[i:i+num_cols_per_set] for i in range(0, len(columns), num_cols_per_set)]


        # Display four sets of four columns each
        for col_set in column_sets:
            col1, col2, col3, col4 = st.columns(4)
            for col, column in zip([col1, col2, col3, col4], col_set):
                with col:
                    # st.write(f"**{column}:**")
                    link = selected_data.at[selected_data.index[0], column]
                    st.markdown(f"""
                    <div style="{block2_style}"><h4>{column}</h4><p><a href={link}>{link}</a>
                    </div>
                    <p>""",unsafe_allow_html=True)

                    
                    # if link:
                    #     st.image("https://mailmeteor.com/logos/assets/PNG/Google_Drive_Logo_512px.png", width=20)
                    #     st.markdown(f'<a style="text-decoration:none; border: 1px solid #ccc; border-radius: 5px; background-color: #f9f9f9; padding: 5px 10px; color: #000;" href="{link}">{link}</a>', unsafe_allow_html=True)

        # Additional information and constraints
        bll1,bll2=st.columns(2)
        bll1.header('Additional Information')
        bll1.markdown(f"""
                    <div style="{block2_style}"><h4>{selected_data.at[selected_data.index[0], 'additional_info']}</h4>
                    """,unsafe_allow_html=True)

        bll2.header('Constraints and Considerations')
        bll2.markdown(f"""
                    <div style="{block2_style}"><h4>{selected_data.at[selected_data.index[0], 'constraints']}</h4>
                   """,unsafe_allow_html=True)
        
        


        # Define CSS styles for tiles (replace with actual styles)
        tile_style_1 = """
            .section-tile {
                padding: 20px;
                margin-bottom: 20px;
                background-color: #f9f9f9;
            }
            .section-title {
                font-size: 1.6em;
                font-weight: bold;
                color:Blue;
                margin-bottom: 10px;
            }
            .property {
                margin: 5px 0;
                font-size: 1.4em;
                margin-bottom: 10px;
                padding: 20px;
                background-color: #f9f9f9;
            }
            .property-name {
                font-weight: bold;
                font-size: 1.2em;
            }
            .property-value {
                margin-left: 10px;
                font-size: 1.2em;
            }
        """

        # # Sample JSON data
        # f1=open('borrower_details.json')
        # sample_data= json.load(f1)

        # # # Apply custom CSS styles
        # st.markdown(f'<style>{tile_style_1}</style>', unsafe_allow_html=True)

        # # Display JSON data in section
        # flag="left"
        # c1,c2=st.columns(2)
        # for section_title, section_data in sample_data.items():
        #     prop_content=f"""
        #         <div class="section-tile">
        #             <div class="section-title">{section_title}</div>
        #             <div style="property">
        #         """
            
        #     for property_name, property_value in section_data.items():
        #         # prop_content+=f"""<span class="property-name">{property_name}: {property_value}</span><p>"""
        #         prop_content+=f"""<span class="property-name">{property_name}: </span>
        #         <span class="property-name">{property_value}</span><br>"""

        #     prop_content += "</div>"
        #     if flag=="left":
        #         with c1:
        #             st.markdown(prop_content, unsafe_allow_html=True)
        #             flag="right"
        #     else:
        #         with c2:
        #             st.markdown(prop_content, unsafe_allow_html=True)
        #             flag="left"
       
     
        # Define CSS styles for tiles (replace with actual styles)
        tile_style = """
            .section-tile {
                padding: 20px;
                border: 1px solid #ccc;
                margin-bottom: 20px;
                background-color: #f9f9f9;
            }
            .section-title {
                font-size: 1.2em;
                font-weight: bold;
                margin-bottom: 10px;
            }
            .property {
                margin: 5px 0;
            }
            .property-name {
                font-weight: bold;
            }
            .property-value {
                margin-left: 10px;
            }
        """

        # Sample data for tabular records
        accounts_data = pd.DataFrame({
            "Account Holder Name": ["Unimoni Account 1","Unimoni Account 2","Unimoni Account 3","Unimoni Account 4"],
            "Bank Name": ["State Bank of India", "Axis Bank", "HDFC Bank", "ICICI Bank"],
            "Account Number": ["143345908", "0139001712", "330718349", "955003921"],
            "Balance($)": [100000, 120000, 80000, 150000],
            "Account Type": ["Savings", "Current", "Savings", "Current"],
            "Age": [10, 8, 5, 3]
        })

        # Create a sample line chart data
        date_range = pd.date_range(start="2022-01-01", end="2022-12-31", freq="M")
        line_chart_data = pd.DataFrame({
            "Date": date_range,
            "Balance": np.random.randint(50000, 200000, len(date_range)),
            "Average Balance": np.random.randint(60000, 150000, len(date_range)),
            "Credit Amount": np.random.randint(10000, 300000, len(date_range)),
            "Debit Amount": np.random.randint(40000, 200000, len(date_range)),
            "Debit Tx Count": np.random.randint(10, 50, len(date_range)),
            "Credit Tx Count": np.random.randint(10, 50, len(date_range))
        })

        # # Streamlit app
        # st.title("Bank Statement Analysis")
       
        # Apply custom CSS styles
        st.markdown(f'<style>{tile_style_1}</style>', unsafe_allow_html=True)

        # Display tabular records
        table_data=f"""
            <div class="section-tile">
                <div class="section-title">Bank Accounts</div>
                <div class="property">
                    <table>
                        <tr>
                            <th>Account Holder Name</th>
                            <th>Bank Name</th>
                            <th>Account Number</th>
                            <th>Balance($)</th>
                            <th>Account Type</th>
                            <th>Age</th>
                        </tr>"""

        for _, row in accounts_data.iterrows():
            table_data+=f"""<tr>
                    <td>{row['Account Holder Name']}</td>
                    <td>{row['Bank Name']}</td>
                    <td>{row['Account Number']}</td>
                    <td>{row['Balance($)']}</td>
                    <td>{row['Account Type']}</td>
                    <td>{row['Age']}</td>
                </tr>"""

        table_data+=f"""
                    </table>
                </div>
            </div>
            """
        # st.markdown(table_data,unsafe_allow_html=True)

        expander = st.expander("Bank Statement Analysis",expanded=True)
        expander.markdown(table_data,unsafe_allow_html=True)

        expander.subheader("Line Chart: Account Metrics")
        expander.line_chart(line_chart_data.set_index("Date"))

        # Display line chart
        # st.markdown("""
        #     <div class="section-tile">
        #         <div class="section-title">Line Chart: Account Metrics</div>
        #             <img src="data:image/png;base64,{}" alt="Line Chart">
        #     </div>
        #     """.format(st.line_chart(line_chart_data.set_index("Date"))), unsafe_allow_html=True)

        # Display detailed analysis metrics
        expander.markdown("""
            <div class="section-tile">
                <div class="section-title">Detailed Analysis Metrics (Last 6 Months)</div>
                <div class="property">
                    <div>Total credit transactions: 120</div>
                    <div>Total I/W check bounce (12 months): 7</div>
                    <div>Total debit transactions: 80</div>
                    <div>Total O/W check bounce (12 months): 0</div>
                    <div>Total online transactions: 200</div>
                    <div>Total offline transactions: 50</div>
                    <div>Total I/W check bounce (3 months): 2</div>
                    <div>Total O/W check bounce (6 months): 0</div>
                    <div>Average Bank Balance: $100,000</div>
                    <div>Average Eod balance: $95,000</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

      

        # Define CSS styles for tiles (replace with actual styles)
        tile_style = """
            .section-tile {
                padding: 20px;
                border: 1px solid #ccc;
                margin-bottom: 20px;
                background-color: #f9f9f9;
            }
            .section-title {
                font-size: 1.2em;
                font-weight: bold;
                margin-bottom: 10px;
            }
            .property {
                margin: 5px 0;
            }
            .property-name {
                font-weight: bold;
            }
            .property-value {
                margin-left: 10px;
            }
        """

        # Sample data for metrics
        metrics_data = pd.DataFrame({
            "Metric": ["Gross Turnover", "Net Turnover", "Total Clients", "Total Invoices",
                    "Gross Purchases", "Net Purchases", "Gross Margin", "Gross Margin(%)"],
            "FY 2022-23": [750000, 600000, 120, 180, 300000, 240000, 450000, 60],
            "FY 2021-22": [650000, 500000, 110, 160, 250000, 200000, 400000, 58]
        })

        # Create sample line chart data
        date_range = pd.date_range(start="2022-01-01", end="2022-12-31", freq="M")
        line_chart_data = pd.DataFrame({
            "Date": date_range,
            "Total volume": np.random.randint(500, 2000, len(date_range)),
            "Intra organization volume": np.random.randint(100, 800, len(date_range)),
            "Related Party volume": np.random.randint(50, 300, len(date_range))
        })

        # Create sample pie chart data
        pie_chart_data = pd.DataFrame({
            "Distribution": ["B2B", "B2C", "B2B2C"],
            "Percentage": [40, 30, 30]
        })

        # Streamlit app
        expander = st.expander("Tax Returns Analysis",expanded=True)

        # Apply custom CSS styles
        st.markdown(f'<style>{tile_style}</style>', unsafe_allow_html=True)

        # Display metrics for FY 2022-23 and FY 2021-22

        col1, col2 = expander.columns(2)

        col1.markdown("""
            <div class="section-tile">
                <div class="section-title">Metrics for FY 2022-23</div>
                <div class="property">
                    {}
                </div>
            </div>
            """.format(metrics_data.to_html(index=False)), unsafe_allow_html=True)


        with col2:
            st.subheader("Line Chart: Business Volume")
            st.line_chart(line_chart_data.set_index("Date"))

    

        # Display pie chart
        # st.markdown("""
        #     <div class="section-tile">
        #         <div class="section-title">Pie Chart: Distribution Across Borrowers</div>
        #         <div class="property">
        #             <img src="data:image/png;base64,{}" alt="Pie Chart">
        #         </div>
        #     </div>
        #     """.format(st.pie_chart(pie_chart_data.set_index("Distribution"))), unsafe_allow_html=True)

        m1,m2=expander.columns(2)
        # Display structured data for Business Transaction Summary
        m1.markdown("""
            <div class="section-tile">
                <div class="section-title">Business Transaction Summary (Last 3 FY)</div>
                <div class="property">
                    <table>
                        <tr>
                            <th>Metric</th>
                            <th>2020-21</th>
                            <th>2021-22</th>
                            <th>2022-23</th>
                        </tr>
                        <tr>
                            <td>Gross Turnover</td>
                            <td>500000</td>
                            <td>600000</td>
                            <td>750000</td>
                        </tr>
                        <tr>
                            <td>Net Turnover</td>
                            <td>450000</td>
                            <td>550000</td>
                            <td>700000</td>
                        </tr>
                        <tr>
                            <td>Total invoices raised</td>
                            <td>100</td>
                            <td>130</td>
                            <td>150</td>
                        </tr>
                        <!-- Add more rows -->
                    </table>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # col2.markdown("<p><br><br><br><br>",unsafe_allow_html=True)
        # Display structured data for Total Tax Liability
        m2.markdown("""
            <div class="section-tile">
                <div class="section-title">Total Tax Liability (Last 3 FY)</div>
                <div class="property">
                    <table>
                        <tr>
                            <th>Metric</th>
                            <th>2020-21</th>
                            <th>2021-22</th>
                            <th>2022-23</th>
                        </tr>
                        <tr>
                            <td>Total liability paid</td>
                            <td>30000</td>
                            <td>35000</td>
                            <td>40000</td>
                        </tr>
                        <tr>
                            <td>State GST amount payable</td>
                            <td>5000</td>
                            <td>6000</td>
                            <td>7000</td>
                        </tr>
                        <tr>
                            <td>Integrated GST amount payable</td>
                            <td>6000</td>
                            <td>7000</td>
                            <td>8000</td>
                        </tr>
                        <!-- Add more rows -->
                    </table>
                </div>
            </div>
            """, unsafe_allow_html=True)




       
        # Define CSS styles for tiles (replace with actual styles)
        tile_style = """
            .section-tile {
                padding: 20px;
                border: 1px solid #ccc;
                margin-bottom: 20px;
                background-color: #f9f9f9;
            }
            .section-title {
                font-size: 1.2em;
                font-weight: bold;
                margin-bottom: 10px;
            }
            .property {
                margin: 5px 0;
            }
            .property-name {
                font-weight: bold;
            }
            .property-value {
                margin-left: 10px;
            }
        """

        # Sample data for income statement details
        income_statement_data = pd.DataFrame({
            "Audited Status": ["Audited", "Audited", "Audited"],
            "Filling Date": ["2023-05-15", "2022-04-20", "2021-03-10"],
            "Gap in Filings": [0, 1, 2]
        })

        # Sample data for ratios across last 3FY
        ratios_data = pd.DataFrame({
            "Ratio": ["ISCR", "DSCR", "PAT", "D/E Ratio", "Adjusted D/E"],
            "2020-21": [1.5, 2.0, 50000, 0.8, 0.9],
            "2021-22": [1.6, 2.2, 60000, 0.7, 0.8],
            "2022-23": [1.8, 2.5, 70000, 0.6, 0.7]
        })

        # # Sample data for revenue growth
        # revenue_growth_data = pd.DataFrame({
        #     "Year": ["2020-21", "2021-22", "2022-23"],
        #     "Revenue Growth (%)": [15, 12, 18]
        # })

        # Sample data for quarterly revenue with gradual growth
        revenue_growth_data = pd.DataFrame({
        "Quarter": ["2020-03-31", "2020-06-30", "2020-09-30", "2020-12-31",
                    "2021-03-31", "2021-06-30", "2021-09-30", "2021-12-31",
                    "2022-03-31", "2022-06-30", "2022-09-30", "2022-12-31"],
        "Revenue ($)": [500000, 600000, 1200000, 1900000, 2500000, 3000000, 3350000, 4000000,
                        4500000, 5000000, 6000000, 7500000]
            })

        # Sample data for financial statement
        # Placeholder data; replace with actual financial statement data
        financial_statement_data = pd.DataFrame({
            "Item": ["Revenue from Operations (Net)", "Expenses", "EBITDA", "Finance Cost", "Interest Expense paid to Partner / Director", "Profit / (Loss) before tax"],
            "2020-21": [400000, -280000, 120000, -20000, -5000, 100000],
            "2021-22": [450000, -300000, 150000, -25000, -6000, 125000],
            "2022-23": [500000, -320000, 180000, -28000, -7000, 150000]
        })

        # Sample data for financial trends
        # Placeholder data; replace with actual financial trends data
        financial_trends_data = pd.DataFrame({
            "Trend": ["Sales growth over previous year", "Trend on EBIDTA over previous year", "Trend in inventory holding period over previous year",
                    "Trend in Creditor period over previous year", "Trend in Receivables period over previous year",
                    "Increase in working capital cycle over previous year", "Improvement in ATNW over previous year"],
            "Value": [10, 5, 7, -3, 2, 4, 8]
        })


        # Apply custom CSS styles
        st.markdown(f'<style>{tile_style}</style>', unsafe_allow_html=True)
        expander=st.expander("Financials Analysis",expanded=False)
        m11,m12=expander.columns(2)
        # Display income statement details
        m11.markdown("""
            <div class="section-tile">
                <div class="section-title">Income Statement Details (Last 3 FY)</div>
                <div class="property">
                    {}
                </div>
            </div>
            """.format(income_statement_data.to_html(index=False)), unsafe_allow_html=True)

        # Display ratios across last 3FY
     
        # col1, col2 = st.columns(2)

        m12.markdown("""
            <div class="section-tile">
                <div class="section-title">Ratios Across Last 3FY</div>
                <div class="property">
                    {}
                </div>
            </div>
            """.format(ratios_data.to_html(index=False)), unsafe_allow_html=True)

        # Display revenue growth chart
        expander.subheader("Revenue Growth Chart")
        expander.line_chart(revenue_growth_data.set_index("Quarter"))
       
        
        m13,m14=expander.columns(2)
        # Display financial statement
        m13.markdown("""
            <div class="section-tile">
                <div class="section-title">Financial Statement (Last 3 FY)</div>
                <div class="property">
                    {}
                </div>
            </div>
            """.format(financial_statement_data.to_html(index=False)), unsafe_allow_html=True)

        # Display financial trends
        m14.markdown("""
            <div class="section-tile">
                <div class="section-title">Financial Trends (Last 3 FY)</div>
                <div class="property">
                    {}
                </div>
            </div>
            """.format(financial_trends_data.to_html(index=False)), unsafe_allow_html=True)

        # Display liabilities section
        # Placeholder data; replace with actual liabilities data
        liabilities_data = pd.DataFrame({
            "Item": ["Total Old Liabilities", "Other Old Liabilities", "Other Current Liabilities", "Total Current Liabilities", "Total Equity and Liabilities"],
            "2020-21": [50000, 20000, 30000, 70000, 120000],
            "2021-22": [55000, 25000, 35000, 75000, 130000],
            "2022-23": [60000, 28000, 40000, 80000, 140000]
        })

        m13.markdown("""
            <div class="section-tile">
                <div class="section-title">Liabilities (Last 3 FY)</div>
                <div class="property">
                    {}
                </div>
            </div>
            """.format(liabilities_data.to_html(index=False)), unsafe_allow_html=True)

        # Display assets section
        # Placeholder data; replace with actual assets data
        assets_data = pd.DataFrame({
            "Item": ["Net Fixed Assets", "Investments In Subsidiaries/ Associates", "Non Current Investments", "Deferred tax assets (net)", "Intangible assets", "Intangible assets under development"],
            "2020-21": [250000, 50000, 75000, 20000, 10000, 5000],
            "2021-22": [280000, 60000, 80000, 25000, 12000, 6000],
            "2022-23": [320000, 70000, 85000, 28000, 15000, 7500]
        })

        m14.markdown("""
            <div class="section-tile">
                <div class="section-title">Assets (Last 3 FY)</div>
                <div class="property">
                    {}
                </div>
            </div>
            """.format(assets_data.to_html(index=False)), unsafe_allow_html=True)

        # Display ratios section
        # Placeholder data; replace with actual ratio data
        ratios_table_data = pd.DataFrame({
            "Ratio": ["Current ratio", "TOL/TNW", "TOL/ATNW", "Inventory Turnover days", "Account payable days",
                    "Account receivable days", "Total assets turnover", "Adjusted debt to equity",
                    "Interest coverage ratio", "LTD/NCA", "Operating profit margin", "Net profit margin",
                    "Sales/ Total Assets", "Net Profit/ Total Assets", "Cash profit ratio", "Gross profit margin",
                    "DSCR", "Operating cash Flow/ Sales", "Net Debt/EBITDA"],
            "2020-21": [0.986, 21.56 ,21.56 ,0 ,55.056 ,35.694 ,3.383 ,0 ,13.642 ,0 ,7.38 ,0.19 ,3.383 ,0.006 ,-0.003 ,45.10, 0, 0, -2.173],
            "2021-22": [1.024, 19.28 ,19.28 ,20.897 ,25.456 ,25.412 ,3.812 ,0,132.243 ,0 ,5.96 ,0.31 ,3.812 ,0.012 ,-0.002 ,32.17 ,132.243 ,0.28, -0.273],
            "2022-23": [1.034, 26.442, 26.442, 8.466, 22.742, 30.497, 3.019, 0, 373.214, 0, -2.57, 0.79, 3.019, 0.024, 0.007, 15.90, 373.214, 14.74, 7.27]
                            })

        expander.markdown("""
            <div class="section-tile">
                <div class="section-title">Ratios (Last 3 FY)</div>
                <div class="property">
                    {}
                </div>
            </div>
            """.format(ratios_table_data.to_html(index=False)), unsafe_allow_html=True)





      

        # Define CSS styles for the report (replace with actual styles)
        report_style = """
            .report {
                padding: 20px;
                border: 1px solid #ccc;
                background-color: #f9f9f9;
            }
            .report-title {
                font-size: 1.5em;
                font-weight: bold;
                margin-bottom: 10px;
            }
            .section {
                margin-bottom: 20px;
            }
            .section-title {
                font-size: 1.2em;
                font-weight: bold;
                margin-bottom: 10px;
            }
            .property {
                margin: 5px 0;
            }
            .property-name {
                font-weight: bold;
            }
            .property-value {
                margin-left: 10px;
            }
        """


        # Apply custom CSS styles
        st.markdown(f'<style>{report_style}</style>', unsafe_allow_html=True)
        expander=st.expander("Credit Rating/Credit Bureau Analysis",expanded=False)
        # Report title
        m15,m16=expander.columns(2)

        with m15:
            # Business Information
            st.markdown('<div class="section"><div class="section-title">Business Information</div>', unsafe_allow_html=True)
            st.markdown('<div class="property"><span class="property-name">Business Name:</span><span class="property-value">ABC Corporation</span></div>', unsafe_allow_html=True)
            st.markdown('<div class="property"><span class="property-name">Registration Number:</span><span class="property-value">123456789</span></div>', unsafe_allow_html=True)
            st.markdown('<div class="property"><span class="property-name">Address:</span><span class="property-value">123 Main St, City</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # Credit Summary
            st.markdown('<div class="section"><div class="section-title">Credit Summary</div>', unsafe_allow_html=True)
            st.markdown('<div class="property"><span class="property-name">Total Outstanding Amount:</span><span class="property-value">$100,000</span></div>', unsafe_allow_html=True)
            st.markdown('<div class="property"><span class="property-name">Total Available Credit:</span><span class="property-value">$200,000</span></div>', unsafe_allow_html=True)
            st.markdown('<div class="property"><span class="property-name">Credit Utilization Ratio:</span><span class="property-value">50%</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with m16:
            # Credit History
            st.markdown('<div class="section"><div class="section-title">Credit History</div>', unsafe_allow_html=True)
            st.markdown('<div class="property"><span class="property-name">Last Payment Date:</span><span class="property-value">2023-07-15</span></div>', unsafe_allow_html=True)
            st.markdown('<div class="property"><span class="property-name">Credit Score:</span><span class="property-value">750</span></div>', unsafe_allow_html=True)
            st.markdown('<div class="property"><span class="property-name">Late Payments (Last 12 Months):</span><span class="property-value">2</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # Credit Accounts
            st.markdown('<div class="section"><div class="section-title">Credit Accounts</div>', unsafe_allow_html=True)
            st.markdown('<div class="property"><span class="property-name">Account 1:</span><span class="property-value">Loan Account - $50,000</span></div>', unsafe_allow_html=True)
            st.markdown('<div class="property"><span class="property-name">Account 2:</span><span class="property-value">Credit Card - $10,000</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # End of report
            st.markdown('</div>', unsafe_allow_html=True)



        # Define CSS styles for the report (replace with actual styles)
        report_style = """
            .report {
                padding: 20px;
                border: 1px solid #ccc;
            }
            .section {
                margin-bottom: 20px;
            }
            .section-title {
                font-size: 1.2em;
                font-weight: bold;
                margin-bottom: 10px;
            }
            .property {
                margin: 5px 0;
                border-bottom: 1px solid #ccc;
                padding: 5px 0;
            }
            .property-name {
                font-weight: bold;
                display: inline-block;
                width: 300px;
            }
            .property-value {
                display: inline-block;
                width: 200px;
            }
            .blue-bg {
                background-color: #e6f7ff;
            }
            .yellow-bg {
                background-color: #fff6cc;
            }
            .red-bg {
                background-color: #ffd9cc;
            }
        """

        # Apply custom CSS styles
        st.markdown(f'<style>{report_style}</style>', unsafe_allow_html=True)

        # Report title
        # st.markdown('<div class="report">', unsafe_allow_html=True)

        cm1,cm2,cm3=expander.columns(3)


        # 3-column structure
        with cm1:
            st.markdown('<div class="section">', unsafe_allow_html=True)
            st.markdown('<div class="blue-bg property"><span class="property-name">CIBIL Score:</span><span class="property-value">797</span></div>', unsafe_allow_html=True)
            st.markdown('<div class="blue-bg property"><span class="property-name">Total Number of Accounts:</span><span class="property-value">13</span></div>', unsafe_allow_html=True)
            st.markdown('<div class="blue-bg property"><span class="property-name">Open Accounts:</span><span class="property-value">10</span></div>', unsafe_allow_html=True)
            st.markdown('<div class="blue-bg property"><span class="property-name">Closed Accounts:</span><span class="property-value">3</span></div>', unsafe_allow_html=True)
            st.markdown('<div class="blue-bg property"><span class="property-name">Enquiries in last 30 days:</span><span class="property-value">6</span></div>', unsafe_allow_html=True)
            st.markdown('<div class="blue-bg property"><span class="property-name">Enquiries past 12 Months:</span><span class="property-value">12</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with cm2:
            st.markdown('<div class="section">', unsafe_allow_html=True)
            st.markdown('<div class="yellow-bg property"><span class="property-name">DPD over 30 days in last 12 months:</span><span class="property-value">0</span></div>', unsafe_allow_html=True)
            st.markdown('<div class="yellow-bg property"><span class="property-name">DPD over 60 days in last 12 months:</span><span class="property-value">0</span></div>', unsafe_allow_html=True)
            st.markdown('<div class="yellow-bg property"><span class="property-name">DPD over 30 days in last 24 months:</span><span class="property-value">0</span></div>', unsafe_allow_html=True)
            st.markdown('<div class="yellow-bg property"><span class="property-name">DPD over 60 days in last 24 months:</span><span class="property-value">0</span></div>', unsafe_allow_html=True)
            st.markdown('<div class="yellow-bg property"><span class="property-name">Max delinquecy over lifetime:</span><span class="property-value">-1</span></div>',unsafe_allow_html=True)
            st.markdown('<div class="yellow-bg property"><span class="property-name">Delay:</span><span class="property-value">1 month</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with cm3:
            st.markdown('<div class="section">', unsafe_allow_html=True)
            st.markdown('<div class="red-bg property"><span class="property-name">Max overdue over last 12 months:</span><span class="property-value">762</span></div>', unsafe_allow_html=True)
            st.markdown('<div class="red-bg property"><span class="property-name">Total Overdue:</span><span class="property-value">18</span></div>', unsafe_allow_html=True)
            st.markdown('<div class="red-bg property"><span class="property-name">Total Settled Amount - Applicant</span><span class="property-value">18</span></div>', unsafe_allow_html=True)
            st.markdown('<div class="red-bg property"><span class="property-name">Total Write Offs:</span><span class="property-value">9</span></div>', unsafe_allow_html=True)
            st.markdown('<div class="red-bg property"><span class="property-name">Recovered Amount:</span><span class="property-value">-1</span></div>', unsafe_allow_html=True)
            st.markdown('<div class="red-bg property"><span class="property-name">View Report:</span><span class="property-value">Link to Report</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # End of report
        st.markdown('</div>', unsafe_allow_html=True)


        expander=st.expander("Portfolio Analysis",expanded=False)
    
        # Define CSS styles for the report (replace with actual styles)
        report_style = """
            .report {
                padding: 20px;
                border: 1px solid #ccc;
            }
            .section {
                margin-bottom: 20px;
            }
            .section-title {
                font-size: 1.2em;
                font-weight: bold;
                margin-bottom: 10px;
            }
            .property {
                margin: 5px 0;
                border-bottom: 1px solid #ccc;
                padding: 5px 0;
            }
            .property-name {
                font-weight: bold;
                display: inline-block;
                width: 200px;
            }
            .property-value {
                display: inline-block;
            }
            .chart {
                display: inline-block;
                vertical-align: top;
            }
        """

     

        # Apply custom CSS styles
        st.markdown(f'<style>{report_style}</style>', unsafe_allow_html=True)

      
        # 2 columns structure
        clmn1,clmn2=expander.columns(2)
        with clmn1:
            st.markdown('<div class="section">', unsafe_allow_html=True)
            st.markdown('<div class="property"><span class="property-name">Total:</span><span class="property-value">20</span></div>', unsafe_allow_html=True)
            st.markdown('<div class="property"><span class="property-name">DPD:</span><span class="property-value">2</span></div>', unsafe_allow_html=True)
            st.markdown('<div class="property"><span class="property-name">NPA:</span><span class="property-value">150</span></div>', unsafe_allow_html=True)
            st.markdown('<div class="property"><span class="property-name">Write Off:</span><span class="property-value">72</span></div>', unsafe_allow_html=True)
            st.markdown('<div class="property"><span class="property-name">Accounts:</span><span class="property-value">$9,17,70,925.41</span></div>', unsafe_allow_html=True)
            st.markdown('<div class="property"><span class="property-name">Charges:</span><span class="property-value">$64,589.64</span></div>', unsafe_allow_html=True)
            st.markdown('<div class="property"><span class="property-name">Revenue:</span><span class="property-value">$60,575.73</span></div>', unsafe_allow_html=True)
            st.markdown('<div class="property"><span class="property-name">Interest:</span><span class="property-value">$511.09</span></div>', unsafe_allow_html=True)
            st.markdown('<div class="property"><span class="property-name">Penal:</span><span class="property-value">$2.64</span></div>', unsafe_allow_html=True)
            st.markdown('<div class="property"><span class="property-name">Principal Bounces:</span><span class="property-value">3</span></div>', unsafe_allow_html=True)
            st.markdown('<div class="property"><span class="property-name">Amount Received:</span><span class="property-value">2</span></div>', unsafe_allow_html=True)
            st.markdown('<div class="property"><span class="property-name">Principal Disbursed:</span><span class="property-value">2</span></div>', unsafe_allow_html=True)
            st.markdown('<div class="property"><span class="property-name">Outstanding:</span><span class="property-value">$2,30,004.91</span></div>', unsafe_allow_html=True)
            st.markdown('<div class="property"><span class="property-name">Waive Off:</span><span class="property-value">1,000</span></div>', unsafe_allow_html=True)
            st.markdown('<div class="property"><span class="property-name">Amount Generated:</span><span class="property-value">$55,112.64</span></div>', unsafe_allow_html=True)
            st.markdown('<div class="property"><span class="property-name">Overdue:</span><span class="property-value">0</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="section">', unsafe_allow_html=True)
         

            # Create example bar chart (Amount Disbursed, Principal Received, etc.)
            categories = ['Disbursed', 'Principal Received', 'Principal Outstanding', 'Bounces', 'Overdue Amount', 'NOC Generated']
            values = [230004.91, 2628525, 2398520.09, 2, 2368520.09, 2]
            plt.figure(figsize=(8, 4))
            plt.barh(categories, values, color='skyblue')
            plt.xlabel('Amount')
            plt.title('Loan Performance')
            st.pyplot(plt)



        with clmn2:
            # Create example pie chart 1 (DPD vs NPA vs Write Off)
            labels = ['DPD', 'NPA', 'Write Off']
            sizes = [2, 150, 72]
            plt.figure(figsize=(2, 2))
            plt.pie(sizes, labels=labels, autopct='%1.1f%%',textprops={'fontsize': 7}, startangle=140, colors=['#66b3ff','#99ff99','#ff9999'])
            plt.title('Account Status',fontsize=5)
            st.pyplot(plt)

            # Create example pie chart 2 (Charge vs Penal vs Interest)
            labels = ['Charge', 'Penal', 'Interest']
            sizes = [64589.64, 2.64, 60575.73]
            plt.figure(figsize=(2, 2))
            plt.pie(sizes, labels=labels, autopct='%1.1f%%',textprops={'fontsize': 7} ,startangle=140, colors=['#66b3ff','#99ff99','#ff9999'])
            plt.title('Revenue Breakdown',fontsize=5)
            st.pyplot(plt)


        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # End of report
        st.markdown('</div>', unsafe_allow_html=True) 


        
        k1,k2=expander.columns(2)

        with k1:
            #Product Analysis
            st.markdown('<div class="section">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Product Analysis</div>', unsafe_allow_html=True)
            st.markdown('<div class="property"><span class="property-name">Current Loan:</span><span class="property-value">9,29,81,263</span></div>', unsafe_allow_html=True)
            st.markdown('<div class="property"><span class="property-name">Restructured:</span><span class="property-value">4</span></div>', unsafe_allow_html=True)
            st.markdown('<div class="property"><span class="property-name">Re-KYC:</span><span class="property-value">0</span></div>', unsafe_allow_html=True)
            st.markdown('<div class="property"><span class="property-name">DPD:</span><span class="property-value">72</span></div>', unsafe_allow_html=True)
            st.markdown('<div class="property"><span class="property-name">Written Offs:</span><span class="property-value">9,17,70,925.41</span></div>', unsafe_allow_html=True)
            st.markdown('<div class="property"><span class="property-name">Zero Balance:</span><span class="property-value">0</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="section">', unsafe_allow_html=True)

             # Application Analysis
          

        with k2:
            # Portfolio Distribution Pie Chart
            st.markdown('<div class="chart">', unsafe_allow_html=True)
            # Create a pie chart for portfolio distribution
            portfolio_labels = ['Healthy', 'Moderate', 'Critical']
            portfolio_sizes = [30, 40, 30]
            portfolio_colors = ['#5cb85c', '#f0ad4e', '#d9534f']

            plt.figure(figsize=(1.5, 1.5))
            plt.pie(portfolio_sizes, labels=portfolio_labels,textprops={'fontsize': 7}, colors=portfolio_colors, autopct='%1.1f%%', startangle=140)
            plt.title('Portfolio Distribution',fontsize=5)
            st.pyplot(plt)
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)


          
        cmm1,cmm2=expander.columns(2)

        with cmm1:
            #appln analysis
            st.markdown('<div class="section">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Application Analysis</div>', unsafe_allow_html=True)

            # Create a dummy data line chart for monthly application analysis
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            received = np.random.randint(50, 150, size=12)
            in_process = np.random.randint(20, 100, size=12)
            disbursed = np.random.randint(10, 80, size=12)
            closed = np.random.randint(5, 50, size=12)

            plt.figure(figsize=(10, 6))
            plt.plot(months, received, marker='o', label='Received')
            plt.plot(months, in_process, marker='o', label='In Process')
            plt.plot(months, disbursed, marker='o', label='Disbursed')
            plt.plot(months, closed, marker='o', label='Closed')
            plt.xlabel('Month')
            plt.ylabel('Count')
            plt.title('Monthly Application Analysis')
            plt.legend()
            st.pyplot(plt)

            st.markdown('</div>', unsafe_allow_html=True)
            # Repayment Analysis
            st.markdown('<div class="section">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Repayment Analysis</div>', unsafe_allow_html=True)

            st.markdown('<div class="chart">', unsafe_allow_html=True)
            # Create 4 KPIs side by side
            st.markdown('<div class="property"><span class="property-name">Scheduled Payments:</span><span class="property-value">2022</span></div>', unsafe_allow_html=True)
            st.markdown('<div class="property"><span class="property-name">Bounce Payments:</span><span class="property-value">300</span></div>', unsafe_allow_html=True)
            st.markdown('<div class="property"><span class="property-name">Upcoming Payment:</span><span class="property-value">1000</span></div>', unsafe_allow_html=True)
            st.markdown('<div class="property"><span class="property-name">Regular Percentage:</span><span class="property-value">80%</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            st.subheader("DPD Table")
            # st.markdown('<div class="chart">', unsafe_allow_html=True)
            # DPI bucketing table with monthly details
            # You can replace this with your data and table rendering logic
            dpi_table_data = {
                'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                'Regular': [10, 12, 15, 13, 11, 14, 10, 12, 16, 14, 11, 10],
                'Doubtful': [3, 2, 4, 5, 3, 4, 3, 2, 5, 4, 3, 2],
                'Loss': [1, 0, 1, 1, 0, 1, 0, 1, 2, 1, 1, 1],
                'Write-Off': [0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0]
            }

            dpi_table_df = pd.DataFrame(dpi_table_data)

            st.table(dpi_table_df)
            # st.markdown('</div>', unsafe_allow_html=True)

        with cmm2:
            st.markdown('<div class="section">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Yearly Product Performance</div>', unsafe_allow_html=True)
            # Create a bar chart comparing yearly product performance
            years = ['2020', '2021', '2022']
            products = ['Product A', 'Product B', 'Product C']
            data = np.random.randint(100, 1000, size=(3, 3))
            plt.figure(figsize=(8, 4))
            plt.bar(years, data[:, 0], color='r', label='Product A')
            plt.bar(years, data[:, 1], bottom=data[:, 0], color='g', label='Product B')
            plt.bar(years, data[:, 2], bottom=data[:, 0] + data[:, 1], color='b', label='Product C')
            plt.xlabel('Year')
            plt.ylabel('Performance')
            plt.title('Yearly Product Performance')
            plt.legend()
            st.pyplot(plt)

            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("<br><br>",unsafe_allow_html=True)

            st.markdown('<div class="chart">', unsafe_allow_html=True)
            # Create DPD analysis line chart
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
            dpd_data = np.random.randint(0, 30, size=6)
            plt.figure(figsize=(8, 4))
            plt.plot(months, dpd_data, marker='o')
            plt.xlabel('Month')
            plt.ylabel('DPD')
            plt.title('DPD Analysis')
            st.pyplot(plt)
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    if opt == "Important Ratios":
         # Define CSS styles for tiles (replace with actual styles)
        tile_style_1 = """
            .section-tile {
                padding: 20px;
                border: 1px solid #ccc;
                margin-bottom: 20px;
                background-color: #f9f9f9;
            }
            .section-title {
                font-size: 1.6em;
                font-weight: bold;
                color:red;
                margin-bottom: 10px;
            }
            .property {
                margin: 5px 0;
                font-size: 1.4em;
                font-weight: bold;
                margin-bottom: 10px;
                padding: 20px;
                border: 1px solid #ccc;
                background-color: #f9f9f9;
            }
            .property-name {
                font-weight: bold;
                font-size: 1.2em;
            }
            .property-value {
                margin-left: 10px;
                font-size: 1.2em;
            }
        """

        # Sample JSON data
        f1=open('borrower_details.json')
        sample_data= json.load(f1)

        # # Apply custom CSS styles
        st.markdown(f'<style>{tile_style_1}</style>', unsafe_allow_html=True)

        # Display JSON data in section
        flag="left"
        c1,c2=st.columns(2)
        for section_title, section_data in sample_data.items():
            prop_content=f"""
                <div class="section-tile">
                    <div class="section-title">{section_title}</div>
                    <div style="property">
                """
            
            for property_name, property_value in section_data.items():
                # prop_content+=f"""<span class="property-name">{property_name}: {property_value}</span><p>"""
                prop_content+=f"""<span class="property-name">{property_name}: </span>
                <span class="property-name">{property_value}</span><br>"""

            prop_content += "</div>"
            if flag=="left":
                with c1:
                    st.markdown(prop_content, unsafe_allow_html=True)
                    flag="right"
            else:
                with c2:
                    st.markdown(prop_content, unsafe_allow_html=True)
                    flag="left"

    if opt == "Connect APIs":
        # Streamlit app
        st.title("API Integration Dashboard")

        # Sample data for API providers
        api_providers = [
            {
                "logo": "logo_credit.png",
                "name": "Karza KYC",
                "description": "Cloud-based tools and APIs aid banks and insurers in real-time KYC document reading, verification, scoring, and enrichment using government databases.",
                "status": "Not Connected",
            },
            {
                "logo": "logo_credit.png",
                "name": "Perfios",
                "description": "Perfios, a leading FinTech company, empowers Financial Institutions with real-time decisioning, analysis, and credit underwriting.",
                "status": "Not Connected",
            },
            {
                "logo": "logo_credit.png",
                "name": "CRIF",
                "description": "CRIF India is one of India’s leading providers of Credit Information, Business Information, Analytics, Scoring, Credit Management and Decisions Solutions.",
                "status": "Not Connected",
            },
            {
                "logo": "logo_credit.png",
                "name": "Flowboard",
                "description": "Flowboard offers APIs for data extraction and fraud detection from documents like identity cards, income tax returns, bank statements. ",
                "status": "Not Connected",
            },
               {
                "logo": "logo_credit.png",
                "name": "LOS Integration",
                "description": "Streamline the lending process with our robust LOS, ensuring efficient and compliant loan origination.",
                "status": "Not Connected",
            },
            {
                "logo": "logo_credit.png",
                "name": "LMS Integration",
                "description": "Empower lenders with our LMS, simplifying loan servicing, payments, and borrower interactions.",
                "status": "Not Connected",
            },
            {
                "logo": "logo_credit.png",
                "name": "Tax Returns API",
                "description": "Simplify tax data retrieval and processing with our Tax Returns API, enhancing financial compliance and efficiency.",
                "status": "Not Connected",
            },
            {
                "logo": "logo_credit.png",
                "name": "Open Banking API",
                "description": "Leading open banking API platform, enabling fintech innovators to access & interpret financial data & make payments",
                "status": "Not Connected",
            },
            {
                "logo": "logo_credit.png",
                "name": "Karza Scan",
                "description": "Holistic fact-finding tool scans entities' networks via statutory records, covering 500+ databases for comprehensive corporate intelligence.",
                "status": "Not Connected",
            },
               {
                "logo": "logo_credit.png",
                "name": "AuthBridge",
                "description": "AuthBridge: India's top identity and background verification firm. Pioneering authentication tech for onboarding, employee checks, and business insights.",
                "status": "Not Connected",
            },
            {
                "logo": "logo_credit.png",
                "name": "IDfy",
                "description": "IDfy fosters a fraud-free world, enabling secure engagement for people and businesses. As gatekeepers, we ensure genuine access and transactions.",
                "status": "Not Connected",
            },
            {
                "logo": "logo_credit.png",
                "name": "Novel Patterns",
                "description": "Novel Patterns is an Intelligent data extraction from financial documents like Balance Sheets, Bank Statements, Audited Financials etc.",
                "status": "Not Connected",
            },
           
            # Add more API providers...
        ]

        # Define Python functions for connecting and disconnecting
        def connect_to_api(api_name):
            # Your logic to connect to the API
            st.write(f"Connected to {api_name}")

        def disconnect_from_api(api_name):
            # Your logic to disconnect from the API
            st.write(f"Disconnected from {api_name}")

        # Arrange expanders in 4 columns
        col1, col2, col3, col4 = st.columns(4)
        columns = [col1, col2, col3, col4]

        for i, api_provider in enumerate(api_providers):
            with columns[i % 4]:
                expander = st.expander(api_provider['name'],expanded=True)
                expander.image(api_provider['logo'], width=80)
                expander.write(api_provider['description'])
                status_text = expander.empty()
                button_text = "Connect" if api_provider['status'] == "Not Connected" else "Disconnect"
                if expander.button(button_text,key=i):
                    if api_provider['status'] == "Not Connected":
                        connect_to_api(api_provider['name'])
                        api_provider['status'] = "Connected"
                    else:
                        disconnect_from_api(api_provider['name'])
                        api_provider['status'] = "Not Connected"
                    status_text.markdown(f"**Status:** {api_provider['status']}")

    
    if opt == "New Visualization":
        xls = pd.ExcelFile('Cred_data.xlsx')
        df1 = pd.read_excel(xls, 'Index for Credit Saison')
        df2 = pd.read_excel(xls, 'Operations Info')

        left,right=st.columns(2)
        flag="left"
        for i in xls.sheet_names:
            x=pd.read_excel(xls, i)
            x=x.fillna("")
            if flag=="left":
                left.title(i)
                left.write(x)
                flag="right"
            else:
                right.title(i)
                right.write(x)
                flag="left"


        st.title("Portfolio Cuts")
        pc = pd.ExcelFile('PC_22-23.xlsx')
        fr = pd.ExcelFile('22-23_FY.xlsx')

        l1,r1=st.columns(2)
        for i in pc.sheet_names:
            x=pd.read_excel(pc, i)
            x=x.fillna("")
            if flag=="left":
                l1.title(i)
                l1.write(x)
                flag="right"
            else:
                r1.title(i)
                r1.write(x)
                flag="left"

        x=pd.read_excel(xls, "Shareholding pattern")
        x=x.iloc[2:]
        del x[x.columns[0]] 
        x.columns = x.iloc[0]
        x=x[1:]
        x= x.reset_index(drop=True)
        x=x.fillna("")
        st.write(x)
        plot = x.plot.pie(y=x.columns[0],figsize=(5, 5))
        plt.figure(figsize=(2, 2))
        plt.pie(x.iloc[2], labels=x.iloc[1], autopct='%1.1f%%',textprops={'fontsize': 7} ,startangle=140, colors=['#66b3ff','#99ff99','#ff9999'])
        plt.title('Revenue Breakdown',fontsize=5)
        st.pyplot(plt)

        st.title("Financial Statements")
        lv1,rv1=st.columns(2)
        for i in fr.sheet_names:
            x=pd.read_excel(fr, i)
            x=x.fillna("")
            if flag=="left":
                lv1.title(i)
                lv1.write(x)
                flag="right"
            else:
                rv1.title(i)
                rv1.write(x)
                flag="left"
    
        # l1.header("Loan Volume growth")
        # r1.header("DPD growth")

            # profile = ProfileReport(x,title="Pandas Profiling Report")
            # profile.to_file(i+".html")

            # sweet_report = sv.analyze(x)
            # sweet_report.show_html(i+'report.html')
        # st.write(xls.sheet_names)

        # df1=df1.fillna("")
        # df2=df2.fillna("")
        # st.write(df1)
        # st.write(df2)

    if opt == "Fetch APIs":
        st.write("Fetch APIs")

    if opt == "Risk Tracking":
        st.write("Risk tracking")
        c1,c2,c3=st.columns(3)
        with c1:
            st.title("Bank Balance")
            st.write("DPD(30)")
            st.write("DPD(90)")
        with c2:
            st.title("LTV")
        with c3:
            st.title("Repayments")
            
    if opt == "Create Pool":
      

        # Create an empty list to store loan data
        loan_pool = []

        # Streamlit app
        st.title("Simulated Loan Pool Creation")
        st.write("Use this app to create a pool of simulated loans. You can also upload loan data from a spreadsheet.")

        # Loan Types and their corresponding attributes
        loan_types = {
            "Auto Loan": [
                "Loan Name", "Loan Amount (USD)", "Loan Term (months)", "Interest Rate (%)",
                "Borrower Name", "Vehicle Make", "Vehicle Model", "Issue Date", "Maturity Date",
                "Risk Rating", "Geography", "Repayments Done Till Now", "Missed Repayments", "History"
            ],
            "Real Estate Bridge Loan": [
                "Loan Name", "Loan Amount (USD)", "Loan Term (months)", "Interest Rate (%)",
                "Borrower Name", "Property Address", "Loan-to-Value Ratio (%)", "Issue Date",
                "Maturity Date", "Risk Rating", "Geography", "Repayments Done Till Now", "Missed Repayments", "History"
            ],
            "Invoice Financing": [
                "Loan Name", "Loan Amount (USD)", "Loan Term (months)", "Interest Rate (%)",
                "Borrower Name", "Invoice Number", "Invoice Amount (USD)", "Issue Date", "Maturity Date",
                "Risk Rating", "Geography", "Repayments Done Till Now", "Missed Repayments", "History"
            ],
            "Trade Financing": [
                "Loan Name", "Loan Amount (USD)", "Loan Term (months)", "Interest Rate (%)",
                "Borrower Name", "Trade Transaction ID", "Trade Amount (USD)", "Issue Date", "Maturity Date",
                "Risk Rating", "Geography", "Repayments Done Till Now", "Missed Repayments", "History"
            ],
            "SMB Loan": [
                "Loan Name", "Loan Amount (USD)", "Loan Term (months)", "Interest Rate (%)",
                "Borrower Name", "Business Name", "Business Type", "Issue Date", "Maturity Date",
                "Risk Rating", "Geography", "Repayments Done Till Now", "Missed Repayments", "History"
            ],
        }

        # Function to add a loan to the pool
        def add_loan_to_pool(loan_data):
            loan_pool.append(loan_data)

        # Streamlit form for adding loans
        st.subheader("Add Loan to the Pool")
        loan_type = st.selectbox("Loan Type", list(loan_types.keys()))

        # Get the attributes for the selected loan type
        loan_attributes = loan_types[loan_type]

        # Create input fields based on the loan type
        loan_data = {}
        for attribute in loan_attributes:
            if attribute in ["Repayments Done Till Now", "Missed Repayments", "History"]:
                loan_data[attribute] = st.text_area(attribute)
            else:
                loan_data[attribute] = st.text_input(attribute)

        if st.button("Add Loan"):
            add_loan_to_pool(loan_data)
            st.success("Loan Added to Pool!")

        # Streamlit file uploader
        st.subheader("Upload Loan Data from Spreadsheet")
        uploaded_file = st.file_uploader("Choose a file", type=["xlsx", "csv"])

        if uploaded_file is not None:
            if st.button("Process and Add Loans"):
                if uploaded_file.name.endswith('.xlsx'):
                    df = pd.read_excel(uploaded_file)
                else:
                    df = pd.read_csv(uploaded_file)

                # Convert DataFrame to JSON and add to the loan pool
                loan_data_from_file = df.to_dict(orient="records")
                for loan_data in loan_data_from_file:
                    add_loan_to_pool(loan_data)
                st.success("Loans Added to Pool!")

        # Display the list of loans in the pool
        st.subheader("Loan Pool")
        for idx, loan_data in enumerate(loan_pool, start=1):
            st.write(f"Loan #{idx}")
            st.write(json.dumps(loan_data, indent=4))
            st.write("")

        # Export the loan pool to a JSON file
        if st.button("Export Loan Pool to JSON"):
            with open("loan_pool.json", "w") as json_file:
                json.dump(loan_pool, json_file, indent=4)
            st.success("Loan Pool Exported to loan_pool.json")



