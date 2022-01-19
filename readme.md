
# GENERIC CRAWLER
**The project is intended for educational purposes only and its main idea is being able to crawl different websites for different purposes under the same structure**   
<br>

### Preparing to run the project
#### To start with, we need to create the virtualenv
First of all. Make sure you have virtualenv installed in your computer (for macOS `brew install virtualenv`)
<br> Inside the repository folder run the command `virtualenv --python=/usr/bin/python3 venv` to create the venv folder which will contain all dependencies and binaries we'll use
<br> After this run `source venv/bin/activate` in order to activate venv
<br> Once venv is activated, we'll install all required libraries inside it with `pip3 install -r requirements.txt`
<br> In case installation fails in linux try -> sudo apt-get install python3-dev default-libmysqlclient-dev build-essential
<br> Configure your interpreter to use this new virtualenv. In PyCharm go to Preferences -> Project -> Python Interpreter. Here just configure the binary that should be placed in <project_path>/venv/bin/python (or python3. Make sure you run python >= 3.7)
<br> Download geckodriver for firefox from https://github.com/mozilla/geckodriver/releases 
<br> Place download in `/usr/local/bin/` (make sure `/usr/local/bin` is in your PATH [check it through `echo $PATH` in a console])
<br> For running with chrome you'll need to install chromium via `brew install --cask eloston-chromium`. Check which chromium version gets installed 
<br> Download the chromedriver that corresponds to the chromium version you've just downloaded. If you got chromium v96 then download chromedriver v96 (https://chromedriver.storage.googleapis.com/index.html?path=96.0.4664.45/chromedriver). Otherwise project will just crash
<br> Don't forget to set the proper webdriver binary location in config.yaml->web_driver->chrome_binary/firefox_binary
<br> Create a .env file in root directory. Inside this you'll have to add the following data

> DB_ENGINE=
>
> DB_USER=
>
> DB_PASSWORD=
>
> DB_HOST=localhost
>
> DB_PORT=
>
> DB_SCHEMA=
>
> SPIDER_ID_USERNAME=
>
> SPIDER_ID_PASSWORD=
>
> SPIDER_ID_EMAIL=


### Installing MySQL
#### In MacOS:
>
> `brew install mysql` -- install driver
>
> `brew services start mysql` -- start mysql service
>
> `mysql_secure_installation` -- start service, passwords, users

#### In Linux:
>
> `sudo apt-get update`
>
> `sudo apt-get install mysql-server`
>
> Check mysql service status via `systemctl status mysql`
>
> In case it's stopped run `systemctl start mysql`

After installing MYSQL run the following for configuring database local connection
>
> `sudo mysql_secure_installation` -- for password strength selection use STRONG, after that just set your local database password and everything just hit YES

In case you have problem accessing using the password you have just defined try the following
>
> `sudo mysql`
>
> `alter user 'root'@'localhost' identified with mysql_native_password by 'oneNewPasswordYouJustInvented'';`

Don't forget to complete the connection data into the .env variables we created a few steps before

### Create MySQL corresponding tables
After installing MySQL just copy the tables places in resources/generic_crawler.sql
<br> There, you'll also find the accounts that'll be tagged in draws and an insert example for a draw
<br> Don't forget to complete the spiders_account information for each spider in `.env`. For each spider you'll need to replace the id for the corresponding database id. For example, if database id is 15 your env var will be `SPIDER_15_USERNAME=username`


### HELPERS
#### You might need to run Firefox v66 in case of failures or misbehaving
Firefox v66 on https://ftp.mozilla.org/pub/firefox/releases/66.0.3/
- Mac installation is just straight forward
- For linux installation steps to follow are this:
    - sudo tar xjf ~/FirefoxSetup.tar.bz2 -C /opt/
    - sudo ln -s /opt/firefox/firefox /usr/lib/firefox/firefox

**IN BOTH CASES AUTOMATIC UPDATES NEED TO BE DISABLED**

<p> For checking xpath in browser use $x(expression)
<br> For checking css selector in browser use $$(expresion)
<br> For checking HTTPRequest after posting a comment refer to https://stackoverflow.com/questions/27644615/getting-chrome-performance-and-tracing-logs/27644635#27644635
