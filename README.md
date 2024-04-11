# multiodoo
This repository contains code which makes Odoo instances ephemeral, this makes it possible to create and destroy
multiple instances at will without any loss of data, enabling Odoo to be parallelized.

## How it works
MultiOdoo works by making each Odoo instance stateless. In normal deployments this is impossible since
Odoo stores sessions and attachments on a local filestore. If the instance goes down, the filestore goes with it and
so does the data.

MultiOdoo solves this by storing all data in specialized storage engines. Redis is used to store sessions while
PostgreSQL stores attachments.

## Try it out
A `compose.yaml` file is included, just run `docker compose up`. This will create the following services:

* Caddy server. Works as a reverse proxy and provides HTTPs.
* Redis server. Sessions are stored here. An administrative interface is also provided on port `8001`.
* PostgreSQL server. All other data, including attachments will be stored here.
* Bootstrap server. This service initializes the database before parallel instances are run. 
* Odoo servers. Three odoo servers are run in parallel. These servers are the one fulfilling users' requests. 
  You should see logs from all three servers, indicating the load is being distributed among them.

Odoo will be available on https://localhost:8443. To avoid getting HTTPS certificate warnings consider
setting up Caddy's CA on your computer.

## Chaos Monkey
In order to test the resilience of such a setup a Chaos Monkey is available. This monkey will randomly
kill/start Odoo containers. This simulates system failures. By default, the monkey will leave at least one
Odoo instance alive. You can modify the wait time between each one of the monkey's action with
`--min-wait` and `--max-wait`.

To run the chaos monkey with its default behaviour simply execute the following command:

```shell
./chaos-monkey
```
