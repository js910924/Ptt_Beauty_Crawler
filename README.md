# PTT Beauty Board Crawler - Python
This implementation is for learing crawler and python programming skill.

## Update
### 2020.01.16
> Modify error handling
> Advance input date and article date compare

### 2019.06.18
> Use multithreading to download pictures and made some change to improve efficiency.
> Set default path where BeautyCrawler.py is.

## Instructions
install bs4 & requests before execute Crawler
```shell
pip install bs4
pip install requests
```

### Download today beauty board pictures
```shell
python3 BeautyCrawler.py
```

### Download the specified data on beauty board pictrues
```shell
python3 BeautyCrawler.py 11/5
```