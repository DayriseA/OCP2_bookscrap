# Bookscrap

> ### ***Disclaimer :***
>
> *This project, including what is included in this README, is a school project responding to a fictional scenario and has no other purpose.*  

A little program, still in beta version, designed by and for *Books Online* to track book prices at [Books to Scrape](http://books.toscrape.com/), an online book reseller. It also retrieves some other important information (title, description, upc, etc.). The information is saved locally in csv format and the cover images are also retrieved.  
In this beta version, the program runs on demand and retrieves data at runtime; it does not perform real-time monitoring.

## Installation

This Python program just needs `requests` and `BeautifulSoup`. Install latest versions using requirements.txt file: 

```bash
pip install -r requirements.txt
```
FYI, at the time of writing this we use `requests==2.28.2` and `beautifulsoup4==4.12.0`  
Developed and tested under Python 3.11.2

## Usage

Plain and simple: just use Python to execute main.py from your terminal as usual.
```bash
python ./main.py
```
Datas will be collected and stored as **csv** files in a local folder named ***scrapped_datas***. They are named using the category name and the date of when the file is created.  
  
  Images are stored in folders named by categories that are themselves in the subfolder ***./scrapped_datas/images/***.  
  They are named based on the title of corresponding book.