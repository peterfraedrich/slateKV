# SlateKV
*SlateKV is a key:value store that (for now) runs on MongoDB. Its sorta like `etcd` in that you can access it via HTTP and it uses JSON for everything.*

### Why do I need this?
You probably don't, but if you did, I could imagine you using it for something like sharing confguration between scripts / servers / etc., using it in place of `etcd` for service discovery and whatnot, storing clustering information, or whatever you would need a key/value store for.

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
