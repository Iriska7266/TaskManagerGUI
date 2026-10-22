# Task Manager (Flet version)

To run the program you need installed PostgreSQL and all requirements from `requirements.txt`.

---

## Preparations

### DB initialization

You can skip 1st and 2nd steps if you have alredy added postgres to `%PATH%`.
1. Go to PostgreSQL\bin folder. Copy path.
2. Open terminal (win+R -> cmd) and paste copied path into `cd copied_path`. Run this command.
3. Run `psql -U -user_name -d tasks_system_db < path_to_db_dump.sql`. db_dump.sql is located in database folder, enter your DB name after `-U` (default - postgres).
4. Created database already contains test data with 1 user and 2 tasks. Test account login and password: `Test` `Test`.

---
### Dotenv preparing

When the program is run at the first time, it suggests to set up database connection parameters.
Fill all the presented fields correctly.
The program will create .env file in your `%APPDATA%` directory, and you can use the program.

You can edit these parameters in any time on the same configuration page from the authentification page.
But restart of the programm may be required.

---

#### Why is restart required?

When you start the program, connecion with database isn't set immediately, it will be set when you enter into you account.
From this point Python interpreter reads `.env` and session maker, which will be used through the all program's lifecycle, is created.
That's why the main task page opens longer after the first login in this session.
So, you need to restart the program to re-read the `.env` file.

---
### Final step
Install all requirements from `requirements.txt`.
That's all, now you can run main.py file and use the program.

Database also includes actions_log table, which stores history of all data manipulations, it can't be seen from task manager, but if you want, you can observe it in your DBMS.

---
## Project structure
    |-backend
    |--constraints.py
    |--controller.py
    |--domain_models.py
    |--dto.py # data transfer object classes
    |--settings.py
    |-database
    |--db.py # connection and session factory
    |--orm.py
    |--repository # db repository classes (db helpers)
    |-GUI
    |--auth_page.py
    |--dotenv_set_page.py
    |--gui_configuration.py
    |--tasks_page.py
    |--utils.py # common graphical functions
    |-src
    |--assets
    |---icon.png
    |-main.py <-- start the program from here
### Routes
- `/` - authorisation page
- `/db_conf` - db config (.env settings)
- `/tasks` - tasks page