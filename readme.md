First you need to create the virtualenv

virtualenv --python=/usr/bin/python3 venv
** Make sure you're running >=python3.8 **

After this you need to load the virtualenv -> source venv/bin/activate
And install all requirements needed -> pip3 install -r requirements.txt

Configure your interpreter to use this new virtualenv

Download geckodriver for firefox from https://github.com/mozilla/geckodriver/releases 
Place download in /usr/local/bin/ (make sure /usr/local/bin is in your PATH [check it through ´echo $PATH´ in a console])

For running with chrome you'll need to install chromium -> ´brew install --cask eloston-chromium´. This will download chromium version 96 
For downloading the chromedriver that you need for running chrome head to -> https://chromedriver.storage.googleapis.com/index.html?path=96.0.4664.45/
chromedriver 96 goes along with chromium 96 version. Otherwise it'll crash

HELPERS
For checking xpath in browser use $x(<expression>)
For checking css selector in browser use $$(<expresion>)
Firefox v66 on https://ftp.mozilla.org/pub/firefox/releases/66.0.3/mac/es-AR/


Installing MySQL
In MacOS:
    `brew install mysql` -- install driver
    `brew services start mysql` -- start mysql service
    `mysql_secure_installation` -- start service, passwords, users

For checking HTTPRequest after posting a comment refer to
https://stackoverflow.com/questions/27644615/getting-chrome-performance-and-tracing-logs/27644635#27644635
