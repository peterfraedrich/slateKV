# SlateKV
*SlateKV is a key:value store that (for now) runs on MongoDB. Its sorta like `etcd` in that you can access it via HTTP and it uses JSON for everything.*

### Why do I need this?
You probably don't, but if you did, I could imagine you using it for something like sharing confguration between scripts / servers / etc., using it in place of `etcd` for service discovery and whatnot, storing clustering information, or whatever you would need a key/value store for.

### SlateKV has 3 parts:
* slated -- *the HTTP front-end for MongoDB that takes care of all the work*
* slatectl -- *a CLI client used for interacting with slated*
* slatelib -- *a python library that allows you to use SlateKV in your scripts*
