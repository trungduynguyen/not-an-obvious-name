# README.md


How to validate the code
======================================

- Check the 'data' folder: 
	- If exists daily_data.csv then the program succeeded downloading and storing bitcoin prices via Alpha vantage API
- Check the 'db' folder: 
	- open sqlite cmd (required installing sqlite3) and type following commands: If the query returns values, then the daily data is stored
	```
	.open crypto.db #open database

	select * from bitcoin limit 10;

	```
- Compute the average price of each week (only on business day from MON to FRI): 
	- Check the 'pandas_weekly_report.csv' for the in memory python method
	- Check the 'sql_weekly_report.csv' for the database using query
Note that: the 2 csv files must have the same values to consider the task is correct

- Compute what is the week that had the greatest relative span on closing prices:
	- We have the two results which come from calculation in pandas dataframe and SQL query. The 2 results printed on the console must have the same week of the year and relative span value to be considered as the correct results



How to run
======================================

There are 2 ways to run the code:

- Run on Python IDE
- Run on Docker container

## 1 . Run on Python IDE (eg: Pycharm)

- Clone the repo following the link: https://github.com/trungduynguyen/not-an-obvious-name.git

```
git clone https://github.com/trungduynguyen/not-an-obvious-name.git
```

- Get into the working directory and run the script
```
python ./bitcoin_price.py
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
docker run bitcoin-price
```

- For validating the result, you have to run these commands to get result from container. Copy csv and database files from container to host:
```
docker cp {CONTAINER ID}:/data data
docker cp {CONTAINER ID}:/db db
```