#Firebird employee database
#Specify subset of tables and fields 
#to be exported
#NOTE: employee.fdb errors on opening 
#with charset utf-8
'''
Table:  COUNTRY
Fields:  COUNTRY,CURRENCY

Table:  CUSTOMER
Fields:  CUST_NO,CUSTOMER,CONTACT_FIRST,CONTACT_LAST,PHONE_NO,ADDRESS_LINE1,ADDRESS_LINE2,CITY,STATE_PROVINCE,COUNTRY,POSTAL_CODE,ON_HOLD

Table:  DEPARTMENT
Fields:  DEPT_NO,DEPARTMENT,HEAD_DEPT,MNGR_NO,BUDGET,LOCATION,PHONE_NO

Table:  EMPLOYEE
Fields:  EMP_NO,FIRST_NAME,LAST_NAME,PHONE_EXT,HIRE_DATE,DEPT_NO,JOB_CODE,JOB_GRADE,JOB_COUNTRY,SALARY,FULL_NAME

Table:  EMPLOYEE_PROJECT
Fields:  EMP_NO,PROJ_ID

Table:  JOB
Fields:  JOB_CODE,JOB_GRADE,JOB_COUNTRY,JOB_TITLE,MIN_SALARY,MAX_SALARY,JOB_REQUIREMENT,LANGUAGE_REQ

Table:  PHONE_LIST
Fields:  EMP_NO,FIRST_NAME,LAST_NAME,PHONE_EXT,LOCATION,PHONE_NO

Table:  PROJECT
Fields:  PROJ_ID,PROJ_NAME,PROJ_DESC,TEAM_LEADER,PRODUCT

Table:  PROJ_DEPT_BUDGET
Fields:  FISCAL_YEAR,PROJ_ID,DEPT_NO,QUART_HEAD_CNT,PROJECTED_BUDGET

Table:  SALARY_HISTORY
Fields:  EMP_NO,CHANGE_DATE,UPDATER_ID,OLD_SALARY,PERCENT_CHANGE,NEW_SALARY

Table:  SALES
Fields:  PO_NUMBER,CUST_NO,SALES_REP,ORDER_STATUS,ORDER_DATE,SHIP_DATE,DATE_NEEDED,PAID,QTY_ORDERED,TOTAL_VALUE,DISCOUNT,ITEM_TYPE,AGED
'''

STable = ["CUSTOMER", "EMPLOYEE", "PROJECT"]

SFields = { 
    "CUSTOMER": [ "CUST_NO","CUSTOMER","CONTACT_FIRST","CONTACT_LAST" ],
    "EMPLOYEE": [ "EMP_NO", "FIRST_NAME", "LAST_NAME", "FULL_NAME" ],
    "PROJECT" : [ "PROJ_ID", "PROJ_NAME","PROJ_DESC", "TEAM_LEADER" ,"PRODUCT" ]
}