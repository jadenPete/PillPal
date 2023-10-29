# PillPal
Our HackNC 2023 project: an inventory management system with helpful warnings to prevent misprescription and human error

# Setup / Installation
- Pull repo and cd into pill_pal
- Make sure you have postgres installed, and make note of your username & password. Create a database named "pill_pal".
- Run "flask run" in terminal
- Open home page
  - If an error occurs, you (probably) need to configure the program to utilize your specific postgres username and password
  - To do this, open the root folder and create a file named "config.json"
  - Inside this file create an object with one key and one value as follows
  - {"connectionInfo": "dbname=pill_pal user=your_postgres_username pass=your_postgres_password"}
  - Note: if you do not have a password, leave out the pass= field.
- With the application open and running, you are free to create prescriptions and look up information about specific substances
