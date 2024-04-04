# multiodoo
This module patches Odoo to:

* Use Redis as session storage
* Store attachments on the database

It must be loaded as a server wide module. The Redis server's URL must also
be specified either through configuration (`redis_url`) or the environment variable `ODOO_REDIS_URL`.
