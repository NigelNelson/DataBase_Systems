'''
Aparna Joshi
10/04/2021
'''

# install mysql-connector-python for version your specific mysql version
# you may use pip install or go to settings -> python interpreter -> install package
# you will able to choose version when you say 'install package'

import mysql.connector
import numpy
connect = mysql.connector.connect(host="localhost",  user="root",  password="root", database="world_db")
cursor = connect.cursor()

try:
    cursor.execute("select c.name,group_concat(cl.language) from country c inner join countryLanguage cl"
                   " on c.code = cl.countryCode group by c.name")
    for c in cursor:
        print('county name : ',c[0],'---- Languages : ',c[1])

except:
    print("error in sql")