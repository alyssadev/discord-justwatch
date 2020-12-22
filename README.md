discord-justwatch
=================

a simple web service that serves responses to a slash command to retrieve data from JustWatch

![example](https://media.discordapp.net/attachments/755749108458979328/790901910659268618/unknown.png)

Usage
-----

* Write your application's bot token to a file named .bottoken. Discord says you can use an oauth bearer token but idk how that works.
* Set environment variables as below:
  * `JWBOT_PUBKEY`: the public key from your application's info page
  * `JWBOT_CLIENT_ID`: the client ID from the same place
  * `JWBOT_TARGET_GUILD`: the guild ID where you want to use this command
* Install requirements, `pip install -r requirements.txt`
* `python3 register.py`, it should print some json that doesn't have any errors idk
* `python3 jw.py` starts a web service on localhost:8001, forward that through your web server's proxy thing or something
* Add the url to the service to Interactions Endpoint URL on your application's info page
