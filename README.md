## RightMoveScraper

[rightmove.co.uk](https://www.rightmove.co.uk/) is one of the UK's largest property listings websites, hosting thousands of listings of properties for sale and rent.

This _python script_ scrapes property listings from [rightmove.co.uk](https://www.rightmove.co.uk/) website. It also sends a **notification** through *Telegram* if new ads added that respects the search criteria.

[Telegram Bot](https://core.telegram.org/bots) is used.

### How to create a Telegram Bot
1. Create your bot by following [these instructions](https://core.telegram.org/bots#6-botfather)
2. Save the generated **token**
3. Get the list of updates for your bot by going to ` https://api.telegram.org/bot<YourBOTToken>/getUpdates`
4. Send a message to your bot (any)
5. Look for `"id"` and that would be your **chatid**

In case you would add the bot to a group (public or private), [here are the instructions](https://stackoverflow.com/questions/32423837/telegram-bot-how-to-get-a-group-chat-id)

### Requirements to use the scraper

I strongly suggest using a virtual environment, eg. [miniconda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/download.html#)

* `python 3.x`
* `requestes` -  `python -m pip requests`
* `Beautiful Soap` - `python -m pip bs4`

Why `python -m pip ...`? Here is a meaningful explanation [Why you should use `python -m pip`](https://snarky.ca/why-you-should-use-python-m-pip/)?

### How to run the scraper

Activate the environment (if you have created it), then:
```
python rightmove.py --url ... --addtoken ... --addchatid ...
```
* `--url` is the URL of your search
* `--addtoken` is the token of the bot
* `--addchatid` is the id of the chat to send the notification

It makes a new request for every random delta between `30 min` to `1 hour`.

### Legal
This project is meant only for educational purposes. Even though this script makes a new request between 30min and 1 hour, scraping a website is a [grey area](https://benbernardblog.com/web-scraping-and-crawling-are-perfectly-legal-right/).
