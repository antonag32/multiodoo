

def post_init(env):
    env["ir.attachment"].sudo().force_storage()
