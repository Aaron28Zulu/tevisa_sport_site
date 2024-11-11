# TEVISA SPORT SITE
# *__Prerequisites__*
- PostgreSQL installed 
- Access to the terminal (Linux/macOS)
- Sufficient permissions to access and modify the database

*** 
## ***STEP 1: Prepare the Environment***
Ensure necessary permissions are given to access the PostgreSQL server.
1. **Log in to PostgreSQL**
    ```bash
   psql -U postgres -d your_database
    ```
   
2. Create a new database (SQL)
    ```sql
    CREATE DATABASE 
   tevisa;
   ```
## ***STEP 2: Import the Database***
To import the database, use the psql command with the flag -f, specifing the path to the tevisa.sql file. The command with execute all SQL commands in the file, recreating the database schema and data
   ```shell
psql -U postgres -d tevisa -f /path/to/tevisa.sql
```

You'll have to modify the database connection password in the `utils/database_connection.py` file to the password set for the database in your working environment. Current password: `admin@123`
