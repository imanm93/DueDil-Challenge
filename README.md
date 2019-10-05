# DueDil-Challenge
This is the solution to the DueDil take home test

## Requirements

Please install Docker and docker-compose to run the application. See [here](https://docs.docker.com/docker-for-mac/install/) for installation instruction on MAC OS.

Please install `pytest` using the following command to run the automated tests.

`pip3 install pytest`

## Usage

Run the API by doing the following in a terminal from the root folder and wait till everything is set up.

```
docker-compose up --build
``` 

### Step 1: Upload User file to compute matches

To upload a User file to compute matches please make a POST request using Postman or any other utility (such as curl) - specifying the file you want to upload and threshold you want to use.

An example with curl looks like below. The command has to be executed from the directory in which your file exists.

```
curl -v -F threshold=0.5 -F file=@sample_user_records.csv http://127.0.0.1:5000/api/v1/user/records
```

Take note of the `id` returned by the response. You will need this to check the status of your request and download the output.

### Step 2: Check Status/Download result

To check the status or download the result you need to make a GET request with the `id` you recieved from Step 1.

- Open your browser and enter the url: `http://127.0.0.1:5000/api/v1/user/matches/<id>`

If the async process has completed it will download the resulting .csv file. Otherwise it will display the current status of the process.

The different statuses you will see are described below.

| STATUS  | DESCRIPTION  | ADDITIONAL INFO         |
| ------- | ------------ | ----------------------- |
| PENDING | The process is in the queue and has not yet started | |
| STARTED | The process has just started | |
| MATCHING_IN_PROGRESS | The process has started to compute the matches for the user uploaded file | You are also shown the current record it is matching out of the total records provided |
| MATCHING_COMPLETE | The process has completed computing the matches for the user uploaded file | |
| FILE_IN_CREATION | The process has started to create the result | You are also shown the current record it is writing to the file out of the total records to be written |
| SUCCESS | The process has completed and was successful | You will never actually see this state. Instead the file will download on your browser once this state is reached |
| FAILED | The process had some error and exited | |

**NOTE: Without the forceful delay put in during test mode it is unlikely you will be able to view any state other than PENDING and SUCCESS unless you increase the size of your input.csv file or companies.csv file by a significant amount.**

## Run Tests

To run the tests please follow the below steps.

- Please uncomment the lines 15-16 and 27-28 from `docker-compose.yml` and save the file. 
- Open a terminal and run `docker-compose up --build` from the root folder and wait until everything is setup.
- Open another terminal from the root folder and run `pytest`

The tests will take some time to run as an imaginery lag is introduced for testing purposes.
