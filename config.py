import yaml

bot_token = ""
webhook_url_full = ""
webhook_url = ""
admins = {1234567890}
admins_usernames = "@idk"
rules = ""
dbname = ""
allowed_chats = {1234567890}
host = ""
port = 443
user_blacklist = {1234567890}
report_admin_userid = 1234567890
url_allowlist = {"example.com"}
report_bot_id = 1234567890
channel_id = -10012345678
advert_text = "nodef"
bot_path = "/home/sigma"
suda_admins_text = "nodef"
about_bot_text = "nodef"

with open("config.yml", "r") as file:
    data = yaml.safe_load(file)
    bot_token = data["main"]["bot_token"]
    webhook_url_full = data["main"]["webhook_url_full"]
    webhook_url = data["main"]["webhook_url"]
    host = data["main"]["host"]
    admins = data["main"]["admins"]
    admins_usernames = data["misc"]["admins_usernames"]
    rules = data["main"]["rules"]
    dbname = data["sqlite_adapter"]["dbname"]
    allowed_chats = data["main"]["allowed_chats"]
    port = data["main"]["port"]
    user_blacklist = data["main"]["blacklist"]
    report_admin_userid = data["report"]["admin_userid"]
    url_allowlist = data["url_filter"]["allowlist"]
    report_bot_id = data["report"]["bot_id"]
    channel_id = data["misc"]["channel_id"]
    advert_text = data["misc"]["advert"]
    bot_path = data["main"]["bot_path"]
    suda_admins_text = data["main"]["suda_admins"]
    about_bot_text = data["main"]["about_bot"]