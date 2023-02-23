## Imgur Scraper
Scrape imgur.com images and find secrets that aren't that secret

### Warning
:warning: There is more Porn than you can imagine  
**Also, it may be aggainst the TOS of Imgur Inc., use at own risk!**

### Sample Command
```
python3 main.py --threads=16
```

### Arguments
**`--threads`** will determine how many threads will be started.  
Default value is **8**

**`--directory`** will determine where the images should be stored.  
Default value is **./output/**

**`--minsize`** will determine the minimum size the Image should have
Default value is **100x100**

**`--id-length`** will determine length the Image ID should have
Default value is **6-7**.
You can either put a single number or a range. eg. `6-7`

**`--disallow-ghost`** will determine if unindexed images (imgur tells on some images that they are not in their db and no upload data eg. can be be found)
should be auto. deleted. Default is **False**
