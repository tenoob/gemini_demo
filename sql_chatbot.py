#prompt is given to gemini llm which gives a sql query which is given to a db from which the response is reverted back

from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import sqlite3
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#fun to load gemini and provide sql query as response
def get_sql_response(question,prompt):
    model = genai.GenerativeModel()
    response = model.generate_content([prompt[0],question])
    return response.text

#fun to retrive query from sql db using query from gemini 
def read_sql_query(sql,db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows


prompt = [
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name Employee and has the following columns - NAME, DEPARTMENT, 
    ROLE and SALARY \n\nFor example,\nExample 1 - How many entries of records are present?, 
    the SQL command will be something like this SELECT COUNT(*) FROM Employee ;
    \nExample 2 - Tell me all the employee working in Sales Department?, 
    the SQL command will be something like this SELECT * FROM Employee 
    where DEPARTMENT="Sales"; 
    also the sql code should not have ``` in beginning or end and sql word in output
    """
]

#streamlit app
st.set_page_config(page_title="SQL helper")
st.header("Gemini App")

question =st.text_input("Input",key='input')
submit = st.button("Ask for query")

if submit:
    response = get_sql_response(question=question,prompt=prompt)
    st.subheader(f"Sql Query is: {response}")
    sql_response = read_sql_query(response,"demo.db")
    print(sql_response)
    st.subheader("Data is:")
    for row in sql_response:
        print(row)
        st.subheader(row)
