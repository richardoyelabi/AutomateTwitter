GENERAL HOW-TO
- Type or paste the text(s) you want to post as tweets (hashtags included) inside the tweets.json file. You may also include the file paths of images or videos you want to attach (or even include only images/videos without text, you're the boss here). Just follow the exemplified format (you'll see the format when you open tweets.json); the format is also illustrated in tweets_template.json. (You can validate .json files at https://jsonlint.com/ so you know you're doing the right thing.)

- Regarding file paths, if you put the images and/or videos in the AutomateTwitter folder, you only need to include the names of the files in tweets.json (like I did with "heart.jpg" and "pretty.jpg"). Also, please don't forget the quotes and commas when editing .json files; they're important.

- Type or paste the text you want the bot to automatically reply message requests with inside the dmreply.txt file. There's no format to follow here; just enter the dang message.

- Type or paste login details for three twitter accounts inside credentials.json. I don't mean to sound like a broken record but... Just follow the exemplified format (you'll see the format when you open credentials.json); the format is also illustrated in credentials_template.json. (You can validate .json files at [jsonValidatorSite] so you know you're doing the right thing.)

- main.py is the most important file here. It contains the python code that runs the bot. Run this code to get the bot running. Hiyah!

BACKGROUND INFO AND HOW TO SET IT UP
- The bot controls three browsers (Chrome, Firefox, and Edge) to automate one twitter account each (a total of three accounts).

- The bot can run on Windows, MacOS, and Linux. It just needs the right environment.

- The right environment includes python and three browser drivers, one for each browser.

THE RIGHT ENVIRONMENT
- Download the drivers for your browsers and put them in the AutomateTwitter folder. Their names are chromedriver (for Chrome), geckodriver (for Firefox), and msedgedriver (for Edge). The code relies on these to control the browsers, and they are different for different operating systems.
I have included all three of them for Windows. For Edge however, different versions of browsers have different versions of drivers; so, you'll have to replace the msedgedriver I have included with a new one compatible with your version of Edge.
Follow this link for more information and guidance: https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/

- Install Python. This page is a great guide: https://realpython.com/installing-python/

- Install python dependencies by running the following on your terminal:
    - pip install selenium OR pip3 install selenium
    - pip install pyautogui OR pip3 install pyautogui
Whether pip or pip3 works depends on your version of Python.

You can now run the program: python main.py OR python3 main.py OR py main.py
Which one works depends on your version of python and/or operating system.
