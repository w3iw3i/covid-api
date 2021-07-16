# Covid-API

A simple API that is build using FastAPI, Postgres database and Docker technologies to deliver Covid timeseries and daily new count data. The data is based on the COVID-19 Data Repository by the Center for Systems Science and Engineering (CSSE) at Johns Hopkins University which can be found [here](https://github.com/CSSEGISandData/COVID-19) 

## Getting Started

Clone the repo and ensure that the project is setup correctly. To get started with this project, you would need to have downloaded and installed Docker. Refer to [Docker's Getting Started Page](https://docs.docker.com/get-started/) for more details.  

To setup the dataset, navigate to the data folder and run "python load.py". This will run a data processing script and output a master.csv and a country.csv file in the data folder 

For privacy reasons, the passwords and usernames in certain areas have been filled with placeholder values. Please fill in the data in .envtocustomise and rename the file to ".env"

## Building

Once Docker has been setup, navigate to the project dicrectory in terminal/command prompt and run the following command:

```
docker compose up
```

This creates a docker network containing the database which loads the master and country dataset data, and the API for you to query from. You can then navigate to localhost:8000 or 127.0.0.1:8000 to access the API. For the list of APIs available, you can get it from localhost:8000/docs or 127.0.0.1:8000/docs.

When you want to delete the network and its containers, you can run the command below:

```
docker compose down
```

You can also run it with the -v flag to remove the volume which helps persist the database info. 
If you want to remove the images as well, you can run:

```
docker compose down --rmi all
```

If you wish to run the API in live debug mode to see your changes in real-time, you can use the debug version of the docker compose file. This can be done by running:

```
docker compose -f docker-compose.debug.yml up
```


## Testing

A separate pipeline is setup for testing by using the docker-compose.test.yml file instead. Run the following command for testing:

```
docker compose -f docker-compose.test.yml up
```

## Load Testing

The load test is performed using locust, which can either be run locally or within a separate docker container in the same network. For the former, you have to run "pip install locust" to setup locust on your local machine. Then, you can "docker-compose up" and run the locust command once your app container is up. To test with locust, navigate to the folder where locustfile.py is located and run:

```
locust -f locustfile.py
```

Then go to localhost:8089 to interact with the locust web interface. For the latter option, you can just run the following command and head to localhost:8089:

```
docker-compose -f docker-compose.loadtest.yml up
```