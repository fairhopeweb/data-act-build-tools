import sys
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import json
from run-databricks-jobs import getJobIds, getRequest


INSTANCE_ID = sys.argv[1]
JOB_NAME = sys.argv[2]
BRANCH = sys.argv[3]
JOB_PARAMETERS = sys.argv[4]
ENV = sys.argv[5]
FILE_LOCATION = sys.argv[6]


def updateJsonFile(fileName):
    # Open the JSON file for reading
    jsonFile = open(fileName, "r") 
    data = json.load(jsonFile) 
    jsonFile.close()

    # Edit content
    # Set notebook params for job
    python_params = JOB_PARAMETERS.split("\n")
    env_vars = {
        "DATABASE_URL": "{{secrets/" + ENV + "/DATABASE_URL}}",
        "BRANCH": BRANCH,
        "ENV_CODE": ENV 
    }
    data["tasks"][0]["spark_python_task"]["python_file"] = "dbfs:/FileStore/" + BRANCH + "/manage.py"
    data["tasks"][0]["spark_python_task"]["parameters"] = python_params
    data["tasks"][0]["new_cluster"]["spark_env_vars"] = env_vars
    data["name"] = JOB_NAME

    ## Save our changes to JSON file
    jsonFile = open(fileName, "w+")
    jsonFile.write(json.dumps(data))
    jsonFile.close()


# Start script
jobs = getJobIds(getRequest("/jobs/list"))

if( JOB_NAME in jobs ):
    sys.stdout.write( (str(jobs[JOB_NAME])) )

    updateJsonFile(FILE_LOCATION)




