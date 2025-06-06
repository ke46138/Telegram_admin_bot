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
misc_nav_post = "nodef"
misc_thanks_post = "nodef"
group_chatid = 000000
rules_id = 000000
nav_post_id = 00000
thanks_post_id = 00000

def reload():
    global bot_token, webhook_url_full, webhook_url, host, admins, admins_usernames, rules, dbname, allowed_chats, port, user_blacklist, report_admin_userid, \
        url_allowlist, report_bot_id, channel_id, advert_text, bot_path, suda_admins_text, about_bot_text, misc_nav_post, group_chatid, rules_id, nav_post_id, \
        misc_thanks_post, thanks_post_id
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
        misc_nav_post = data["misc"]["nav_post"]
        group_chatid = data["main"]["group_chatid"]
        rules_id = data["main"]["rules_id"]
        nav_post_id = data["main"]["nav_post_id"]
        misc_thanks_post = data["misc"]["thanks_post"]
        thanks_post_id = data["main"]["thanks_post_id"]

reload()