# tripit-co2

Technically this repo is just a fork of tripit's Python bindings with
my scripts added, because I ran into some bugs in their code at earlier
stages. But in the end none of the bugs really got in my way.

Since the library is obscure and not exactly apt-gettable, I decided to
just stick to this format anyway.

Anyway, brief instructions:

```shell
./login.sh
./co2.py ##LOGIN_ARGUMENTS##
./fix_co2.py
```

`login.sh` helps you with getting OAuth credentials. `co2.sh` will
download all your flight data and dump it into a file named `co2.csv`.
This is a very raw dump, it's not even sorted. Lots of info is barely
parsed. Likely it'll contain some of your contacts' trips as well (even
though the script isn't requesting them). See the source code, there's a
commented out check to filter those out.

Pay attention in particular to parsing of flight class data, I've added
some heuristics to convert BA terminology to standard terms (and the
class descriptions used by goclimateneutral), you may want to add some
extra rules if your flights are with a different airline.

For `fix_co2.py`, you'll need to request an API key at
https://api.goclimateneutral.org/api_keys and add it to the script. I'd
include my API keys (as I've done for the TripIt scripts) but the
request form specifically had me tick a checkbox promising to keep the
API keys for myself.

When that's run, it will convert `co2.csv` into `co2-fixed.csv` with
hopefully more accurate CO₂ emission numbers. (You'll find that it
creates a `co2-cache.db` to cache all API responses since likely you'll
be doing a lot of the same flights.)

Up to you to then do the maths and figure out where to buy your offsets.
I've bought some from goclimateneutral.org since I appreciate them
offering the API and have used atmosfair.de since I've heard good things
about them. Curious about other people's recommendations as well!
