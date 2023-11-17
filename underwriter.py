def app():
    import streamlit as st
    import streamlit as st
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
    import plotly.express as px

    with st.sidebar:
        opt=st.radio("Select Option",('Dashboard','Borrower List',"Pool UW/Filtering","Borrower UW"),)

    if opt=="Borrower List":
        conn = sqlite3.connect('my_db.db')

        # Load borrower's document links from the database
        df = pd.read_sql('SELECT * FROM docs', conn)

    
        # Main Streamlit code
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
        bd_df = bd_df.iloc[0]
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
            <div style="{block2_style}"><h3>Company Name: {bd_df.iloc[1]}</h1></div>
            <p>""",unsafe_allow_html=True)
        kp2.markdown(f"""
            <div style="{block2_style}"><h3>Credit Rating: {bd_df.iloc[9]}</h1></div>
            <p>""",unsafe_allow_html=True)
        kp3.markdown(f"""
            <div style="{block2_style}"><h3>Credit Score: {bd_df.iloc[10]}</h1></div>
            <p>""",unsafe_allow_html=True)

        # Generate HTML content with embedded data using .iloc
        block1_content = f"""
            <div style="{block1_style}">
                """
        # Fetch column names and values dynamically
        for i in range(2, 9):
            col_name = bd_df.index[i]
            col_value = bd_df.iloc[i]
            block1_content += f"<p><strong>{col_name}:</strong> {col_value}</p>\n"

        block1_content += "</div>"

        block2_content = f"""
            <div style="{block2_style}">
                """
        # Fetch column names and values dynamically
        for i in range(11, 18):
            col_name = bd_df.index[i]
            col_value = bd_df.iloc[i]
            block2_content += f"<p><strong>{col_name}:</strong> {col_value}</p>\n"

        block2_content += "</div>"

        # Render the HTML content using Streamlit's st.markdown() function
        block1.markdown(block1_content, unsafe_allow_html=True)
        block2.markdown(block2_content, unsafe_allow_html=True)



        # # Display document links as clickable tiles with Google Drive icons
        # block1,block2=st.columns(2)
    
        # bd_df=pd.read_csv("company_det.csv")
        # bd_columns = bd_df.columns.tolist()
        # # bd_df.drop(bd_df.iloc[0:1], inplace=True, axis=1)
        # # bd_columns.remove("Unnamed: 0.1")
        # # bd_columns.remove("Unnamed: 0")
        # bd_df=bd_df.iloc[0]
        # bd_num_cols_per_set = 5

        # with block1:
        #     st.title(bd_df["Credit Rating"])
        #     st.write(bd_df.iloc[1:9])

        # with block2:
        #     st.title(bd_df["Location"])
        #     # st.metric(value=bd_df["Credit Score"], label="Credit Score")
        #     st.write(bd_df.iloc[11:19])

            
         


        # bd_column_sets = [bd_columns[i:i+bd_num_cols_per_set] for i in range(0, len(bd_columns), bd_num_cols_per_set)]
        # for col_set in bd_column_sets:
        #     cl1,cl2,cl3,cl4,cl5 = st.columns(5)
        #     for col, column in zip([cl1,cl2,cl3,cl4,cl5], col_set):
        #         with col:
        #             st.write(f"**{column}:**")
        #             st.write(f"{bd_df[column]}")
        #             # link =
        #             # if link:
        #             #     st.markdown(link, unsafe_allow_html=True)


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
        
        

        # Sample JSON data (Replace this with your actual JSON data)
        # json_data = {"Borrower Eligibility": {"ID": 1, "Lending Business": true, "Adhere to Local Lending Laws": true, "Track Record Years": 5, "Institutional Investment": true, "Series A Raised": true}, "Promoter and CXO Evaluation": {"Promoter's Expertise": true, "CXO's Relevant Work Experience": true, "Additional Due Diligence for CEO Relatives": false}, "Company Board and Independent Directors": {"Presence of Board or Independent/Nominee Directors": true, "Independent Directors Experience": true, "Independent/Nominee Directors from Major Institutional Investors": true}, "Capital Adequacy": {"Equity Base (USD)": 2000000, "Net Worth (USD)": 1000000, "Assets Under Management (USD)": 100000, "Capital Adequacy Ratio": 20.0}, "Leverage": {"Total Outstanding Debt": 1000000.0, "FLDG Guarantees": 1000.0, "Intangible Assets": 3000.0, "Adjusted Tangible Net Worth": 1996000.0, "Leverage Ratio": 0.501002004008016, "Loan Type": "secured loan business"}, "Portfolio Quality": {"Portfolio at Risk": 1000.0, "Days Past Due 0+": 500.0, "Days Past Due 30+": 400.0, "Days Past Due 90+ (Gross NPAs)": 100.0, "Past 12 Months Write-offs": 50, "Actual Portfolio Quality": 150.0, "Unsecured Provisions": true}, "Profitability": {"Return on Assets (ROA) for the Past Three Years": 5.0, "Return on Equity (ROE)": 21.0}, "Liquidity": {"Liquidity Policy": true, "Operational Expenses Liquidity": true, "Debt Repayment Obligations Liquidity": true, "Liquid Short-term Mutual Funds": true, "Obligations from Guarantees": true}, "Asset Liability Management (ALM)": {"Loan Assets": 10000.0, "Deposits/Borrowings Liabilities": 1500.0, "Static ALM": 11500.0, "Inflow from Loans Given": 100000.0, "Outflow to Loans Taken": 4000.0, "Positive Mismatch": true, "Average Tenor of Loans Given": 3, "Average Tenor of Borrowings": 3}, "Resource Profile": {"Diversified Lender Base": true, "Non-Bank Lenders Represent 40% of Borrowings": true}, "Operational Performance": {"Current Collection": 10000.0, "Overdue Collection": 8000.0, "Current Demand": 20000.1, "Current Collection Efficiency": 0.4999975000125, "Total Collection Efficiency (Past 12 Months Average)": 90.0, "Growth in AUM (Average for the Last 3 Years or Last 6 Quarters)": 30.06, "GNPA": 100.0, "Restructured Portfolio": 120.0, "Portfolio in 90+ Bucket for Restructured Portfolio": 100.0, "Stressed Book": 120.0, "Yield on Portfolio": 15.0, "Cost of Funds": 10.0, "Net Interest Margin": 5.0, "Restructuring Loans": false, "Net Worth > Stressed Portfolio": true, "YoY Growth in Employees (%)": 10.0, "YoY Growth in NIM (%)": 10.0, "YoY Growth in AUM > Growth in Total Employees": true, "YoY Positive Growth in NIM": true, "Loan Book Ratio to Outstanding Borrowings > 1.1": true}}
        

        # json_data=json.load("borrower_details.json")

        # Function to render the Borrower Eligibility section
        def render_borrower_eligibility(json_data):
            st.header("Borrower Eligibility")
            st.subheader("Borrower Information")
            st.write(f"Lending Business: {json_data['Borrower Eligibility']['Lending Business']}")
            st.write(f"Adhere to Local Lending Laws: {json_data['Borrower Eligibility']['Adhere to Local Lending Laws']}")
            st.write(f"Track Record Years: {json_data['Borrower Eligibility']['Track Record Years']}")
            st.write(f"Institutional Investment: {json_data['Borrower Eligibility']['Institutional Investment']}")
            st.write(f"Series A Raised: {json_data['Borrower Eligibility']['Series A Raised']}")

            st.subheader("Promoter and CXO Evaluation")
            # st.write(f"Promoter's Expertise: {json_data['Promoter and CXO Evaluation']["Promoter's Expertise"]}")
            # st.write(f"CXO's Relevant Work Experience: {json_data['Promoter and CXO Evaluation']['CXO\'s Relevant Work Experience']}")
            st.write(f"Additional Due Diligence for CEO Relatives: {json_data['Promoter and CXO Evaluation']['Additional Due Diligence for CEO Relatives']}")

            # Add other sections of the Borrower Eligibility here

        # Function to render the Capital Adequacy section
        def render_capital_adequacy(json_data):
            st.header("Capital Adequacy")
            st.subheader("Financial Information")
            st.write(f"Equity Base (USD): {json_data['Capital Adequacy']['Equity Base (USD)']}")
            st.write(f"Net Worth (USD): {json_data['Capital Adequacy']['Net Worth (USD)']}")
            st.write(f"Assets Under Management (USD): {json_data['Capital Adequacy']['Assets Under Management (USD)']}")
            st.write(f"Capital Adequacy Ratio: {json_data['Capital Adequacy']['Capital Adequacy Ratio']}")

            # Add other sections of the Capital Adequacy here

        # Function to render the Leverage section
        def render_leverage(json_data):
            st.header("Leverage")
            st.subheader("Debt Information")
            st.write(f"Total Outstanding Debt (USD): {json_data['Leverage']['Total Outstanding Debt']}")
            st.write(f"FLDG Guarantees (USD): {json_data['Leverage']['FLDG Guarantees']}")
            st.write(f"Intangible Assets (USD): {json_data['Leverage']['Intangible Assets']}")
            st.write(f"Adjusted Tangible Net Worth (USD): {json_data['Leverage']['Adjusted Tangible Net Worth']}")
            st.write(f"Leverage Ratio: {json_data['Leverage']['Leverage Ratio']}")
            st.write(f"Loan Type: {json_data['Leverage']['Loan Type']}")

            # Add other sections of the Leverage here

        # Function to render the Portfolio Quality section
        def render_portfolio_quality(json_data):
            st.header("Portfolio Quality")
            st.subheader("Portfolio at Risk")
            st.write(f"Portfolio at Risk (USD): {json_data['Portfolio Quality']['Portfolio at Risk']}")
            st.write(f"Days Past Due 0+ (USD): {json_data['Portfolio Quality']['Days Past Due 0+']}")
            st.write(f"Days Past Due 30+ (USD): {json_data['Portfolio Quality']['Days Past Due 30+']}")
            st.write(f"Days Past Due 90+ (Gross NPAs) (USD): {json_data['Portfolio Quality']['Days Past Due 90+ (Gross NPAs)']}")
            st.write(f"Past 12 Months Write-offs (USD): {json_data['Portfolio Quality']['Past 12 Months Write-offs']}")
            st.write(f"Actual Portfolio Quality (USD): {json_data['Portfolio Quality']['Actual Portfolio Quality']}")
            st.write(f"Unsecured Provisions: {json_data['Portfolio Quality']['Unsecured Provisions']}")

            # Add other sections of the Portfolio Quality here

        # Function to render the Profitability section
        def render_profitability(json_data):
            st.header("Profitability")
            st.subheader("Return on Assets (ROA)")
            st.write(f"ROA for the Past Three Years: {json_data['Profitability']['Return on Assets (ROA) for the Past Three Years']}%")
            st.write(f"Return on Equity (ROE): {json_data['Profitability']['Return on Equity (ROE)']}%")

            # Add other sections of the Profitability here

        # Function to render the Liquidity section
        def render_liquidity(json_data):
            st.header("Liquidity")
            st.subheader("Liquidity Policy")
            st.write(f"Liquidity Policy: {json_data['Liquidity']['Liquidity Policy']}")
            st.write(f"Operational Expenses Liquidity: {json_data['Liquidity']['Operational Expenses Liquidity']}")
            st.write(f"Debt Repayment Obligations Liquidity: {json_data['Liquidity']['Debt Repayment Obligations Liquidity']}")
            st.write(f"Liquid Short-term Mutual Funds: {json_data['Liquidity']['Liquid Short-term Mutual Funds']}")
            st.write(f"Obligations from Guarantees: {json_data['Liquidity']['Obligations from Guarantees']}")

            # Add other sections of the Liquidity here

        # Function to render the Asset Liability Management (ALM) section
        def render_asset_liability_management(json_data):
            st.header("Asset Liability Management (ALM)")
            st.subheader("Assets and Liabilities")
            st.write(f"Loan Assets (USD): {json_data['Asset Liability Management (ALM)']['Loan Assets']}")
            st.write(f"Deposits/Borrowings Liabilities (USD): {json_data['Asset Liability Management (ALM)']['Deposits/Borrowings Liabilities']}")
            st.write(f"Static ALM (USD): {json_data['Asset Liability Management (ALM)']['Static ALM']}")
            st.write(f"Inflow from Loans Given (USD): {json_data['Asset Liability Management (ALM)']['Inflow from Loans Given']}")
            st.write(f"Outflow to Loans Taken (USD): {json_data['Asset Liability Management (ALM)']['Outflow to Loans Taken']}")
            st.write(f"Positive Mismatch: {json_data['Asset Liability Management (ALM)']['Positive Mismatch']}")
            st.write(f"Average Tenor of Loans Given: {json_data['Asset Liability Management (ALM)']['Average Tenor of Loans Given']} years")
            st.write(f"Average Tenor of Borrowings: {json_data['Asset Liability Management (ALM)']['Average Tenor of Borrowings']} years")

            # Add other sections of the Asset Liability Management (ALM) here

        # Function to render the Resource Profile section
        def render_resource_profile(json_data):
            st.header("Resource Profile")
            st.write(f"Diversified Lender Base: {json_data['Resource Profile']['Diversified Lender Base']}")
            st.write(f"Non-Bank Lenders Represent 40% of Borrowings: {json_data['Resource Profile']['Non-Bank Lenders Represent 40% of Borrowings']}")

            # Add other sections of the Resource Profile here

        # Function to render the Operational Performance section
        def render_operational_performance(json_data):
            st.header("Operational Performance")
            st.subheader("Collection Information")
            st.write(f"Current Collection (USD): {json_data['Operational Performance']['Current Collection']}")
            st.write(f"Overdue Collection (USD): {json_data['Operational Performance']['Overdue Collection']}")
            st.write(f"Current Demand (USD): {json_data['Operational Performance']['Current Demand']}")
            st.write(f"Current Collection Efficiency: {json_data['Operational Performance']['Current Collection Efficiency']:.2%}")
            st.write(f"Total Collection Efficiency (Past 12 Months Average): {json_data['Operational Performance']['Total Collection Efficiency (Past 12 Months Average)']:.2%}")

            st.subheader("Loan Portfolio Quality")
            st.write(f"GNPA (Gross Non-Performing Assets) (USD): {json_data['Operational Performance']['GNPA']}")
            st.write(f"Restructured Portfolio (USD): {json_data['Operational Performance']['Restructured Portfolio']}")
            st.write(f"Portfolio in 90+ Bucket for Restructured Portfolio (USD): {json_data['Operational Performance']['Portfolio in 90+ Bucket for Restructured Portfolio']}")
            st.write(f"Stressed Book (USD): {json_data['Operational Performance']['Stressed Book']}")
            st.write(f"Yield on Portfolio: {json_data['Operational Performance']['Yield on Portfolio']}%")
            st.write(f"Cost of Funds: {json_data['Operational Performance']['Cost of Funds']}%")
            st.write(f"Net Interest Margin (NIM): {json_data['Operational Performance']['Net Interest Margin']}%")
            st.write(f"Restructuring Loans: {json_data['Operational Performance']['Restructuring Loans']}")
            st.write(f"Net Worth > Stressed Portfolio: {json_data['Operational Performance']['Net Worth > Stressed Portfolio']}")
            st.write(f"YoY Growth in Employees: {json_data['Operational Performance']['YoY Growth in Employees (%)']}%")
            st.write(f"YoY Growth in NIM: {json_data['Operational Performance']['YoY Growth in NIM (%)']}%")
            st.write(f"YoY Growth in AUM > Growth in Total Employees: {json_data['Operational Performance']['YoY Growth in AUM > Growth in Total Employees']}")
            st.write(f"YoY Positive Growth in NIM: {json_data['Operational Performance']['YoY Positive Growth in NIM']}")

            # Add other sections of the Operational Performance here

        # Main function to render the dashboard
        def main_json():
            st.title("Borrower Profile Dashboard")
            import json

            # json_file = st.file_uploader("Choose a borrower json file", type=["json"])
            f=open('borrower_details.json')
            json_data = json.load(f)
      

            r1,r2=st.columns(2)
            with r1:
                render_borrower_eligibility(json_data)
                render_capital_adequacy(json_data)
                render_leverage(json_data)
                render_portfolio_quality(json_data)
                render_liquidity(json_data)
            with r2:
                render_asset_liability_management(json_data)
                render_resource_profile(json_data)
                render_operational_performance(json_data)

            # Applying CSS styling using the 'st.markdown' function
            # st.markdown(
            #     """
            #     <style>
            #     .stApp {
            #         background-color: #f0f0f0;
            #     }
            #     .stApp main {
            #         max-width: 900px;
            #         margin: 0 auto;
            #         padding: 20px;
            #     }
            #     .stApp h1, .stApp h2, .stApp h3 {
            #         color: #1f78b4;
            #     }
            #     .stApp subheader {
            #         color: #1f78b4;
            #     }
            #     .stApp div, .stApp p {
            #         color: #333;
            #     }
            #     .stApp header, .stApp footer {
            #         display: none;
            #     }
            #     .stApp .block-container {
            #         border: 1px solid #ddd;
            #         border-radius: 5px;
            #         margin-bottom: 20px;
            #         padding: 15px;
            #         background-color: #fff;
            #     }
            #     </style>
            #     """,
            #     unsafe_allow_html=True,
            # )

        
        main_json()



    if opt=="Dashboard":
        st.write("Underwriter view")

        col1, col2, col3, col4 = st.columns(4)


        with col1:
            st.markdown('<div style="color: #008080; padding: 20px; background-color:white; text-align: center;">'
                        '<h2 style="color: #008080;">Active Cases</h2>'
                        '<p>10</p>'
                        '</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div style="color: #800080; padding: 20px; background-color:white; text-align: center;">'
                        '<h2 style="color:#800000;">Pending Cases</h2>'
                        '<p>5</p>'
                        '</div>', unsafe_allow_html=True)

        with col3:
            st.markdown('<div style="color: #800000; padding: 20px; background-color:white; text-align: center;">'
                        '<h2 style="color: #800000;">Score</h2>'
                        '<p>9.5/10</p>'
                        '</div>', unsafe_allow_html=True)

        with col4:
            st.markdown('<div style="color: #008000; padding: 20px; background-color:white; text-align: center;">'
                        '<h2 style="color: #008080;">Earnings</h2>'
                        '<p>$1000</p>'
                        '</div>', unsafe_allow_html=True)

        

        # Example data
        data = pd.DataFrame({
            'Category': ['Fintech', 'Supply-Chain', 'Marketplaces', 'Real-Estate'],
            'Value': [10, 20, 15, 25]
        })

        # # Set Streamlit page config
        # # st.set_page_config(page_title='Sleek Dashboard', layout='wide')

        # # 1st row - 4 columns with KPI banners
        # col1, col2, col3, col4 = st.columns(4)


        # # 2nd row - 4 columns with KPI banners
        # col5, col6, col7, col8 = st.columns(4)

        # with col5:
        #     st.markdown('<div style="background-color: #008080; padding: 20px; color: white; text-align: center;">'
        #                 '<h2>KPI 5</h2>'
        #                 '<p>Value: 300</p>'
        #                 '</div>', unsafe_allow_html=True)

        # with col6:
        #     st.markdown('<div style="background-color: #800080; padding: 20px; color: white; text-align: center;">'
        #                 '<h2>KPI 6</h2>'
        #                 '<p>Value: 400</p>'
        #                 '</div>', unsafe_allow_html=True)

        # with col7:
        #     st.markdown('<div style="background-color: #800000; padding: 20px; color: white; text-align: center;">'
        #                 '<h2>KPI 7</h2>'
        #                 '<p>Value: 350</p>'
        #                 '</div>', unsafe_allow_html=True)

        # with col8:
        #     st.markdown('<div style="background-color: #008000; padding: 20px; color: white; text-align: center;">'
        #                 '<h2>KPI 8</h2>'
        #                 '<p>Value: 450</p>'
        #                 '</div>', unsafe_allow_html=True)

        # # 3rd row - 2 columns with list/table and filters
        # col9, col10 = st.columns(2)

        # with col9:
        #     st.subheader('Data List/Table')
        #     # Display the data list/table
        #     st.dataframe(data)

        #     # Filter options
        #     selected_category = st.selectbox('Select Category', data['Category'].unique())

        #     # Filtered data based on selected category
        #     filtered_data = data[data['Category'] == selected_category]
        #     st.write('Filtered Data:')
        #     st.dataframe(filtered_data)

        # with col10:
        #     st.subheader('Filters')
        #     # Display filters
        #     # ...

        # # 4th row - 3 columns with graphs
        # col11, col12, col13 = st.columns(3)

        datad = pd.DataFrame({
            'Date': pd.date_range(start='2023-01-01', periods=10, freq='M'),
            'Growth': [100, 120, 150, 180, 200, 230, 250, 270, 300, 320]
        })



        cl1,cl2,cl3=st.columns(3)
        with cl1:
            cl1.header('Category Comparisions')
            fig1 = px.bar(data, x='Category', y='Value', color='Category')
            st.plotly_chart(fig1)

        with cl2:
            cl2.header('Category Distribution')
            fig2 = px.pie(data, names='Category', values='Value')
            st.plotly_chart(fig2)

        with cl3:
            cl3.header('Category growth')
            fig = px.line(datad, x='Date', y='Growth', labels={'Date': 'Date', 'Growth': 'Growth'})
            st.plotly_chart(fig)



    if opt=="Asset Originator UW":
        menu_option = st.sidebar.selectbox("Select an option", ["Create & Edit Policy", "Underwrite"])

        if menu_option=="Create & Edit Policy":
            policy_rules = {
                    "Lending and non-lending businesses should be kept separate": True,
                    "Adhere to local money lending laws and fulfill all regulatory requirements": True,
                    "Track record - Promoter-driven entity": {"min_years": 5},
                    "Track record - Entity backed by institutional investors": {"min_years": 3, "series_a_funding": True},
                    "Promoter and CXO qualifications - Relevant work experience": {"cxo_work_experience": True},
                    "Promoter and CXO qualifications - Relatives of CEO": {"ceo_relatives_diligence": True},
                    "Board of directors - Independent and nominee directors": {"institutional_investors_directors": True},
                    "Board of directors - Additional scrutiny for CEO relatives": {"ceo_relatives_diligence_additional": True},
                    "Board of directors - Independent directors experience": {"independent_directors_experience": True},
                    "Capital Adequacy - Equity base": {"min_equity_base": 100},
                    "Capital Adequacy - Marquee institutional equity investors": {"min_net_worth": 100},
                    "Capital Adequacy Ratio (CAR)": {"min_car_ratio": 20},
                    "Leverage (D/E ratio) - Personal loan business": {"max_de_ratio_personal_loan": 3},
                    "Leverage (D/E ratio) - Secured businesses": {"max_de_ratio_secured_businesses": 5},
                    "Leverage (D/E ratio) - Housing, Loan against properties, and microfinance companies": {"max_de_ratio_other_businesses": 5},
                    "Portfolio Quality - Unsecured businesses": {"max_par_unsecured_businesses": 8},
                    "Portfolio Quality - Microfinance": {"max_par_microfinance": 5},
                    "Portfolio Quality - Secured businesses": {"max_par_secured_businesses": 5},
                    "Provisions for NPAs - Unsecured loans": True,
                    "Profitability - Positive ROA": {"min_roa_positive": True},
                    "Profitability - ROA range": {"min_roa": 0.5, "max_roa": 2},
                    "Profitability - ROE range": {"min_roe": 5, "max_roe": 20},
                    "Liquidity - Well-documented liquidity policy": True,
                    "Liquidity - Maintain operational expenses and debt repayment": True,
                    "Asset Liability Management (ALM) - Positive mismatch": True,
                    "Asset Liability Management (ALM) - Long-term liabilities and short-term assets": True,
                    "Resource Profile - Diversified lender base": True,
                    "Resource Profile - Maximum lender class exposure": {"max_lender_class_exposure": 40},
                    "Operational Performance - Current collection efficiency - Personal loans": {"min_collection_efficiency_personal_loans": 85},
                    "Operational Performance - Current collection efficiency - Other asset classes": {"min_collection_efficiency_other_assets": 90},
                    "Operational Performance - Total collection efficiency": True,
                    "Operational Performance - Growing trend in AUM and disbursements": True,
                    "Operational Performance - Restructuring of loans": {"loan_restructuring": False},
                    "Operational Performance - Net worth vs stressed portfolio": True,
                    "Operational Performance - YoY growth in AUM vs growth in total employees": True,
                    "Operational Performance - Net Interest Margin (NIM)": True,
                    "Operational Performance - Loan book vs outstanding borrowings": {"min_loan_book_cover": 1.1},
                    "Operational Performance - Unit economics calculation": {"loan_tenure_up_to_6_months": True}
                }

            def create_policy():
                st.header("Create Policy")
                policy_name = st.text_input("Policy Name")
                # Input fields for policy details
                lending_nonlending_separate = st.checkbox("Lending and non-lending businesses should be kept separate")
                adhere_lending_laws_regulatory_req = st.checkbox("Adhere to local money lending laws and fulfill all regulatory requirements")
                track_record_promoter_driven = st.checkbox("Track record - Promoter-driven entity")
                track_record_promoter_driven_years = st.number_input("Track record - Promoter-driven (Years)", value=0, step=1)
                track_record_institutional_investors = st.checkbox("Track record - Entity backed by institutional investors")
                track_record_institutional_investors_years = st.number_input("Track record - Institutional Investors (Years)", value=0, step=1)
                track_record_institutional_investors_series_a = st.checkbox("Track record - Institutional Investors (Series A)")
                promoter_cxo_qualifications_work_experience = st.checkbox("Promoter and CXO qualifications - Relevant work experience")
                promoter_cxo_qualifications_ceo_relatives = st.checkbox("Promoter and CXO qualifications - Relatives of CEO")
                board_of_directors_independent_nominee_directors = st.checkbox("Board of directors - Independent and nominee directors")
                board_of_directors_ceo_relatives_additional_scrutiny = st.checkbox("Board of directors - Additional scrutiny for CEO relatives")
                board_of_directors_independent_directors_experience = st.checkbox("Board of directors - Independent directors experience")
                capital_adequacy_equity_base = st.number_input("Capital Adequacy - Equity base", value=0, step=1)
                capital_adequacy_marquee_institutional_investors = st.checkbox("Capital Adequacy - Marquee institutional equity investors")
                capital_adequacy_ratio_car = st.number_input("Capital Adequacy Ratio (CAR)", value=0, step=1)
                leverage_personal_loan_business = st.checkbox("Leverage (D/E ratio) - Personal loan business")
                leverage_personal_loan_business_ratio = st.number_input("Leverage (D/E ratio) - Personal loan business (Max Ratio)", value=0.0, step=0.1)
                leverage_secured_businesses = st.checkbox("Leverage (D/E ratio) - Secured businesses")
                leverage_secured_businesses_ratio = st.number_input("Leverage (D/E ratio) - Secured businesses (Max Ratio)", value=0.0, step=0.1)
                leverage_housing_loan_microfinance_companies = st.checkbox("Leverage (D/E ratio) - Housing, Loan against properties, and microfinance companies")
                leverage_housing_loan_microfinance_companies_ratio = st.number_input("Leverage (D/E ratio) - Housing, Loan against properties, and microfinance companies (Max Ratio)", value=0.0, step=0.1)
                portfolio_quality_unsecured_businesses = st.checkbox("Portfolio Quality - Unsecured businesses")
                portfolio_quality_unsecured_businesses_par = st.number_input("Portfolio Quality - Unsecured businesses (Max PAR)", value=0, step=1)
                portfolio_quality_microfinance = st.checkbox("Portfolio Quality - Microfinance")
                portfolio_quality_microfinance_par = st.number_input("Portfolio Quality - Microfinance (Max PAR)", value=0, step=1)
                portfolio_quality_secured_businesses = st.checkbox("Portfolio Quality - Secured businesses")
                portfolio_quality_secured_businesses_par = st.number_input("Portfolio Quality - Secured businesses (Max PAR)", value=0, step=1)
                provisions_npas_unsecured_loans = st.checkbox("Provisions for NPAs - Unsecured loans")
                profitability_positive_roa = st.checkbox("Profitability - Positive ROA")
                profitability_roa_range = st.checkbox("Profitability - ROA range")
                profitability_roa_min = st.number_input("Profitability - ROA range (Min)", value=0.0, step=0.1)
                profitability_roa_max = st.number_input("Profitability - ROA range (Max)", value=0.0, step=0.1)
                profitability_roe_range = st.checkbox("Profitability - ROE range")
                profitability_roe_min = st.number_input("Profitability - ROE range (Min)", value=0.0, step=0.1)
                profitability_roe_max = st.number_input("Profitability - ROE range (Max)", value=0.0, step=0.1)
                liquidity_well_documented_liquidity_policy = st.checkbox("Liquidity - Well-documented liquidity policy")
                liquidity_maintain_operational_expenses = st.checkbox("Liquidity - Maintain operational expenses and debt repayment")
                asset_liability_management_positive_mismatch = st.checkbox("Asset Liability Management (ALM) - Positive mismatch")
                asset_liability_management_long_term_short_term_assets = st.checkbox("Asset Liability Management (ALM) - Long-term liabilities and short-term assets")
                resource_profile_diversified_lender_base = st.checkbox("Resource Profile - Diversified lender base")
                resource_profile_max_lender_class_exposure = st.number_input("Resource Profile - Maximum lender class exposure", value=0, step=1)
                operational_performance_collection_efficiency_personal_loans = st.checkbox("Operational Performance - Current collection efficiency - Personal loans")
                operational_performance_collection_efficiency_personal_loans_min = st.number_input("Operational Performance - Current collection efficiency - Personal loans (Min)", value=0, step=1)
                operational_performance_collection_efficiency_other_assets = st.checkbox("Operational Performance - Current collection efficiency - Other asset classes")
                operational_performance_collection_efficiency_other_assets_min = st.number_input("Operational Performance - Current collection efficiency - Other asset classes (Min)", value=0, step=1)
                operational_performance_total_collection_efficiency = st.checkbox("Operational Performance - Total collection efficiency")
                operational_performance_growth_aum_disbursements = st.checkbox("Operational Performance - Growing trend in AUM and disbursements")
                operational_performance_restructuring_loans = st.checkbox("Operational Performance - Restructuring of loans")
                operational_performance_net_worth_stressed_portfolio = st.checkbox("Operational Performance - Net worth vs stressed portfolio")
                operational_performance_aum_vs_employees_growth = st.checkbox("Operational Performance - YoY growth in AUM vs growth in total employees")
                operational_performance_net_interest_margin_growth = st.checkbox("Operational Performance - Net Interest Margin (NIM) growth")
                operational_performance_loan_book_outstanding_borrowings = st.checkbox("Operational Performance - Loan book vs outstanding borrowings")
                operational_performance_unit_economics_loan_tenure = st.checkbox("Operational Performance - Unit economics calculation")

                # Create policy data dictionary
                policy_data = {
                    "Lending and non-lending businesses should be kept separate": lending_nonlending_separate,
                    "Adhere to local money lending laws and fulfill all regulatory requirements": adhere_lending_laws_regulatory_req,
                    "Track record - Promoter-driven entity": {
                        "min_years": track_record_promoter_driven_years
                    },
                    "Track record - Entity backed by institutional investors": {
                        "min_years": track_record_institutional_investors_years,
                        "series_a_funding": track_record_institutional_investors_series_a
                    },
                    "Promoter and CXO qualifications - Relevant work experience": promoter_cxo_qualifications_work_experience,
                    "Promoter and CXO qualifications - Relatives of CEO": promoter_cxo_qualifications_ceo_relatives,
                    "Board of directors - Independent and nominee directors": board_of_directors_independent_nominee_directors,
                    "Board of directors - Additional scrutiny for CEO relatives": board_of_directors_ceo_relatives_additional_scrutiny,
                    "Board of directors - Independent directors experience": board_of_directors_independent_directors_experience,
                    "Capital Adequacy - Equity base": {
                        "min_equity_base": capital_adequacy_equity_base
                    },
                    "Capital Adequacy - Marquee institutional equity investors": capital_adequacy_marquee_institutional_investors,
                    "Capital Adequacy Ratio (CAR)": {
                        "min_car_ratio": capital_adequacy_ratio_car
                    },
                    "Leverage (D/E ratio) - Personal loan business": {
                        "max_de_ratio_personal_loan": leverage_personal_loan_business_ratio
                    },
                    "Leverage (D/E ratio) - Secured businesses": {
                        "max_de_ratio_secured_businesses": leverage_secured_businesses_ratio
                    },
                    "Leverage (D/E ratio) - Housing, Loan against properties, and microfinance companies": {
                        "max_de_ratio_other_businesses": leverage_housing_loan_microfinance_companies_ratio
                    },
                    "Portfolio Quality - Unsecured businesses": {
                        "max_par_unsecured_businesses": portfolio_quality_unsecured_businesses_par
                    },
                    "Portfolio Quality - Microfinance": {
                        "max_par_microfinance": portfolio_quality_microfinance_par
                    },
                    "Portfolio Quality - Secured businesses": {
                        "max_par_secured_businesses": portfolio_quality_secured_businesses_par
                    },
                    "Provisions for NPAs - Unsecured loans": provisions_npas_unsecured_loans,
                    "Profitability - Positive ROA": {
                        "min_roa_positive": profitability_positive_roa
                    },
                    "Profitability - ROA range": {
                        "min_roa": profitability_roa_min,
                        "max_roa": profitability_roa_max
                    },
                    "Profitability - ROE range": {
                        "min_roe": profitability_roe_min,
                        "max_roe": profitability_roe_max
                    },
                    "Liquidity - Well-documented liquidity policy": liquidity_well_documented_liquidity_policy,
                    "Liquidity - Maintain operational expenses and debt repayment": liquidity_maintain_operational_expenses,
                    "Asset Liability Management (ALM) - Positive mismatch": asset_liability_management_positive_mismatch,
                    "Asset Liability Management (ALM) - Long-term liabilities and short-term assets": asset_liability_management_long_term_short_term_assets,
                    "Resource Profile - Diversified lender base": resource_profile_diversified_lender_base,
                    "Resource Profile - Maximum lender class exposure": {
                        "max_lender_class_exposure": resource_profile_max_lender_class_exposure
                    },
                    "Operational Performance - Current collection efficiency - Personal loans": {
                        "min_collection_efficiency_personal_loans": operational_performance_collection_efficiency_personal_loans_min
                    },
                    "Operational Performance - Current collection efficiency - Other asset classes": {
                        "min_collection_efficiency_other_assets": operational_performance_collection_efficiency_other_assets_min
                    },
                    "Operational Performance - Total collection efficiency": operational_performance_total_collection_efficiency,
                    "Operational Performance - Growing trend in AUM and disbursements": operational_performance_growth_aum_disbursements,
                    "Operational Performance - Restructuring of loans": {
                        "loan_restructuring": operational_performance_restructuring_loans
                    },
                    "Operational Performance - Net worth vs stressed portfolio": operational_performance_net_worth_stressed_portfolio,
                    "Operational Performance - YoY growth in AUM vs growth in total employees": operational_performance_aum_vs_employees_growth,
                    "Operational Performance - Net Interest Margin (NIM)": operational_performance_net_interest_margin_growth,
                    "Operational Performance - Loan book vs outstanding borrowings": operational_performance_loan_book_outstanding_borrowings,
                    "Operational Performance - Unit economics calculation": {
                        "loan_tenure_up_to_6_months": operational_performance_unit_economics_loan_tenure
                    }
                }

                return policy_name,policy_data

            def save_policy(policy_name,policy_data,file_path):
                with open(file_path, 'r') as file:
                    existing_policies = json.load(file)

                # Generate a new policy name
                # new_policy_name = f"Policy_{len(existing_policies) + 1}"

                # Add the new policy to existing policies
                existing_policies[policy_name] = policy_data

                with open(file_path, 'w') as file:
                    json.dump(existing_policies, file, indent=4)

                st.success("Policy saved successfully.")

            policy_name,policy=create_policy()
            if st.button("Save Policy"):
                save_policy(policy_name,policy,"borrow.json")
 

        if menu_option=="Underwrite":
            sub_menu_option=st.sidebar.selectbox("Select an option", ["Create new borrower", "Run policy"])
            if sub_menu_option=="Create new borrower":
                def create_borrower():
                    st.subheader("Create Borrower")
                    borrower = {}

                    borrower['id'] = st.number_input("ID")

                    borrower['lending_business'] = st.checkbox("Lending Business")
                    borrower['separate_businesses'] = st.checkbox("Separate Businesses")
                    borrower['adhere_lending_laws'] = st.checkbox("Adhere to Lending Laws")

                    # Track record
                    st.subheader("Track record")
                    borrower['track_record'] = {}
                    borrower['track_record']['promoter_driven'] = {}
                    borrower['track_record']['promoter_driven']['years'] = st.number_input("Promoter-driven years", value=0, min_value=0)

                    borrower['track_record']['institutional_investors'] = {}
                    borrower['track_record']['institutional_investors']['years'] = st.number_input("Institutional investors years", value=0, min_value=0)
                    borrower['track_record']['institutional_investors']['series_a'] = st.checkbox("Requires series A funding (Institutional investors)")

                    # Promoter and CXO qualifications
                    st.subheader("Promoter and CXO qualifications")
                    borrower['promoter_cxo_qualifications'] = {}
                    borrower['promoter_cxo_qualifications']['work_experience'] = st.checkbox("Requires work experience")

                    borrower['promoter_cxo_qualifications']['ceo_relatives'] = {}
                    borrower['promoter_cxo_qualifications']['ceo_relatives']['due_diligence'] = st.checkbox("Requires due diligence for CEO relatives")

                    # Board of directors
                    st.subheader("Board of directors")
                    borrower['board_of_directors'] = {}
                    borrower['board_of_directors']['independent_nominee_directors'] = st.checkbox("Requires independent and nominee directors")

                    borrower['board_of_directors']['ceo_relatives'] = {}
                    borrower['board_of_directors']['ceo_relatives']['additional_scrutiny'] = st.checkbox("Requires additional scrutiny for CEO relatives")

                    borrower['board_of_directors']['independent_directors_experience'] = {}
                    borrower['board_of_directors']['independent_directors_experience']['lending_banking_insurance'] = st.checkbox("Requires independent directors with experience in lending, banking, and insurance")

                    # Capital Adequacy
                    st.subheader("Capital Adequacy")
                    borrower['capital_adequacy'] = {}
                    borrower['capital_adequacy']['equity_base'] = st.number_input("Equity base", value=0, min_value=0)

                    borrower['capital_adequacy']['net_worth_less_100cr'] = {}
                    borrower['capital_adequacy']['net_worth_less_100cr']['marquee_investors_backing'] = st.checkbox("Requires marquee institutional equity investors backing")

                    # Capital Adequacy Ratio (CAR)
                    st.subheader("Capital Adequacy Ratio (CAR)")
                    borrower['capital_adequacy_ratio'] = {}
                    borrower['capital_adequacy_ratio']['car'] = st.number_input("CAR", value=0.0, min_value=0.0)

                    # Leverage (D/E ratio)
                    st.subheader("Leverage (D/E ratio)")
                    borrower['leverage'] = {}
                    borrower['leverage']['de_ratio_personal_loan'] = st.number_input("D/E ratio for personal loan business", value=0.0, min_value=0.0)
                    borrower['leverage']['de_ratio_secured_businesses'] = st.number_input("D/E ratio for secured businesses", value=0.0, min_value=0.0)
                    borrower['leverage']['de_ratio_housing_loan'] = st.number_input("D/E ratio for housing loan", value=0.0, min_value=0.0)
                    borrower['leverage']['de_ratio_microfinance'] = st.number_input("D/E ratio for microfinance", value=0.0, min_value=0.0)

                    # Portfolio Quality
                    st.subheader("Portfolio Quality")
                    borrower['portfolio_quality'] = {}
                    borrower['portfolio_quality']['par_dpd_unsecured'] = st.number_input("PAR/DPD for unsecured loans", value=0.0, min_value=0.0)
                    borrower['portfolio_quality']['par_dpd_microfinance'] = st.number_input("PAR/DPD for microfinance", value=0.0, min_value=0.0)
                    borrower['portfolio_quality']['par_dpd_secured'] = st.number_input("PAR/DPD for secured loans", value=0.0, min_value=0.0)
                    borrower['portfolio_quality']['provisions_unsecured'] = st.number_input("Provisions for unsecured loans", value=0, min_value=0)

                    # Profitability
                    st.subheader("Profitability")
                    borrower['profitability'] = {}
                    borrower['profitability']['roa'] = st.number_input("ROA", value=0.0, min_value=0.0)
                    borrower['profitability']['roe'] = st.number_input("ROE", value=0.0, min_value=0.0)

                    borrower['liquidity'] = st.checkbox("Liquidity")

                    # Asset Liability Management (ALM)
                    st.subheader("Asset Liability Management (ALM)")
                    borrower['asset_liability_management'] = {}
                    borrower['asset_liability_management']['positive_mismatch'] = st.checkbox("Positive mismatch in ALM")
                    borrower['asset_liability_management']['avg_tenor_alignment'] = st.checkbox("Average tenor alignment in ALM")

                    borrower['resource_profile'] = {}
                    borrower['resource_profile']['diversified_lender_base'] = st.checkbox("Diversified lender base")

                    # Operational Performance
                    st.subheader("Operational Performance")
                    borrower['operational_performance'] = {}
                    borrower['operational_performance']['collection_efficiency_personal_loans'] = st.number_input("Collection efficiency for personal loans", value=0, min_value=0)
                    borrower['operational_performance']['collection_efficiency_other_assets'] = st.number_input("Collection efficiency for other assets", value=0, min_value=0)
                    borrower['operational_performance']['total_collection_efficiency'] = st.checkbox("Total collection efficiency")
                    borrower['operational_performance']['aum_disbursements_growth'] = st.checkbox("AUM and disbursements growth")
                    borrower['operational_performance']['restructuring_loans'] = st.checkbox("Restructuring of loans")
                    borrower['operational_performance']['stressed_book'] = st.number_input("Stressed book", value=0, min_value=0)
                    borrower['operational_performance']['net_worth_stressed_portfolio'] = st.checkbox("Net worth vs stressed portfolio")
                    borrower['operational_performance']['aum_growth_vs_employees_growth'] = st.checkbox("AUM growth vs employees growth")
                    borrower['operational_performance']['net_interest_margin_growth'] = st.checkbox("Net interest margin growth")
                    borrower['operational_performance']['loan_book_outstanding_borrowings'] = st.checkbox("Loan book vs outstanding borrowings")
                    borrower['operational_performance']['unit_economics_loan_tenure'] = st.checkbox("Unit economics calculation for loan tenure")

                    return borrower

                def save_borrower(borrower):
                    print("XXX")
                    file_path = "borrower1.json"
                    print(file_path)
                    if file_path:
                        with open(file_path, 'r') as file:
                            existing_borrowers = json.load(file)
                            print(existing_borrowers)

                        # Append the new borrower to the existing borrowers
                        existing_borrowers.append(borrower)
                        print(existing_borrowers)

                        with open(file_path, 'w') as file:
                            json.dump(existing_borrowers, file)
                        st.success("Borrower details saved successfully!")

                # Main code
                st.title("Borrower Input Form")

                borrower = create_borrower()
                st.write(borrower)

                if st.button("Save Borrower"):
                    save_borrower(borrower)
        
            if sub_menu_option=="Run policy":
                st.write("Run Policy")   
                # Function to check adherence of borrower profiles to policies
                def check_adherence(policy):
                    st.subheader("Check Adherence")
                    borrower_data = st.file_uploader("Upload borrower dataset (JSON)", type=["json"])
                    if borrower_data:
                        borrower_data = json.load(borrower_data)
                        l_flag=False
                        for borrower in borrower_data:
                            borrower_id = borrower['id']
                            st.write(f"Borrower ID: {borrower_id}")
                            for param, param_value in policy.items():
                                if param == 'New_1':
                                    if param_value.get('Lending and non-lending businesses should be kept separate', False) and not borrower['separate_businesses']:
                                        st.write("Lending and non-lending businesses are not kept separate.")
                                    if param_value.get('Adhere to local money lending laws and fulfill all regulatory requirements', False) and not borrower['adhere_lending_laws']:
                                        st.write("Borrower does not adhere to local money lending laws and regulatory requirements.")
                                elif param == 'Track record - Promoter-driven entity':
                                    track_value = param_value
                                    if borrower['track_record']['promoter_driven']['years'] < track_value['min_years']:
                                        st.write(f"Track Record - Promoter-driven: Years less than {track_value['min_years']}")
                                elif param == 'Track record - Entity backed by institutional investors':
                                    track_value = param_value
                                    if borrower['track_record']['institutional_investors']['years'] < track_value['min_years']:
                                        st.write(f"Track Record - Institutional Investors: Years less than {track_value['min_years']}")
                                    if track_value['series_a_funding'] and not borrower['track_record']['institutional_investors']['series_a']:
                                        st.write("Track Record - Institutional Investors: Series A does not match")
                                elif param == 'Promoter and CXO qualifications - Relevant work experience':
                                    if borrower['promoter_cxo_qualifications']['work_experience'] != param_value['cxo_work_experience']:
                                        st.write("Promoter and CXO Qualifications: Work experience does not match")
                                elif param == 'Promoter and CXO qualifications - Relatives of CEO':
                                    if borrower['promoter_cxo_qualifications']['ceo_relatives']['due_diligence'] != param_value['ceo_relatives_diligence']:
                                        st.write("Promoter and CXO Qualifications: CEO relatives due diligence does not match")
                                elif param == 'Board of directors - Independent and nominee directors':
                                    if borrower['board_of_directors']['independent_nominee_directors'] != param_value['institutional_investors_directors']:
                                        st.write("Board of Directors: Independent and nominee directors do not match")
                                elif param == 'Board of directors - Additional scrutiny for CEO relatives':
                                    if borrower['board_of_directors']['ceo_relatives']['additional_scrutiny'] != param_value['ceo_relatives_diligence_additional']:
                                        st.write("Board of Directors: CEO relatives additional scrutiny does not match")
                                elif param == 'Board of directors - Independent directors experience':
                                    if borrower['board_of_directors']['independent_directors_experience']['lending_banking_insurance'] != param_value['independent_directors_experience']:
                                        st.write("Board of Directors: Independent directors experience does not match")
                                elif param == 'Capital Adequacy - Equity base':
                                    if borrower['capital_adequacy']['equity_base'] < param_value['min_equity_base']:
                                        l_flag=True
                                        st.write(f"Capital Adequacy: Equity base less than {param_value['min_equity_base']}")
                                elif param == 'Capital Adequacy - Marquee institutional equity investors' and l_flag:
                                    if 'net_worth_less_100cr' in borrower['capital_adequacy']:
                                        if borrower['capital_adequacy']['net_worth_less_100cr']['marquee_investors_backing'] != param_value['marquee_investors']:
                                            st.write(f"Capital Adequacy: Net worth less than 100cr, marquee investors backing does not match")
                                elif param == 'Capital Adequacy Ratio (CAR)':
                                    if borrower['capital_adequacy_ratio']['car'] < param_value['min_car_ratio']:
                                        st.write(f"Capital Adequacy Ratio: CAR less than {param_value['min_car_ratio']}")
                                elif param == 'Leverage (D/E ratio) - Personal loan business':
                                    if borrower['leverage']['de_ratio_personal_loan'] > param_value['max_de_ratio_personal_loan']:
                                        st.write(f"Leverage: D/E ratio for personal loans exceeds {param_value['max_de_ratio_personal_loan']}")
                                elif param == 'Leverage (D/E ratio) - Secured businesses':
                                    if borrower['leverage']['de_ratio_secured_businesses'] > param_value['max_de_ratio_secured_businesses']:
                                        st.write(f"Leverage: D/E ratio for secured businesses exceeds {param_value['max_de_ratio_secured_businesses']}")
                                elif param == 'Leverage (D/E ratio) - Housing, Loan against properties, and microfinance companies':
                                    if borrower['leverage']['de_ratio_housing_loan'] > param_value['max_de_ratio_other_businesses']:
                                        st.write(f"Leverage: D/E ratio for housing loans exceeds {param_value['max_de_ratio_other_businesses']}")
                                elif param == 'Portfolio Quality - Unsecured businesses':
                                    if borrower['portfolio_quality']['par_dpd_unsecured'] > param_value['max_par_unsecured_businesses']:
                                        st.write(f"Portfolio Quality: PAR/DPD for unsecured businesses exceeds {param_value['max_par_unsecured_businesses']}")
                                elif param == 'Portfolio Quality - Microfinance':
                                    if borrower['portfolio_quality']['par_dpd_microfinance'] > param_value['max_par_microfinance']:
                                        st.write(f"Portfolio Quality: PAR/DPD for microfinance exceeds {param_value['max_par_microfinance']}")
                                elif param == 'Portfolio Quality - Secured businesses':
                                    if borrower['portfolio_quality']['par_dpd_secured'] > param_value['max_par_secured_businesses']:
                                        st.write(f"Portfolio Quality: PAR/DPD for secured businesses exceeds {param_value['max_par_secured_businesses']}")
                                elif param == 'Provisions for NPAs - Unsecured loans':
                                    if not param_value:
                                        st.write("Portfolio Quality: Provisions for unsecured loans not maintained")
                                elif param == 'Profitability - Positive ROA':
                                    if not param_value['min_roa_positive']:
                                        st.write("Profitability: ROA is not positive")
                                elif param == 'Profitability - ROA range':
                                    if borrower['profitability']['roa'] < param_value['min_roa'] or borrower['profitability']['roa'] > param_value['max_roa']:
                                        st.write(f"Profitability: ROA not within the specified range")
                                elif param == 'Profitability - ROE range':
                                    if borrower['profitability']['roe'] < param_value['min_roe'] or borrower['profitability']['roe'] > param_value['max_roe']:
                                        st.write(f"Profitability: ROE not within the specified range")
                                elif param == 'Liquidity - Well-documented liquidity policy':
                                    if not borrower['liquidity']:
                                        st.write("Liquidity: Not adhering to liquidity policy")
                                elif param == 'Liquidity - Maintain operational expenses and debt repayment':
                                    if not param_value:
                                        st.write("Liquidity: Not maintaining operational expenses and debt repayment")
                                elif param == 'Asset Liability Management (ALM) - Positive mismatch':
                                    if not borrower['asset_liability_management']['positive_mismatch']:
                                        st.write("Asset Liability Management: Negative mismatch")
                                elif param == 'Asset Liability Management (ALM) - Long-term liabilities and short-term assets':
                                    if not borrower['asset_liability_management']['avg_tenor_alignment']:
                                        st.write("Asset Liability Management: Average tenor misalignment")
                                elif param == 'Resource Profile - Diversified lender base':
                                    if not borrower['resource_profile']['diversified_lender_base']:
                                        st.write("Resource Profile: Lender base not diversified")
                                elif param == 'Resource Profile - Maximum lender class exposure':
                                    if borrower['resource_profile'].get('max_lender_class_exposure', 0) > param_value['max_lender_class_exposure']:
                                        st.write(f"Resource Profile: Maximum lender class exposure exceeded {param_value['max_lender_class_exposure']}")
                                elif param == 'Operational Performance - Current collection efficiency - Personal loans':
                                    if borrower['operational_performance']['collection_efficiency_personal_loans'] < param_value['min_collection_efficiency_personal_loans']:
                                        st.write(f"Operational Performance: Collection efficiency for personal loans less than {param_value['min_collection_efficiency_personal_loans']}")
                                elif param == 'Operational Performance - Current collection efficiency - Other asset classes':
                                    if borrower['operational_performance']['collection_efficiency_other_assets'] < param_value['min_collection_efficiency_other_assets']:
                                        st.write(f"Operational Performance: Collection efficiency for other assets less than {param_value['min_collection_efficiency_other_assets']}")
                                elif param == 'Operational Performance - Total collection efficiency':
                                    if not borrower['operational_performance']['total_collection_efficiency']:
                                        st.write("Operational Performance: Total collection efficiency not adhered")
                                elif param == 'Operational Performance - Growing trend in AUM and disbursements':
                                    if not borrower['operational_performance']['aum_disbursements_growth']:
                                        st.write("Operational Performance: AUM and disbursements growth not maintained")
                                elif param == 'Operational Performance - Restructuring of loans':
                                    if borrower['operational_performance']['restructuring_loans'] != param_value['loan_restructuring']:
                                        st.write("Operational Performance: Restructuring of loans not used as a last resort")
                                elif param == 'Operational Performance - Net worth vs stressed portfolio':
                                    if not borrower['operational_performance']['net_worth_stressed_portfolio']:
                                        st.write("Operational Performance: Net worth less than stressed portfolio")
                                elif param == 'Operational Performance - YoY growth in AUM vs growth in total employees':
                                    if not borrower['operational_performance']['aum_growth_vs_employees_growth']:
                                        st.write("Operational Performance: AUM growth vs. employees growth not maintained")
                                elif param == 'Operational Performance - Net Interest Margin (NIM)':
                                    if not borrower['operational_performance']['net_interest_margin_growth']:
                                        st.write("Operational Performance: Net interest margin growth not maintained")
                                elif param == 'Operational Performance - Loan book vs outstanding borrowings':
                                    if not borrower['operational_performance']['loan_book_outstanding_borrowings']:
                                        st.write("Operational Performance: Loan book less than outstanding borrowings")
                                elif param == 'Operational Performance - Unit economics calculation':
                                    if borrower['operational_performance']['unit_economics_loan_tenure'] != param_value['loan_tenure_up_to_6_months']:
                                        st.write("Operational Performance: Unit economics calculated on loan tenure, not disbursements")
                            st.write()

                # Main function
                with open("borrow.json", "r") as f:
                    policies = json.load(f)
                if policies:
                    selected_policy = st.sidebar.selectbox("Select a policy", list(policies.keys()))
                    policy = policies[selected_policy]
                    check_adherence(policy)
                else:
                    st.warning("No policies found. Please create a policy first.")

    if opt=="Pool UW/Filtering":
        menu_option = st.sidebar.selectbox("Select an option", ["Create new pool", "Create pool policy","Check pool criteria"])

      
        if menu_option=="Create new pool":
            def save_borrower_to_json(borrower):
                borrower_id = datetime.now().strftime('%Y%m%d%H%M%S')
                filename = f"borrower_{borrower_id}.json"
                with open(filename, 'w') as file:
                    json.dump(borrower, file)
                st.success(f'Borrower data saved as {filename}.')

            def borrower_creation_form():
                st.title('Borrower Creation Form')

                # Input fields for all the parameters listed above
                tenor = st.number_input('Tenor (in years)', min_value=3, max_value=5, value=3)
                loan_cycles = st.number_input('Number of Loan Cycles', min_value=1, value=1)
                loan_ticket_size = st.number_input('Loan Ticket Size', min_value=0.0, value=100000.0, step=1000.0)
                interest_rate = st.number_input('Interest Rate', min_value=0.0, value=10.0, step=0.1)
                borrower_diversification = st.number_input('Number of Contracts', min_value=10000, value=10000, step=1000)
                geographical_diversification = st.text_input('Geographical Diversification')
                overdue_profile = st.radio('Overdue Profile', ['Last 6 EMIs on or before due date', 'Last 9 EMIs within 30 days'])
                product_mix = st.text_input('Product Mix')
                ltv_ratio = st.number_input('LTV Ratio (If Applicable)', min_value=40, max_value=60, value=50)
                bureau_score = st.number_input('Bureau Score', min_value=0, value=700)
                last_4_years_overdue = st.checkbox('No 90+ Overdue in Last 4 Years')
                promoter_age = st.number_input('Promoter Age', min_value=21, max_value=60, value=30)
                business_vintage = st.number_input('Business Vintage (in years)', min_value=2, value=2)
                enterprise_types = ['Proprietorship', 'Partnership Firm', 'Closely Held Private Limited Company']
                selected_enterprise_type = st.selectbox('Enterprise Type', enterprise_types)
                co_applicant_guarantor = st.checkbox('Prefer Co-applicant and Guarantor')
                has_bank_account = st.checkbox('Has Bank Account')
                disbursal_collections_digital = st.checkbox('Disbursals and Collections are Digital')

                if st.button('Create Borrower'):
                    # Process the form data and create a borrower object
                    borrower = {
                        'tenor': tenor,
                        'loan_cycles': loan_cycles,
                        'loan_ticket_size': loan_ticket_size,
                        'interest_rate': interest_rate,
                        'borrower_diversification': borrower_diversification,
                        'geographical_diversification': geographical_diversification,
                        'overdue_profile': overdue_profile,
                        'product_mix': product_mix,
                        'ltv_ratio': ltv_ratio,
                        'bureau_score': bureau_score,
                        'last_4_years_overdue': last_4_years_overdue,
                        'promoter_age': promoter_age,
                        'business_vintage': business_vintage,
                        'enterprise_type': selected_enterprise_type,
                        'co_applicant_guarantor': co_applicant_guarantor,
                        'has_bank_account': has_bank_account,
                        'disbursal_collections_digital': disbursal_collections_digital,
                    }
                    st.success('Borrower created successfully!')
                    save_borrower_to_json(borrower)
                    return borrower

            borrower=borrower_creation_form()

        if menu_option=="Create pool policy":
            def create_pool_policy():
                st.title('Create Policy and Save to JSON')

                # Input fields for all the policy parameters
                tenor_criteria = st.text_input('Tenor Criteria (min, max)', '3, 5')
                loan_cycles_criteria = st.number_input('Loan Cycles Criteria', min_value=1, value=1)
                loan_ticket_size_criteria = st.number_input('Loan Ticket Size Criteria', min_value=0.0, value=100000.0, step=1000.0)
                interest_rate_criteria = st.text_input('Interest Rate Criteria (min, max)', '0, 20')
                borrower_diversification_criteria = st.number_input('Borrower Diversification Criteria', min_value=10000, value=10000, step=1000)
                geographical_diversification_criteria = st.text_input('Geographical Diversification Criteria')
                overdue_profile_criteria = st.radio('Overdue Profile Criteria', ['Last 6 EMIs on or before due date', 'Last 9 EMIs within 30 days'])
                product_mix_criteria = st.text_input('Product Mix Criteria')
                ltv_ratio_criteria = st.text_input('LTV Ratio Criteria (min, max)', '40, 60')
                bureau_score_criteria = st.number_input('Bureau Score Criteria', min_value=0, value=700)
                last_4_years_overdue_criteria = st.checkbox('No 90+ Overdue in Last 4 Years')
                promoter_age_criteria = st.text_input('Promoter Age Criteria (min, max)', '21, 60')
                business_vintage_criteria = st.text_input('Business Vintage Criteria (min, max)', '2, 10')

                # Additional policy parameters
                eligible_enterprise_types = st.multiselect('Eligible Enterprise Types', ['Proprietorship', 'Partnership Firm', 'Closely Held Private Limited Company'])
                prefer_co_applicant_guarantor = st.checkbox('Prefer Co-applicant and Guarantor')
                require_bank_account = st.checkbox('Require Bank Account')
                digital_disbursal_collections = st.checkbox('Disbursals and Collections must be Digital')

                if st.button('Save Policy to JSON'):
                    # Process the form data and create a policy dictionary
                    policy = {
                        'tenor_criteria': tuple(map(int, tenor_criteria.split(','))),
                        'loan_cycles_criteria': loan_cycles_criteria,
                        'loan_ticket_size_criteria': loan_ticket_size_criteria,
                        'interest_rate_criteria': tuple(map(float, interest_rate_criteria.split(','))),
                        'borrower_diversification_criteria': borrower_diversification_criteria,
                        'geographical_diversification_criteria': geographical_diversification_criteria,
                        'overdue_profile_criteria': overdue_profile_criteria,
                        'product_mix_criteria': product_mix_criteria,
                        'ltv_ratio_criteria': tuple(map(int, ltv_ratio_criteria.split(','))),
                        'bureau_score_criteria': bureau_score_criteria,
                        'last_4_years_overdue_criteria': last_4_years_overdue_criteria,
                        'promoter_age_criteria': tuple(map(int, promoter_age_criteria.split(','))),
                        'business_vintage_criteria': tuple(map(int, business_vintage_criteria.split(','))),
                        'eligible_enterprise_types': eligible_enterprise_types,
                        'prefer_co_applicant_guarantor': prefer_co_applicant_guarantor,
                        'require_bank_account': require_bank_account,
                        'digital_disbursal_collections': digital_disbursal_collections,
                    }

                    # Save the policy to a JSON file
                    with open('policy.json', 'w') as file:
                        json.dump(policy, file)

                    st.success('Policy created and saved successfully!')

            create_pool_policy()

        if menu_option=="Check pool criteria":
            import streamlit as st
            import json

            def load_borrower_from_json(uploaded_file):
                content = uploaded_file.getvalue()
                return json.loads(content)
                # with open(filename, 'r') as file:
                #     return json.load(file)

            def load_policy_from_json(uploaded_file):
                content = uploaded_file.getvalue()
                return json.loads(content)

            def check_policy_adherence(borrower, policy):
                st.title('Policy Adherence Check')

                # Extract the policy criteria
                tenor_criteria = policy['tenor_criteria']
                loan_cycles_criteria = policy['loan_cycles_criteria']
                loan_ticket_size_criteria = policy['loan_ticket_size_criteria']
                interest_rate_criteria = policy['interest_rate_criteria']
                borrower_diversification_criteria = policy['borrower_diversification_criteria']
                geographical_diversification_criteria = policy['geographical_diversification_criteria']
                overdue_profile_criteria = policy['overdue_profile_criteria']
                product_mix_criteria = policy['product_mix_criteria']
                ltv_ratio_criteria = policy['ltv_ratio_criteria']
                bureau_score_criteria = policy['bureau_score_criteria']
                last_4_years_overdue_criteria = policy['last_4_years_overdue_criteria']
                promoter_age_criteria = policy['promoter_age_criteria']
                business_vintage_criteria = policy['business_vintage_criteria']

                # Additional policy criteria
                eligible_enterprise_types = set(policy['eligible_enterprise_types'])
                prefer_co_applicant_guarantor = policy['prefer_co_applicant_guarantor']
                require_bank_account = policy['require_bank_account']
                digital_disbursal_collections = policy['digital_disbursal_collections']

                # Perform policy adherence checks based on the borrower data and policy
                adherence_status = True

                if not (tenor_criteria[0] <= borrower['tenor'] <= tenor_criteria[1]):
                    st.error('Tenor criteria: Failed')
                    adherence_status = False
                else:
                    st.success('Tenor criteria: Passed')

                if borrower['loan_cycles'] < loan_cycles_criteria:
                    st.error('Loan Cycle criteria: Failed')
                    adherence_status = False
                else:
                    st.success('Loan Cycle criteria: Passed')

                if abs(borrower['loan_ticket_size'] - loan_ticket_size_criteria) / loan_ticket_size_criteria > 0.15:
                    st.error('Loan Ticket Size criteria: Failed')
                    adherence_status = False
                else:
                    st.success('Loan Ticket Size criteria: Passed')

                if not (interest_rate_criteria[0] <= borrower['interest_rate'] <= interest_rate_criteria[1]):
                    st.error('Interest Rate criteria: Failed')
                    adherence_status = False
                else:
                    st.success('Interest Rate criteria: Passed')

                if borrower['borrower_diversification'] < borrower_diversification_criteria:
                    st.error('Borrower Diversification criteria: Failed')
                    adherence_status = False
                else:
                    st.success('Borrower Diversification criteria: Passed')

                if borrower['enterprise_type'] not in eligible_enterprise_types:
                    st.error('Enterprise Type criteria: Failed')
                    adherence_status = False
                else:
                    st.success('Enterprise Type criteria: Passed')

                if prefer_co_applicant_guarantor and (not borrower['co_applicant_guarantor']):
                    st.warning('Co-applicant and Guarantor criteria: Preferred, but not met')
                else:
                    st.success('Co-applicant and Guarantor criteria: Passed')

                if require_bank_account and (not borrower['has_bank_account']):
                    st.error('Bank Account criteria: Failed')
                    adherence_status = False
                else:
                    st.success('Bank Account criteria: Passed')

                if digital_disbursal_collections and (not borrower['disbursal_collections_digital']):
                    st.error('Digital Disbursals and Collections criteria: Failed')
                    adherence_status = False
                else:
                    st.success('Digital Disbursals and Collections criteria: Passed')

                # Add checks for other parameters

                if adherence_status:
                    st.markdown('**Overall Adherence Status: Passed**')
                else:
                    st.markdown('**Overall Adherence Status: Failed**')

            # def chainlink_uw():

            #     command =["npx hardhat functions-read --contract 0xB28b0Ce6F42CD3Aa80CF06b814997872bC9462D4  --network polygonMumbai --configpath tutorials/4-post-data/config.js",
            #     "npx env-enc set-pw","npx env-enc set","npx hardhat compile",]
            #     try:
            #         working_directory = "/Users/nishikant_gravityx/functions-hardhat-starter-kit"
            #         process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,cwd=working_directory)
            #         # Wait for the command to complete
            #         stdout, stderr = process.communicate()
            #         # Print the command output to Streamlit
            #         if stdout:
            #             st.code(stdout.decode('utf-8'))
            #         if stderr:
            #             st.error(stderr.decode('utf-8'))

            #     except subprocess.CalledProcessError as e:
            #         # In case of an error, print the error output to Streamlit
            #         st.error(f"Error occurred: {e}")
                    # st.write(e.stderr)
            

            st.title('Check Borrower Adherence against Policy')

            borrower_json_file = st.file_uploader('Upload Borrower JSON File', type=['json'])
            if borrower_json_file:
                borrower_data = load_borrower_from_json(borrower_json_file)
                policy_json_file = st.file_uploader('Upload Policy JSON File', type=['json'])
                if policy_json_file:
                    policy_data = load_policy_from_json(policy_json_file)

                    if st.button('Check Policy Adherence'):
                        # chainlink_uw()
                        check_policy_adherence(borrower_data, policy_data)


    

    if opt=="Borrower UW":
        menu_option = st.sidebar.selectbox("Select an option", ["Generate Borrower Profile", "Create UW policy","Check UW criteria"])
        if menu_option =="Generate Borrower Profile":
            def save_to_json(data):
                with open('borrower_details.json', 'w') as file:
                    json.dump(data, file)

            def get_user_input():
                gm1,gm2=st.columns(2)
                # Borrower Eligibility
                with gm1:
                    st.header("Borrower Eligibility")
                    b_id = st.number_input("ID", value=1, min_value=1)
                    lending_business = st.checkbox("Is the company's prime business lending?")
                    adhere_lending_laws = st.checkbox("Does the Company Adhere to Local Lending Laws?")
                    track_record_years = st.number_input("Number of years of track record:", min_value=0, step=1)
                    institutional_investment = st.checkbox("Is the company backed by institutional investors?")
                    if institutional_investment:
                        series_a_raised = st.checkbox("Has the company raised at least Series A funding?")
                    else:
                        series_a_raised = "NA"
                
                with gm1:
                    # Promoter and CXO Evaluation
                    st.header("Promoter and CXO Evaluation")
                    promoter_expertise = st.checkbox("Promoter's expertise in money lending business?")
                    cxo_work_experience = st.checkbox("CXO's have relevant work experience?")
                    ceo_relatives_additional_dd = st.checkbox("Require additional due diligence for CEO relatives holding CXO level positions?")


                    # Company Board and Independent Directors
                    st.header("Company Board Directors")
                    independent_director_presence = st.checkbox("Do they have board of directors or independent/nominee directors")
                    independent_director_experience = st.checkbox("Do independent directors have experience in lending, banking, insurance, or related?")
                    major_institutional_investors = st.checkbox("Are there independent and nominee directors from major institutional investors?")

                with gm1:
                    # Capital Adequacy
                    st.header("Capital Adequacy")
                    equity_base = st.number_input("Equity base (USD):", min_value=0, step=1)
                    net_worth = st.number_input("Net worth (USD):", min_value=1, step=1)
                    aum = st.number_input("Assets Under Management (USD):", min_value=1, step=1)
                    car = equity_base / aum
                    st.write("Capital Adequacy Ratio: ", car)

                    # Leverage
                    st.header("Leverage")
                    total_outstanding_debt = st.number_input("total_outstanding_debt", min_value=0.0, step=0.1)
                    fldg_gurantees = st.number_input("fldg_guarantees", min_value=0.0, step=0.1)
                    intangible_assets = st.number_input("intangible_assets", min_value=0.0, step=0.1)
                    adjusted_tangible_nw = (equity_base) - (fldg_gurantees) - (intangible_assets)
                    if adjusted_tangible_nw == 0.0:
                        DE_ratio = total_outstanding_debt
                    else:
                        DE_ratio = total_outstanding_debt / adjusted_tangible_nw
                    st.write("D/E ratio",DE_ratio)
                    loan_de_type = st.selectbox("Which loan types", ["Personal loan business", "secured loan business",
                                                                    " housing, loan against properties, and microfinance companies"])
                
                with gm2:
                    # Portfolio Quality
                    st.header("Portfolio Quality")
                    par = st.number_input("Portfolio at Risk:", min_value=0.0, step=0.1)
                    dpd = st.number_input("Days past due 0+", min_value=0.0, step=0.1)
                    dpd30 = st.number_input("Days past due 30+", min_value=0.0, step=0.1)
                    dpd90 = st.number_input("Days past due 90+ (Gross NPAs)", min_value=0.0, step=0.1)
                    past_12_months_write_offs = st.number_input("Past 12 months write-offs:", min_value=0, step=1)
                    actual_portfolio_quality = dpd90 + past_12_months_write_offs
                    st.write("Actual Portfolio Quality", actual_portfolio_quality)
                    unsecured_provisions = st.checkbox("Does the company make 100% provisions for NPAs in case of unsecured loans?")

                    # Profitability
                    st.header("Profitability")
                    roa = st.number_input("Return on Assets (ROA) for the past three years:", min_value=0.0, step=0.01)
                    roe = st.number_input("Return on Equity (ROE) percentage:", min_value=0, step=1)

                    # Liquidity
                    st.header("Liquidity")
                    liquidity_policy = st.checkbox("Do they have a well-documented liquidity policy?")
                    opex_liquidity = st.checkbox("Do they have minimum 2-3 months operations expenses liquidity?")
                    repay_liquidity = st.checkbox("Do they have minimum 2-3 months debt repay obligations liquidity?")
                    mf_liquidity = st.checkbox("Do they have liquid short-term mutual funds?")
                    obligations_from_guarantees = st.checkbox("Do they have obligations arising from guarantees provided by the firm?")


                with gm1:
                    # Asset Liability Management (ALM)
                    st.header("Asset Liability Management (ALM)")
                    loan_assets = st.number_input("loan_assets", min_value=0.0, step=0.01)
                    deposits_borrowings_liabilities = st.number_input("deposits_borrowings_liabilities", min_value=0.0, step=0.01)
                    static_alm = loan_assets + deposits_borrowings_liabilities
                    st.write("Static_ALM", static_alm)
                    inflow_from_loans_given = st.number_input("inflow from loans given", min_value=0.0, step=0.01)
                    outflow_to_loans_taken = st.number_input("outflow to loan taken", min_value=0.0, step=0.01)
                    if inflow_from_loans_given > outflow_to_loans_taken:
                        positive_mismatch = True
                    else:
                        positive_mismatch = False
                    avg_tenor_loans = st.number_input("Average tenor of loans given:", min_value=0, step=1)
                    avg_tenor_borrowings = st.number_input("Average tenor of borrowings:", min_value=0, step=1)

                    # Resource Profile
                    st.header("Resource Profile")
                    diversified_lender_base = st.checkbox("Does the company have a diversified lender base other than banks?")
                    forty_percent_check = st.checkbox("Does any non-bank lenders represent 40 percent of borrowings?")


                with gm2:
                # Operational Performance
                    st.header("Operational Performance")
                    current_collection = st.number_input("Current Collection", min_value=0.0, step=0.1)
                    overdue_collection = st.number_input("Overdue Collection", min_value=0.0, step=0.1)
                    current_demand = st.number_input("Current Demand", min_value=0.1, step=0.1)

                    current_collection_efficiency = current_collection / current_demand
                    total_collection_efficiency = (current_collection + overdue_collection) / current_demand
                    total_collection_efficiency = st.number_input("Total collection efficiency (past 12 months average):", min_value=0.0,
                                                                step=0.1)
                    aum_growth = st.number_input("Growth in AUM (average for the last 3 years or last 6 quarters):", min_value=0.0,
                                                step=0.01)

                    GNPA = st.number_input("GNPA", min_value=0.0, step=0.1)
                    restructured_portfolio = st.number_input("Restructured portfolio", min_value=0.0, step=0.1)
                    portfolio_90_bucket = st.number_input("portfolio in 90+ bucket for restructured portfolio ", min_value=0.0,
                                                        step=0.1)
                    stressed_book = (GNPA) + (restructured_portfolio) - (portfolio_90_bucket)
                    st.write("Stressed Book", stressed_book)

                    yield_portfolio = st.number_input("Yield on Portfolio", min_value=0.0, step=0.1)
                    cost_of_funds = st.number_input("Cost of Funds", min_value=0.0, step=0.1)
                    NIM = (yield_portfolio) - (cost_of_funds)
                    st.write("Net Interest Margin", NIM)
                    st.write("Net worth", net_worth)

                    restructuring_loans = st.checkbox("Does the company occasionally take restructuring of loans?")
                    if net_worth > stressed_book:
                        networth_stressed_portfolio_check = True
                    else:
                        networth_stressed_portfolio_check = False

                    YoY_growth_emp = st.number_input("YoY growth employess (%)", min_value=0.0, step=0.1)
                    YoY_growth_nim = st.number_input("YoY growth NIM (%)", min_value=0.0, step=0.1)

                    growth_aum_vs_employees = st.checkbox("YoY growth in AUM should be more than growth in total employees:")
                    growth_nim = st.checkbox("YoY positive growth in NIM?")
                    loan_book_vs_outstanding_borrowings = st.checkbox("Loan book ratio to outstanding borrowings greater than 1.1?")

                # Display submit button
                if st.button("Submit"):
                    data = {
                        "Borrower Eligibility": {
                            "ID": b_id,
                            "Lending Business": lending_business,
                            "Adhere to Local Lending Laws": adhere_lending_laws,
                            "Track Record Years": track_record_years,
                            "Institutional Investment": institutional_investment,
                            "Series A Raised": series_a_raised
                        },
                        "Promoter and CXO Evaluation": {
                            "Promoter's Expertise": promoter_expertise,
                            "CXO's Relevant Work Experience": cxo_work_experience,
                            "Additional Due Diligence for CEO Relatives": ceo_relatives_additional_dd
                        },
                        "Company Board and Independent Directors": {
                            "Presence of Board or Independent/Nominee Directors": independent_director_presence,
                            "Independent Directors Experience": independent_director_experience,
                            "Independent/Nominee Directors from Major Institutional Investors": major_institutional_investors
                        },
                        "Capital Adequacy": {
                            "Equity Base (USD)": equity_base,
                            "Net Worth (USD)": net_worth,
                            "Assets Under Management (USD)": aum,
                            "Capital Adequacy Ratio": car
                        },
                        "Leverage": {
                            "Total Outstanding Debt": total_outstanding_debt,
                            "FLDG Guarantees": fldg_gurantees,
                            "Intangible Assets": intangible_assets,
                            "Adjusted Tangible Net Worth": adjusted_tangible_nw,
                            "Leverage Ratio": DE_ratio,
                            "Loan Type": loan_de_type
                        },
                        "Portfolio Quality": {
                            "Portfolio at Risk": par,
                            "Days Past Due 0+": dpd,
                            "Days Past Due 30+": dpd30,
                            "Days Past Due 90+ (Gross NPAs)": dpd90,
                            "Past 12 Months Write-offs": past_12_months_write_offs,
                            "Actual Portfolio Quality": actual_portfolio_quality,
                            "Unsecured Provisions": unsecured_provisions
                        },
                        "Profitability": {
                            "Return on Assets (ROA) for the Past Three Years": roa,
                            "Return on Equity (ROE)": roe
                        },
                        "Liquidity": {
                            "Liquidity Policy": liquidity_policy,
                            "Operational Expenses Liquidity": opex_liquidity,
                            "Debt Repayment Obligations Liquidity": repay_liquidity,
                            "Liquid Short-term Mutual Funds": mf_liquidity,
                            "Obligations from Guarantees": obligations_from_guarantees
                        },
                        "Asset Liability Management (ALM)": {
                            "Loan Assets": loan_assets,
                            "Deposits/Borrowings Liabilities": deposits_borrowings_liabilities,
                            "Static ALM": static_alm,
                            "Inflow from Loans Given": inflow_from_loans_given,
                            "Outflow to Loans Taken": outflow_to_loans_taken,
                            "Positive Mismatch": positive_mismatch,
                            "Average Tenor of Loans Given": avg_tenor_loans,
                            "Average Tenor of Borrowings": avg_tenor_borrowings
                        },
                        "Resource Profile": {
                            "Diversified Lender Base": diversified_lender_base,
                            "Non-Bank Lenders Represent 40% of Borrowings": forty_percent_check
                        },
                        "Operational Performance": {
                            "Current Collection": current_collection,
                            "Overdue Collection": overdue_collection,
                            "Current Demand": current_demand,
                            "Current Collection Efficiency": current_collection_efficiency,
                            "Total Collection Efficiency (Past 12 Months Average)": total_collection_efficiency,
                            "Growth in AUM (Average for the Last 3 Years or Last 6 Quarters)": aum_growth,
                            "GNPA": GNPA,
                            "Restructured Portfolio": restructured_portfolio,
                            "Portfolio in 90+ Bucket for Restructured Portfolio": portfolio_90_bucket,
                            "Stressed Book": stressed_book,
                            "Yield on Portfolio": yield_portfolio,
                            "Cost of Funds": cost_of_funds,
                            "Net Interest Margin": NIM,
                            "Restructuring Loans": restructuring_loans,
                            "Net Worth > Stressed Portfolio": networth_stressed_portfolio_check,
                            "YoY Growth in Employees (%)": YoY_growth_emp,
                            "YoY Growth in NIM (%)": YoY_growth_nim,
                            "YoY Growth in AUM > Growth in Total Employees": growth_aum_vs_employees,
                            "YoY Positive Growth in NIM": growth_nim,
                            "Loan Book Ratio to Outstanding Borrowings > 1.1": loan_book_vs_outstanding_borrowings
                        }
                    }

                    save_to_json(data)


            get_user_input()

        if menu_option == "Create UW policy":
            
            # Function to save the policy as JSON
            def save_as_json_file(policy, file_name):
                with open(file_name, "w") as f:
                    json.dump(policy, f, indent=4)
                st.success(f"Policy saved as {file_name}")
        
            # Default policy rules
            default_policy = {
                "Entity Focus and Business Separation": {
                    "Lending Business Focus": True,
                    "Separate Lending and Non-lending Businesses": True
                },
                "Borrower Eligibility": {
                    "Adhere to Local Lending Laws": True,
                    "Track Record Years": 5,
                    "Institutional Investment": True,
                    "Series A Raised": True
                },
                "Promoter and CXO Evaluation": {
                    "Promoter's Expertise": True,
                    "CXO's Relevant Work Experience": True,
                    "Additional Due Diligence for CEO Relatives": False
                },
                "Board of Directors": {
                    "Presence of Board or Independent/Nominee Directors": True,
                    "Independent Directors Experience": True,
                    "Independent/Nominee Directors from Major Institutional Investors": True
                },
                "Capital Adequacy": {
                    "Equity Base (USD)": 2000000,
                    "Net Worth (USD)": 1000000,
                    "Capital Adequacy Ratio": 20.0
                },
                "Leverage": {
                    "Debt-to-Equity (D/E) Ratio for Personal Loans": 2.5,
                    "Debt-to-Equity (D/E) Ratio for Secured Loans": 5.0,
                    "Debt-to-Equity (D/E) Ratio for Housing, Loan against Property, and Microfinance": 5.0,
                    "Leverage Ratio": 5.0
                },
                "Portfolio Quality": {
                    "Portfolio at Risk (PAR) for Unsecured Loans": 0.08,
                    "Portfolio at Risk (PAR) for Microfinance": 0.05,
                    "Portfolio at Risk (PAR) for Secured Loans": 0.03,
                    "Provisions for NPAs (Unsecured Loans)": 1.0
                },
                "Profitability": {
                    "Return on Assets (ROA) for the Past Three Years": 2.0,
                    "Return on Equity (ROE)":20
                },
                "Liquidity": {
                    "Liquidity Policy": True,
                    "Operational Expenses Liquidity": True,
                    "Debt Repayment Obligations Liquidity": True,
                    "Liquid Short-term Mutual Funds": True,
                    "Obligations from Guarantees": True
                },
                "Asset Liability Management (ALM)": {
                    "Positive Mismatch": True
                },
                "Resource Profile": {
                    "Diversified Lender Base": True,
                    "Non-Bank Lenders Represent 40% of Borrowings": True
                },
                "Operational Performance": {
                    "Current Collection Efficiency for Personal Loans (%)": 85,
                    "Current Collection Efficiency for Other Asset Classes (%)": 90,
                    "Total Collection Efficiency (Past 12 Months Average)": 90,
                    "Growth in AUM (Average for the Last 3 Years or Last 6 Quarters)": 30,
                    "Restructuring of Loans (Occasional Use)": False
                }
            }

            # Streamlit app
            def policy_creation():
                
                st.title("Policy Creation Form")
                st.write("Edit the policy rules and save as JSON.")

                policy = {}

                # Create sections for each policy
                for section, rules in default_policy.items():
                    st.header(section)
                    section_rules = {}
                    for rule, default_value in rules.items():
                        if isinstance(default_value, bool):
                            section_rules[rule] = st.checkbox(rule, value=default_value)
                        else:
                            section_rules[rule] = st.number_input(rule, value=default_value)
                    policy[section] = section_rules

                file_name = st.text_input("Enter the file name for the policy JSON:", "policy.json")

                if st.button("Save Policy"):
                    save_as_json_file(policy, file_name)



            policy_creation()

        if menu_option == "Check UW criteria":
            def check_eligibility(borrower_data, policy_data):
                for section, rules in policy_data.items():
                    st.subheader(section)
                    for rule, policy_value in rules.items():
                        borrower_value = borrower_data.get(section, {}).get(rule, None)
                        if borrower_value is None:
                            flag=1
                        elif isinstance(policy_value, bool):
                            st.write(f"{rule}: {'Passed' if borrower_value == policy_value else 'Failed'}")
                        else:
                            st.write(f"{rule}: {'Passed' if borrower_value >= policy_value else 'Failed'}")

            def uw_main():
                st.title("Credit Policy Checker")
                st.write("Upload the borrower JSON and policy JSON to check eligibility.")

                # Upload borrower JSON
                st.subheader("Upload Borrower JSON")
                borrower_file = st.file_uploader("Choose a borrower json file", type=["json"])
                if borrower_file is not None:
                    borrower_data = json.load(borrower_file)

                # Upload policy JSON
                st.subheader("Upload Policy JSON")
                policy_file = st.file_uploader("Choose a credit policy file", type=["json"])
                if policy_file is not None:
                    policy_data = json.load(policy_file)

                if st.button("Check Eligibility") and 'borrower_data' in locals() and 'policy_data' in locals():
                    check_eligibility(borrower_data, policy_data)

            
            uw_main()

    if opt=="Generate Imp Ratios":
        st.write("Enter Your Assessment")
        def create_borrower():
                st.subheader("Create Borrower")
                borrower = {}

                borrower['id'] = st.number_input("ID",value=1,min_value=1)

                borrower['lending_business'] = st.checkbox("Lending Business")
                borrower['separate_businesses'] = st.checkbox("Separate Businesses")
                borrower['adhere_lending_laws'] = st.checkbox("Adhere to Lending Laws")

                # Track record
                st.subheader("Track record")
                borrower['track_record'] = {}
                borrower['track_record']['promoter_driven'] = {}
                borrower['track_record']['promoter_driven']['years'] = st.number_input("Promoter-driven years", value=0, min_value=0)

                borrower['track_record']['institutional_investors'] = {}
                borrower['track_record']['institutional_investors']['years'] = st.number_input("Institutional investors years", value=0, min_value=0)
                borrower['track_record']['institutional_investors']['series_a'] = st.checkbox("Requires series A funding (Institutional investors)")

                # Promoter and CXO qualifications
                st.subheader("Promoter and CXO qualifications")
                borrower['promoter_cxo_qualifications'] = {}
                borrower['promoter_cxo_qualifications']['work_experience'] = st.checkbox("Requires work experience")

                borrower['promoter_cxo_qualifications']['ceo_relatives'] = {}
                borrower['promoter_cxo_qualifications']['ceo_relatives']['due_diligence'] = st.checkbox("Requires due diligence for CEO relatives")

                # Board of directors
                st.subheader("Board of directors")
                borrower['board_of_directors'] = {}
                borrower['board_of_directors']['independent_nominee_directors'] = st.checkbox("Requires independent and nominee directors")

                borrower['board_of_directors']['ceo_relatives'] = {}
                borrower['board_of_directors']['ceo_relatives']['additional_scrutiny'] = st.checkbox("Requires additional scrutiny for CEO relatives")

                borrower['board_of_directors']['independent_directors_experience'] = {}
                borrower['board_of_directors']['independent_directors_experience']['lending_banking_insurance'] = st.checkbox("Requires independent directors with experience in lending, banking, and insurance")

                # Capital Adequacy
                st.subheader("Capital Adequacy")
                borrower['capital_adequacy'] = {}
                borrower['capital_adequacy']['equity_base'] = st.number_input("Equity base", value=0, min_value=0)

                borrower['capital_adequacy']['net_worth_less_100cr'] = {}
                borrower['capital_adequacy']['net_worth_less_100cr']['marquee_investors_backing'] = st.checkbox("Requires marquee institutional equity investors backing")

                # Capital Adequacy Ratio (CAR)
                st.subheader("Capital Adequacy Ratio (CAR)")
                borrower['capital_adequacy_ratio'] = {}
                borrower['capital_adequacy_ratio']['car'] = st.number_input("CAR", value=0.0, min_value=0.0)

                # Leverage (D/E ratio)
                st.subheader("Leverage (D/E ratio)")
                borrower['leverage'] = {}
                borrower['leverage']['de_ratio_personal_loan'] = st.number_input("D/E ratio for personal loan business", value=0.0, min_value=0.0)
                borrower['leverage']['de_ratio_secured_businesses'] = st.number_input("D/E ratio for secured businesses", value=0.0, min_value=0.0)
                borrower['leverage']['de_ratio_housing_loan'] = st.number_input("D/E ratio for housing loan", value=0.0, min_value=0.0)
                borrower['leverage']['de_ratio_microfinance'] = st.number_input("D/E ratio for microfinance", value=0.0, min_value=0.0)

                # Portfolio Quality
                st.subheader("Portfolio Quality")
                borrower['portfolio_quality'] = {}
                borrower['portfolio_quality']['par_dpd_unsecured'] = st.number_input("PAR/DPD for unsecured loans", value=0.0, min_value=0.0)
                borrower['portfolio_quality']['par_dpd_microfinance'] = st.number_input("PAR/DPD for microfinance", value=0.0, min_value=0.0)
                borrower['portfolio_quality']['par_dpd_secured'] = st.number_input("PAR/DPD for secured loans", value=0.0, min_value=0.0)
                borrower['portfolio_quality']['provisions_unsecured'] = st.number_input("Provisions for unsecured loans", value=0, min_value=0)

                # Profitability
                st.subheader("Profitability")
                borrower['profitability'] = {}
                borrower['profitability']['roa'] = st.number_input("ROA", value=0.0, min_value=0.0)
                borrower['profitability']['roe'] = st.number_input("ROE", value=0.0, min_value=0.0)

                borrower['liquidity'] = st.checkbox("Liquidity")

                # Asset Liability Management (ALM)
                st.subheader("Asset Liability Management (ALM)")
                borrower['asset_liability_management'] = {}
                borrower['asset_liability_management']['positive_mismatch'] = st.checkbox("Positive mismatch in ALM")
                borrower['asset_liability_management']['avg_tenor_alignment'] = st.checkbox("Average tenor alignment in ALM")

                borrower['resource_profile'] = {}
                borrower['resource_profile']['diversified_lender_base'] = st.checkbox("Diversified lender base")

                # Operational Performance
                st.subheader("Operational Performance")
                borrower['operational_performance'] = {}
                borrower['operational_performance']['collection_efficiency_personal_loans'] = st.number_input("Collection efficiency for personal loans", value=0, min_value=0)
                borrower['operational_performance']['collection_efficiency_other_assets'] = st.number_input("Collection efficiency for other assets", value=0, min_value=0)
                borrower['operational_performance']['total_collection_efficiency'] = st.checkbox("Total collection efficiency")
                borrower['operational_performance']['aum_disbursements_growth'] = st.checkbox("AUM and disbursements growth")
                borrower['operational_performance']['restructuring_loans'] = st.checkbox("Restructuring of loans")
                borrower['operational_performance']['stressed_book'] = st.number_input("Stressed book", value=0, min_value=0)
                borrower['operational_performance']['net_worth_stressed_portfolio'] = st.checkbox("Net worth vs stressed portfolio")
                borrower['operational_performance']['aum_growth_vs_employees_growth'] = st.checkbox("AUM growth vs employees growth")
                borrower['operational_performance']['net_interest_margin_growth'] = st.checkbox("Net interest margin growth")
                borrower['operational_performance']['loan_book_outstanding_borrowings'] = st.checkbox("Loan book vs outstanding borrowings")
                borrower['operational_performance']['unit_economics_loan_tenure'] = st.checkbox("Unit economics calculation for loan tenure")

                return borrower

        def save_borrower(borrower):
            print("XXX")
            file_path = "borrower1.json"
            print(file_path)
            if file_path:
                with open(file_path, 'r') as file:
                    existing_borrowers = json.load(file)
                    print(existing_borrowers)

                # Append the new borrower to the existing borrowers
                existing_borrowers.append(borrower)
                print(existing_borrowers)

                with open(file_path, 'w') as file:
                    json.dump(existing_borrowers, file)
                st.success("Borrower details saved successfully!")

        # Main code
        st.title("Borrower Input Form")

        borrower = create_borrower()
        st.write(borrower)

        if st.button("Save Borrower"):
            save_borrower(borrower)
