from github_api import get_workflow_runs
from datetime import datetime, timedelta
import os
import argparse
import json

OWNER = 'ministryofjustice'


# Read ACCESS_TOKEN from environment
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']

# set up the command-line argument parser
parser = argparse.ArgumentParser()
parser.add_argument('filename', help='path to the input JSON file')
parser.add_argument('date_query', help='date range in the format 2023-04-01..2023-05-01')
args = parser.parse_args()

# load the repository names from a JSON file
with open(args.filename, 'r') as f:
    repos = json.load(f)['repos']

filename, file_extension = os.path.splitext(args.filename)
# Initialize variables
total_workflow_runs = 0
total_unsuccessful_runs = 0
runs = []
per_page = 100
for repo in repos:
# Define the query parameters to retrieve all workflow runs
    params = {"branch": "main", "status": "completed", "per_page": per_page, "created": args.date_query}

    # Retrieve the workflow runs for the given repository using the provided query parameters
    workflow_runs = get_workflow_runs(OWNER, repo, ACCESS_TOKEN, params)
    total_workflow_runs += len(workflow_runs)
    total_unsuccessful_runs += len([run for run in workflow_runs if run['conclusion'] != 'success'])


# Calculate the percentage of unsuccessful runs
failure_rate = (total_unsuccessful_runs / total_workflow_runs) * 100

# Output the Change Failure Rate
print(f'Total Workflow Runs: {total_workflow_runs}')
print(f'Total Unsuccessful Runs: {total_unsuccessful_runs}')
print(f"\033[32m\033[1mChange Failure Rate for {filename}: {failure_rate:.2f}%\033[0m")
