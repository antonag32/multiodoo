# multiodoo
This repository contains code which makes Odoo instances ephemeral, this makes it possible to create and destroy
multiple instances at will without any loss of data, enabling Odoo to be parallelized.

## How it works
MultiOdoo works by making each Odoo instance stateless. In normal deployments this is impossible since
Odoo stores sessions and attachments on a local filestore. If the instance goes down, the filestore goes with it and
so does the data.

MultiOdoo solves this by storing all data in specialized storage engines. Redis is used to store sessions while
PostgreSQL stores attachments.
