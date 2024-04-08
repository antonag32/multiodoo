FROM odoo:17

COPY requirements.txt tmp/requirements.txt
RUN python3 -m pip install -r tmp/requirements.txt
