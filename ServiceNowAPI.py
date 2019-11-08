# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Luis Fuentes & Marco Rodriguez
# To compile run pyinstaller -w -F [your_python_file]

import requests
import os
import csv

# URL
SN_url = 'https://generalatomicsprod.service-now.com/'
report_url = '''https://generalatomicsprod.service-now.com/nav_to.do?uri=%2Fsys_report_template.do%3Fjvar_report_id%3D366749e31312ff4880b8bd395144b0cc%26jvar_selected_tab%3DmyReports%26jvar_list_order_by%3D%26jvar_list_sort_direction%3D%26sysparm_reportquery%3D%26jvar_search_created_by%3D%26jvar_search_table%3D%26jvar_search_report_sys_id%3D%26jvar_report_home_query%3D&CSV'''

# Open a session
s = requests.session()

# Getting credentials
absolut_path = os.getcwd()

with open(f'{os.getcwd()}/info.csv') as f:
    csv_reader = csv.reader(f, delimiter=',')
    for row in csv_reader:
        user = row[0]
        pwd = row[1]

# Getting the payload 
payload = {'UserName': 'ga.com\\{user}'.format(user=user),
           'Password': pwd,
           'AuthMethod': 'FormsAuthentication'}

# GET ServiceNow URL
r = s.get(SN_url)

# Follow 302 redirect to IDP login system
auth_url = r.url # Comment out if not needed

# POST login request
s.post(auth_url, data=payload) # comment out if not needed 

# Do the HTTP request
response = s.get(report_url)

if response.status_code != 400: 
    print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.content)
    exit()

# Writes data to a CSV type of file
with open(f'{os.getcwd()}/ServiceNowReport.csv', 'wb') as excel_file:
    excel_file.write(response.content)
