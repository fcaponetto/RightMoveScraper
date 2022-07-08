## RightMoveScraper

[rightmove.co.uk](https://www.rightmove.co.uk/) is one of the UK's largest property listings websites, hosting thousands of listings of properties for sale and to rent.

This _python script_ scrapes property listings form [rightmove.co.uk](https://www.rightmove.co.uk/) website. It aslso sends a **notification** through *Telegram* at new ads added that respect the search criteria.

[Telegram Bot](https://core.telegram.org/bots) is used.

### How to create a Telegram Bot
1. Create your own bot by followig [these instructions](https://core.telegram.org/bots#6-botfather)
2. Save the generated **token**
3. Get the list of updates for your bot by going to ` https://api.telegram.org/bot<YourBOTToken>/getUpdates`
4. Send a message to your bot (any)
5. Look for `"id"` and that would be your **chatid**

In case you would add the bot to a group (public or private), [here the istructions](https://stackoverflow.com/questions/32423837/telegram-bot-how-to-get-a-group-chat-id)

### Requirements to use the scraper

I strongly suggest to use a virtual evironment, eg. [miniconda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/download.html#)

* `python 3.x`
* `requestes` -  `python -m pip requests`
* `Beautiful Soap` - `python -m pip bs4`

Why `python -m pip ...`? Here a meaningful explanation [Why you should use `python -m pip`](https://snarky.ca/why-you-should-use-python-m-pip/)?

### How to run the scraper

Activate the evironment (if you have created it), then:
```
python rightmove.py --url ... --addtoken ... --addchatid ...
```
* `--url` is the url of your search
* `--addtoken` is the token of the bot
* `--addchatid` is the id of the chat to send the notification
