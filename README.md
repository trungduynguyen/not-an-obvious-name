# README.md


Structure
======================================

- data folder: stores csv files of daily bitcoin prices and weekly prices from both pandas and sql methods
- db folder: stores sql db file of bitcoin prices collected from Alpha vantage API
- bitcoin_price.py: contains Parent class BitcoinPrice with the main purpose of collecting data from API and some abstract methods
- bitcoin_pandas.py: contains Child class BitcoinPricePandas which inherits from BitcoinPrice class, , computation based on pandas DataFrame approach 
	+ get_weekly_stats()
	+ get_max_relative_span()
	+ process(): run the tasks of the assessment
- bitcoin_db.py: contains Child class BitcoinPriceDB which inherits from BitcoinPrice class, computation based on SQL query approach 
	+ get_weekly_stats()
	+ get_max_relative_span()
	+ process(): run the tasks of the assessment
- main.py: main function running entire program
- query_lib.py: stores SQL query as contants then passes them into BitcoinPriceDB class when a specific query is executed
- test.py: unittest for the tasks, contains 2 test cases
	+ test_weekly_data() : Test if two weekly_data csv files from both pandas and sql are equal
	+ test_max_relative_span(): Test if two maximum weekly relative span values from both pandas and sql are equal


- Table bitcoin:

| **FIELD** | **Type** |
| :---: | :---: |
| date |  DATETIME PRIMARY KEY |
| open | FLOAT |
| high | FLOAT |
| low | FLOAT |
| close | FLOAT |
| volume | FLOAT |
| market_cap | FLOAT |
| year_week | VARCHAR(15) |

How to validate and test the code
======================================

- Check the 'data' folder: 
	- If exists daily_data.csv then the program succeeded downloading and storing bitcoin prices via Alpha vantage API
- Check the 'db' folder: 
	- open sqlite cmd (required installing sqlite3) and type following commands: If the query returns values, then the daily data is stored
	```
	.open crypto.db #open database

	select * from bitcoin limit 10;

	```
- Run unitest by following command on your IDE: Make sure there exist csv files in data folder before running unitest

```
python ./test.py API_KEY  DB_NAME TABLE_NAME

#Where Args: 
# API_KEY: api key obtained from Alpha vantage
# DB_NAME: path to sqlite db files
# TABLE_NAME: name of table to store bitcoin daily prices
#Ex: python ./test.py XXXXXXXXX  ./db/your_dbname.db your_table_name
```



How to run
======================================

There are 2 ways to run the code:

- Run on Python IDE
- Run on Docker container (tested on Docker version 17.12.0-ce, build c97c6d6 for Windows)

## 1 . Run on Python IDE (eg: Pycharm)

- Clone the repo following the link: https://github.com/trungduynguyen/not-an-obvious-name.git

```
git clone https://github.com/trungduynguyen/not-an-obvious-name.git
```

- Get into the working directory and run the script
```
python ./main.py API_KEY  DB_NAME TABLE_NAME

#Where Args: 
# API_KEY: api key obtained from Alpha vantage
# DB_NAME: path to sqlite db files
# TABLE_NAME: name of table to store bitcoin daily prices
#Ex: python ./main.py XXXXXXXXX  ./db/your_dbname.db your_table_name
```

## 2 . Run on Docker container

- Clone the repo following the link: https://github.com/trungduynguyen/not-an-obvious-name.git

```
git clone https://github.com/trungduynguyen/not-an-obvious-name.git
```

- First, make sure that you are at the directory containing the Dockerfile.
- Build Docker image
```
docker build -t bitcoin-price .
```

- Run Docker container and validate the result
```
 docker run --rm bitcoin-price API_KEY  DB_NAME TABLE_NAME
```

- For validating the result, you have to run these commands to get results from container. Copy csv and database files from container to host, then you can check the files:
```
docker cp {CONTAINER ID}:/data ./
docker cp {CONTAINER ID}:/db ./
```