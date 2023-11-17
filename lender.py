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

def app():
    with st.sidebar:
        opt=st.radio("Select Option",('Underwriting Report','Active Risk Tracking'))

    if opt=="Underwriting Report":
        st.write("Report")

    if opt=="Active Risk Tracking":
        st.write("Active Risk")