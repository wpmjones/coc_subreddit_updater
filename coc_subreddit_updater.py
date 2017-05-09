import sys
import requests
import json
import praw

# COC Variables
clanName = 'Reddit Oak'          # replace with your clan name
clanTag = 'CVCJR89'              # replace with your clan tag

# Reddit Variables
r_client_id = ''                 # enter your Reddit API client ID here
r_client_secret = ''             # enter your Reddit API client secret here
r_username = ''                  # enter your Reddit username here
r_password = ''                  # enter your Reddit password here
reddit = praw.Reddit(client_id=r_client_id,client_secret=r_client_secret,username=r_username,password=r_password,user_agent='python:com.example.coc_' + clanTag + '_updater:v1.0 (by /u/' + r_username + ')')
subreddit = ''                   # enter your subreddit here (e.g. /r/coc_redditoak without the /r/)
settings = reddit.subreddit(subreddit).mod.settings()
content = settings['description']
newcontent = ''

# Pull clan info from COC API
url = 'https://api.clashofclans.com/v1/clans/%25' + clanTag
api_key = ''                     # place your api key from SuperCell here
headers = {'Accept':'application/json','Authorization':'Bearer ' + api_key}
r = requests.get(url, headers=headers)
data = r.json()

# Update war record
start_marker = '[](#RECstart)'   # [](#RECstart) should exist in your sidebar just before your war record
end_marker = '[](#RECend)'       # [](#RECend) should exist in your sidebar just after your war record
newcontent = str(data['warWins']) + '-' + str(data['warLosses']) + '-' + str(data['warTies'])
start = content.index(start_marker)
end = content.index(end_marker)
content = content.replace(content[start:end], '{}{}{}'.format(start_marker, newcontent, end_marker))

# Update member list
start_marker = '[](#MEMstart)'    # [](#MEMstart) should exist in your sidebar just before your member table (two columns)
end_marker = '[](#MEMend)'        # [](#MEMend) should exist in your sidebar just after your member table
newcontent = ''
for members in data['memberList']:
  role = members['role']
  if role == 'admin':
    role = 'elder'
  memname = members['name'].encode('ascii','ignore')    # if you have a member with nothing but non-ascii characters it will show up blank (future improvements may fix this)
  newcontent += '\n' + memname + '|' + role
start = content.index(start_marker)
end = content.index(end_marker)
content = content.replace(content[start:end], '{}{}{}'.format(start_marker, newcontent, end_marker))

# Pull clan info from COC API and Update last war
url = 'https://api.clashofclans.com/v1/clans/%25' + clanTag + '/warlog?limit=1'
r = requests.get(url, headers=headers)
data = r.json()

start_marker = '[](#WARstart)'        # [](#WARstart) should exist in your sidebar just before your war results
end_marker = '[](#WARend)'            # [](#WARend) should exist in your sidebar just after your war results
newcontent = clanName + '(' + str(data['items'][0]['clan']['stars']) + ') vs ' + data['items'][0]['opponent']['name'].encode('ascii','ignore') + '(' + str(data['items'][0]['opponent']['stars']) + ')'
start = content.index(start_marker)
end = content.index(end_marker)
content = content.replace(content[start:end], '{}{}{}'.format(start_marker, newcontent, end_marker))
reddit.subreddit(subreddit).mod.update(description=content)
