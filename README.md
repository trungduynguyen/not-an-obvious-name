# README.md



How to validate the code
======================================



How to run
======================================

There are 2 ways to run the code:

- Run on Python IDE
- Run on Docker container

## 1 . Run on Python IDE

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

- Build Docker image
```
docker build -t bitcoin-price .
```

- Run Docker container and validate the result
```
docker run bitcoin-price
```

- Copy csv and database files from container to host
```
docker cp {CONTAINER ID}:/data data
docker cp {CONTAINER ID}:/db db
```