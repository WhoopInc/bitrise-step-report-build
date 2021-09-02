import os
import requests
import re
import sys

print("Executing send.py")
message = os.environ.get('message')
branch = os.environ.get('branch')
repository = os.environ.get('repository')
build_num = os.environ.get('build_num')
commit_sha = os.environ.get('commit_sha')
status = os.environ.get('status')
started_at = os.environ.get('started_at')
completed_at = os.environ.get('completed_at')
total_duration_milliseconds = os.environ.get('total_duration')
build_url = os.environ.get('build_url')
github_username = os.environ.get('github_username')
url = os.environ.get('url')
auth_token = os.environ.get('auth_token')

print("Extracting jira ticket")
jira_ticket_pattern = "[a-zA-Z]{1,}-\d{1,}"
ticket = None
branch_match = re.search(jira_ticket_pattern, branch)
message_match = re.search(jira_ticket_pattern, str(message))
if branch_match is not None:
    ticket=branch_match.group(0)
elif message_match is not None:
    ticket=message_match.group(0)
if ticket is not None:
    ticket=ticket.upper()

payload = {
    "repository": repository,
    "branch": branch,
    "build_num": build_num,
    "commit_sha": commit_sha,
    "status": status,
    "started_at": started_at,
    "completed_at": completed_at,
    "total_duration_milliseconds": total_duration_milliseconds,
    "jira_ticket": ticket,
    "build_url": build_url,
    "github_username": github_username
}
print('Payload: {}'.format(payload))

print('Sending payload to {}'.format(url))
request_headers = {'Authorization': auth_token}
r = requests.post(url, json=payload, headers=request_headers)

if r.status_code != 200:
    print('Unable to send build info to {}'.format(url))
    print('Response: {}'.format(r.text))
    sys.exit(1)
else:
    print("Build successfully sent!")
    sys.exit(0)