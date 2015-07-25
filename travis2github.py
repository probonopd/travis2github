import urllib, json, requests
import os, sys
import magic # sudo pip install python-magic
import re

__author__ = 'probonopd'
release_name = "travis"

git_config = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".git/config")
print git_config
config = open(git_config).read()
print(config)
gits = re.findall("https.*.git", config)[0].split("/")
username = gits[3]
repo = gits[4].replace(".git", "")

if os.environ.get('GITHUB_TOKEN')== None:
    print("GitHub token needs to be set in Travis CI Repository Settings")
    exit(1)
else:
    token = os.environ.get('GITHUB_TOKEN')

mime = magic.Magic(mime=True)

url = 'https://api.github.com/repos/' + username + '/' + repo + '/releases'
print url

#
# TODO: MAKE A RELEASE AND DELETE THE PREVIOUS ONE INSTEAD OF HARDCODING ONE
# IF ONE THAT MATCHES THE CURRENT SOURCE IS NOT HERE
# THIS WAY THE SOURCE WILL MATCH TO THE BINARY...
#

# Get the release with the release_name
headers = {'Authorization': 'token ' + token}
response = requests.get(url, headers=headers)
data = json.loads(response.content)

release = None
for candidate in data:
    if candidate['tag_name'] == release_name:
        release = candidate

if (release == None):
    print("No release with name " + release_name + " found, exiting")
    exit(1)

# Delete all binary assets of that release with the corresponding filename
for asset in release["assets"]:
    for arg in sys.argv[1:]:
        filename = arg
        if(asset["name"] == os.path.basename(filename)):
            print("Deleting asset " + str(asset["id"]) + " ...")
            headers = {'Authorization': 'token ' + token}
            url = asset["url"]
            response = requests.delete(url, headers=headers)
            print response


for arg in sys.argv[1:]:
    filename = arg
    content_type = mime.from_file(filename)
    # Upload binary asset
    print("Uploading " + os.path.basename(filename) + "...")
    url = "https://uploads.github.com/repos/" + username + "/" + repo + "/releases/" + str(release["id"]) + "/assets?name=" + os.path.basename(filename)
    headers = {'Authorization': 'token ' + token,
               'Content-Type': content_type}
    data = open(filename, 'rb').read()
    response = requests.post(url, data=data, headers=headers, verify=False)
    print response
    data = json.loads(response.content)
    print data["browser_download_url"]
