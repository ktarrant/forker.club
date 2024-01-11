# seasonal-food-scraper
Scraper for downloading seasonal food data from the seasonal food guide

# Setup

IMPORTANT NOTE: It seems mezzanine has an issue with the latest Django/python.
This issue showed up when trying to create a model which subclass RichTextPage.
I found the solution at this link:
https://blog.lordvan.com/blog/upgrading-mezzanine-forced-to-due-to-move-to-python310/

The solution is:
After looking it up and checking the source I just edited the relevant mezzanine
file (myenv/lib64/python3.10/site-packages/mezzanine/utils/html.py)
and changed line 113 to this:

       protocols=list(ALLOWED_PROTOCOLS) + ["tel"],

So be aware that this monkey-patch is required.