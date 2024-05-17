FROM odoo:17

COPY . /mnt/extra-addons

USER root

RUN python3 -m pip install -r /mnt/extra-addons/requirements.txt

USER odoo
