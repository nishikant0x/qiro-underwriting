import streamlit as st
import borrower
import lender
import underwriter
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import sqlite3
import pandas as pd

st.set_page_config(layout="wide") 

# Dictionary to map page names to the corresponding page modules
PAGES = {
    "Borrower": borrower,
    "Lender": lender,
    "Underwriter": underwriter
}

def main():
   

    conn = sqlite3.connect('my_db.db')
    c = conn.cursor()
    
    c.execute("""
    CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        link TEXT)""")

    # c.execute("""
    #     CREATE TABLE IF NOT EXISTS files (
    #         id INTEGER PRIMARY KEY,
    #         name TEXT,
    #         type TEXT,
    #         data BLOB
    #     )
    # """)

    # conn.commit()

    # gauth = GoogleAuth()
    # gauth.LocalWebserverAuth()  # Authenticate with Google Drive API
    # drive = GoogleDrive(gauth)

    # st.title("File Uploader and Display")



   

    # def save_to_google_drive(uploaded_files):
    #     file_links = []
    #     for file in uploaded_files:
    #         gfile = drive.CreateFile({'title': file.name})
    #         gfile.SetContentFile(file.name)
    #         gfile.Upload()
    #         file_links.append(gfile['alternateLink'])
    #     return file_links

    # def save_to_database(file_links):
    #     for link in file_links:
    #         c.execute("""
    #             INSERT INTO files (link)
    #             VALUES (?)
    #         """, (link,))

    #     conn.commit()

    # def display_links_from_database():
    #     # c.execute("SELECT link FROM files")
    #     # rows = c.fetchall()

    #     # for row in rows:
    #     #     link = row[0]
    #     #     st.markdown(f"[Link to File]({link})")

    #     df = pd.read_sql_query("SELECT * FROM files", conn)
    #     st.table(df)

    # uploaded_files = st.file_uploader("Upload files:", accept_multiple_files=True)

    # if uploaded_files:
    #     file_links=save_to_google_drive(uploaded_files)
    #     save_to_database(file_links)
    #     display_links_from_database()
    
    # Create a selectbox for the user to choose a page
    page = st.sidebar.selectbox("Select a View:", tuple(PAGES.keys()))
    # Execute the function corresponding to the selected page
    page_module = PAGES[page]
    if(page=="borrower"):
        page_module.app()
    else:
        page_module.app()

if __name__ == "__main__":
    main()
