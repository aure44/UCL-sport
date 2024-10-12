# Requirements :

- Python3 : any recent version
- Selenium : any recent version (use 'pip install selenium')
- firefox + geckodriver (see installation of geckodriver on the internet)

Then, execute the code from a shell this way

```
python3 main.py username password sport day/month hour:min-hour:min
```

> e.g. python3 main.py artglenzin 12345678 Escalade 08/05 20:30-22:30

> [!NOTE]
> There is an optional argument which is -head or --headless to make it run in background i.e. no firefox window will open. If you run this code without -head on a virtual machine/server with no GUI, you will have an error because no window can be opened (because no GUI (graphical user interface)).

> e.g. python3 main.py artglenzin 12345678 Escalade 08/05 20:30-22:30 -head

# How does it work :

A webbrowser driver (like geckodriver for firefox) allows python (via selenium) to control a browser. In this case, it has been hard-coded to navigate UCLouvain sport website to log in, change the date, search the sport and finally register to the right sport activity.

If the date is past 7 days in the future (can't register), it will wait for the precise moment at which registration opens.

If the sport session is full, it will check every second if one place has been freed, in which case, it would register itself to it.

Else, it will register to the session without trouble.

# Troubleshooting :

If you want to use chrome, you can download 'chromedriver' and the code needs to be changed this way :

```
line 6 : from selenium.webdriver.**chrome**.options import Options
```
```
line 7 : from selenium.webdriver.**chrome**.service import Service
```

If your driver is not found, you might need to decomment and change line 36 to give the path to the driver. This step is actually necessary for linux machine I believe.

> [!NOTE]
> Same apply to every driver you would want to use. Further tweaking might be required though.


# Motivation :

The motivation to write such a code arose from the frustration of not being able to register to certain sport session like climbing, for which, being awake every midnight one week earlier was mandatory to have acces to said sport.

I hope that UCLouvain will free more vacant spots in a near future.
