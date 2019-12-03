
# Harvest with web service
Capstone: Harvest     

## Objective:

- Harvest application to scrape web pages for information and download files

    - The application saves website information into a database and stores the downloaded files to disk
    
- REST API which accepts file submissions.

     - The application extracts metadata from file uploads and allows users to read the metadata, update/correct the metadata and delete submissions.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
Install all dependencies for Harvest and HarvestApi using its own requirements.txt
```
$ cd ./Harvest
$ pip install -r requirements.txt
```
```
$ cd ./HarvestApi
$ pip install -r requirements.txt
```
Install the postgres server, refer to this [link](https://www.postgresql.org/download/) for the tutorial on how to install PostgreSQL

Create the database for HarvestApi by running this sql script either on terminal or on the PGAdmin.
```
CREATE DATABASE harvest_api_db
```
Then run the migrations for the Harvest API
```
$ python migrate.py db init
$ python migrate.py db migrate
$ python migrate.py db upgrade
```
Now you can run the API with on the directory of HarvestApi
```
$ python run.py
```
Then run the Harvest on its director with the url parameter,
```
$ python run.py <url>
```
or simply with
```
$ python run.py
```
## To run in docker
Build all the docker images needed 
 ```
$ docker build -t <harvest_image_name> ./Harvest
$ docker build -t <api_image_name> ./HarvestApi
```
Pull the image of postgres
```
$ docker pull postgres
```
After that, create a network
```
$ docker network create <network_name>
```
Then run the images
```
# container for Postgres
$  docker run --rm --name <container_name> -e POSTGRES_PASSWORD=<password> --network <network>
 -v <volume> <db_image_name>

# container for Harvest
$ docker run --network <network> --name <container_name> <harvest_image_name>

# container for API
$ docker run --network <network> -p <ports> --name <container_name> <api_image_name>
```
The Harvest will start harvesting and it will also going to upload the harvested files to the API.
 
## Author
**Johnzel Tuddao** - *Initial work* - [J0hnZMT](https://github.com/J0hnZMT)

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

