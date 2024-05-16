{
    "name": "Multi Odoo",
    "author": "Vauxoo",
    "summary": "Enable the parallelization of this instance",
    "version": "17.0.0.1.0",
    "category": "Technical",
    "depends": ["base"],
    "external_dependencies": {"python": ["redis", "hiredis"]},
    "license": "LGPL-3",
    "auto_install": True,
    "post_init_hook": "post_init",
}
