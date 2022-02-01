import os
import requests
import re
import sys
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

status_map = {
    '0': "SUCCESSFUL",
    '1': "FAILED",
    '2': "PENDING"
}

print("Executing send.py")
message = os.environ.get('message')
branch = os.environ.get('branch')
repository = os.environ.get('repository')
build_num = os.environ.get('build_num')
commit_sha = os.environ.get('commit_sha')
status = status_map[os.environ.get('status')]
started_at = os.environ.get('started_at')
completed_at = os.environ.get('completed_at')
total_duration_milliseconds = os.environ.get('total_duration')
build_url = os.environ.get('build_url')
github_username = os.environ.get('github_username')
url = os.environ.get('url')
auth_token = os.environ.get('auth_token')
lifecycle = os.environ.get('lifecycle')
variant = os.environ.get('variant')
version_code = os.environ.get('version_code')
version_name = os.environ.get('version_name')
artifact_s3_url = os.environ.get('artifact_s3_url')

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
if github_username == '':
    github_username = None
if total_duration_milliseconds == '':
    total_duration_milliseconds = None
if completed_at == '':
    completed_at = None
if variant == '':
    variant = None
if version_code == '':
    version_code = None
if version_name == '':
    version_name = None
if artifact_s3_url == '':
    artifact_s3_url = None

if lifecycle == 'START':
    payload = {
        "repository": repository,
        "branch": branch,
        "build_num": build_num,
        "commit_sha": commit_sha,
        "status": status,
        "started_at": started_at,
        "jira_ticket": ticket,
        "build_url": build_url,
        "github_username": github_username,
        "variant": variant
    }
else:
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
        "github_username": github_username,
        "variant": variant,
        "version_code": version_code,
        "version_name": version_name,
        "artifact_s3_url": artifact_s3_url
    }
print('Payload: {}'.format(payload))

print('Sending payload to {}'.format(url))
retry_strategy = Retry(
    total=3,
    status_forcelist=[429, 502, 503, 504],
    method_whitelist=["POST", "PUT"],
    raise_on_status=True,
    backoff_factor= 10
)
adapter = HTTPAdapter(max_retries=retry_strategy)
http = requests.Session()
http.mount("https://", adapter)
request_headers = {'Authorization': auth_token}
r = http.post(url, json=payload, headers=request_headers)

if r.status_code != 200:
    print('Unable to send build info to {}'.format(url))
    print('Response: {}'.format(r.text))
    sys.exit(1)
else:
    print("Build successfully sent!")
    sys.exit(0)