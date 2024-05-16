FROM odoo:17

COPY . /mnt/extra-addons
RUN python3 -m pip install -r /mnt/extra-addons/requirements.txt
