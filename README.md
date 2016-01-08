# SlateKV
*SlateKV is a key:value store that (for now) runs on MongoDB. Its sorta like `etcd` in that you can access it via HTTP and it uses JSON for everything.*

### Why do I need this?
You probably don't, but if you did, I could imagine you using it for something like sharing confguration between scripts / servers / etc., using it in place of `etcd` for service discovery and whatnot, storing clustering information, or whatever you would need a key/value store for.

### Why not redis?
Man, idk. Use redis if you want. Or use SlateKV. I kinda don't care.

### SlateKV has 3 parts:
* `slated` -- *the HTTP front-end for MongoDB that takes care of all the work*
* `slatectl` -- *a CLI client used for interacting with slated*
* `slatelib` -- *a python library that allows you to use SlateKV in your scripts*

#### slated
`slated` is a Flask application (http://flask.pocoo.org/, BSD license, see `LICENSE` for the Flask licesnse). By default it runs on port `:80`, but you can change this by editing the `app.run(host='0.0.0.0', port='80')` line in `slated`, just change `port=80` to whichever port you want to run on.

`slated` has three operations:
* `get` -- fetches a key:value pair and returns JSON
* `post` -- sets a key:value pair based on the request URL, returns the inserted JSON, does nothing if the key already exists
* `change` -- changes an existing key:value pair to the user-supplied values and inserts the pair if it doesn't already exist

When querying `slated`, all information is passed to `slated` via the request URL. Example:
```
http://<someurl>/get/lucy
```
The abole URL tells `slated` to do a lookup for the key **lucy** and return anything it finds. If `lucy` exists in the store the query will return
```
{ "lucy" : "placeholder" }
```
To insert a key:value pair into the store, simply use the `post` method and pass a `key:value` object like this:

```
http://<someurl>/post/schroeder:piano
```
This request will tell `slated` to insert the key:value pair of `mary : 25` into the store if `mary` is not already in the store. This will return the following object:
```
{ "schroeder" : "piano" }
```
If we wanted to update the value for `lucy`, all we need to do is use the `change` method, like so:
```
http://<someurl>/post/lucy:real_estate_agent
```
Which will return the query object in JSON:
```
{ "lucy" : "real_estate_agent" }
```

The `slated.conf` file contains all of the configuration for the `slated` server. To set the location of the MongoDB instance you would like to use, simply put the DB's IP or FQDN in the `db_url` section of the conf. If you are running MongoDB on a non-standard (not `:27017`) port, you can change the port in the config file as well.

**slated requires the following dependencies:**
* `pymongo` -- python mongodb driver
* `flask` -- python WSGI server

### slatectl
`slatectl` is the CLI tool for interacting with `slated`. `slatectl` used the following syntax:
```
slatectl --flag argument
```
Available flags are:
* `--get <key>` -- returns a JSON object if the key exists
* `--post <key:value>` -- adds a new key:value pair to the store
* `--change <key:value>` -- changes the value of an existing key:value pair
* `--set-url <http://<someurl>/>` -- sets the URL of the `slated` server
* `--set-logfile </some/path>` -- sets the path of the logfile, default is no logging
* `--config` -- prints the contents of `slatectl.conf` as JSON

Example:
```
$> slatectl --post linus:shepherd
```
Which will return:
```
$> SUCCESS: { "linus" : "shepherd" }
```

### slatelib.py
`slatelib.py` is the SlateKV Python library which allows developers and operations people to use the SlateKV in their scripts. The library exposes the following methods:
* `Slate.get(query, url)` -- reruns a JSON string of the query results
* `Slate.post(keyvalue, url)` -- returns a JSON string of the key:value submitted
* `Slate.change(key_value, url)` -- -- returns a JSON string of the key:value submitted

To use the library, simply import it:

```
from slatelib.py import Slate
slate = Slate()

print slate.get('lucy', http://<someurl>/)
```
This will print the following string:
```
{ "lucy" : "real_estate_agent" }
```

#### Limitations
Due to not (yet) implementing URI encoding, spaces are not supported in `keys` or `values`.

#### Future Plans
* URI encoding to allow spaces to be put into `values`
* Add function to get a list of existing keys in the KV store
* Create our own database engine to replace MongoDB

#### Open Source
I'm probably a shit programmer that writes sloppy code. If anyone has ideas on how to do things faster/better/stronger feel free to branch and code away.
