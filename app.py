import streamlit as st
import yaml
import mysql.connector as mysql
from db_connection import get_database_connection
from sqlalchemy import create_engine
from uuid import uuid1

 
cursor, db = get_database_connection()
 
# cursor.execute("SHOW DATABASES")
 
# databases = cursor.fetchall() ## it returns a list of all databases present
 
# st.write(databases)
 
# cursor.execute('''CREATE TABLE information (id varchar(255),
#                                               studentname varchar(255),
#                                               re_date date,
#												status varchar(255))''')
# cursor.execute("Select * from information")
# tables = cursor.fetchall()
# st.write(tables)

# cursor.execute('''CREATE TABLE information (id varchar(20) PRIMARY KEY,
#                                       student_name varchar(255),
#                                       fathers_name varchar(255),
#                                       mothers_name varchar(255),
#                                       present_address varchar(500),
#                                       permanent_address varchar(500),
#                                       contact_no varchar(11),
#                                       email varchar(255),
#                                       gpa varchar(10),
#                                       religion varchar(255),
#                                       nationality varchar(15),
#                                       reg_date date,
#                                       date_of_birth date,
#                                       gender varchar(8))''')

def admin():
    username=st.sidebar.text_input('Username',key='user')
    password=st.sidebar.text_input('Password',type='password',key='pass')
    st.session_state.login=st.sidebar.checkbox('Login')
 
    if st.session_state.login==True:
        if username.split('@')[-1] == "gmail.com" and password == "admin@123":
            st.sidebar.success('Login Success')

            date1=st.date_input('Date1')
            date2=st.date_input('Date2')
            cursor.execute(f"select * from information where reg_date between '{date1}' and '{date2}'")
            # db.commit()
            tables =cursor.fetchall()
            # st.write(tables)
            for i in tables:
                st.write(f'studentname---------{i[1]}')
                st.write(f'gpa--------{i[8]}')
                st.write(f'gender------{i[-2]}')
                Accept=st.button('Accept',key=i[0])
                if Accept:
                    st.write('Accepted')
                    cursor.execute(f"Update information set status='Accepted' where id='{i[0]}'")
                    db.commit()
                Reject=st.button('Reject',key=i[0])
                if Reject:
                    st.write('Rejected')
                    cursor.execute(f"Update information set status='Rejected' where id='{i[0]}'")
                    db.commit()

        else:
            st.sidebar.warning('Wrong Credintials')


def form():
    uid=uuid1()
    uid=str(id)[:20]
    with st.form(key='member form'):
        student_name = st.text_input("Name")
        fathers_name = st.text_input("Father's Name")
        mothers_name = st.text_input("Mother's Name")
        present_address = st.text_area("Present Address")
        permanent_address = st.text_area("Permanent Address")
        email = st.text_input("E-mail")
        mobile = st.text_input('Mobile')
        gpa = st.text_input("GPA")
        religion = st.selectbox("Religion",('--Select Religion--','Islam','Hindu','Cristian'))
        nationality = st.text_input("Nationality")
        reg_date = st.date_input("Registration Date")
        date_of_birth = st.date_input("Bith Date")
        gender = st.radio('Gender', ('Male', 'Female'))
        if st.form_submit_button('Submit'):
            x = uuid1()
            x = str(x)[:20]
            col1,col2 = st.columns((4,3))
            col1.warning("Please Store your ID!!")
            col1.info("Your ID is : ")
            col1.code(x)

            query = f'''INSERT INTO information (id ,student_name,fathers_name,mothers_name,present_address,permanent_address,contact_no,email,gpa, 
                                            religion,nationality,reg_date,date_of_birth,gender) 
                                    VALUES ( '{x}', '{student_name}', '{fathers_name}', '{mothers_name}', '{present_address}', '{permanent_address}','{mobile}', '{email}', '{gpa}', '{religion}', '{nationality}' ,'{reg_date}' ,'{date_of_birth}', '{gender}')'''
            cursor.execute(query)
            db.commit()
            st.success(f'{student_name} info inserted successfully')
            st.warning("Please Store this code!!!")
        
def info():
    id=st.text_input('Your Code')
    Submit=st.button(label='Search')
    if Submit:
    	cursor.execute(f"select * from information where id='{id}'")
    	tables = cursor.fetchall()
    	st.write(tables)

def stat():
    id=st.text_input('Your Id')
    submit=st.button('Search',key='sub')
    if submit:
        cursor.execute(f"Select status from information where id='{id}'")
        table=cursor.fetchall()
        for i in table:
            st.success(f'Your status is {i[0]}')

def main():
    st.title('Diploma in Data Science Admission')
    selected=st.sidebar.selectbox('Select',
                        ('-----------',
                        'Admin',
                        'Student Registration',
                        'Student Information',
                        'Show Status'
                        ))
    if selected=='Admin':
        admin()
    elif selected=='Student Registration':
        form()
    elif selected=='Student Information':
        info()
    elif selected=='Show Status':
        stat()
if __name__=='__main__':
    main()
