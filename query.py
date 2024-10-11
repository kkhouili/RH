import mysql.connector
import streamlit as st
import pandas as pd

#connection

conn=mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root",
    passwd="",
    db="myDb"
    
    
)

c=conn.cursor()
#query
def view_all_data():
    c.execute('select * from testfp order by site asc')
    data=c.fetchall()
    return data
