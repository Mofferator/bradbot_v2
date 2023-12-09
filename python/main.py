import mysql.connector

db = mysql.connector.connect(
  host="mysql",
  user="root",
  password=open('/secrets/db_root_password.txt').readline(),
  database='Thermostat_Project'
)

if __name__ == "__main__":
    # Do something :)
    pass