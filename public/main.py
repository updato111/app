from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton,ReplyKeyboardMarkup,WebAppInfo
from pyrogram.errors.exceptions import UserNotParticipant
import pymysql
import json

with open('config/config.json', 'r') as file:
    data = json.load(file)

database_name = data["DataBase"]['database_name']

database_username = data["DataBase"]['database_username']

database_password = data["DataBase"]['database_password']


app = Client(data['Account']["chanell_link"], api_id=data['Account']["api_id"], api_hash=data['Account']["api_hash"], bot_token=data['Account']["token"])
def balance(user):
    connection = pymysql.connect(host='localhost',
                             user=database_username,
                             password=database_password,
                             database=database_name)
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM users WHERE username=%s', (user,))
        results = cursor.fetchall()

        for row in results:
            return row
    connection.close()
def intvi(username):
    connection = pymysql.connect(host='localhost',user=database_username,password=database_password,database=database_name)
    with connection.cursor() as cursor:
        sql = "UPDATE users SET invites = invites + 1 WHERE username =%s"
        cursor.execute(sql, (username,))
        connection.commit()
    connection.close()
def referral(username, friend):
    try:
        connection = pymysql.connect(host='localhost',
                             user=database_username,
                             password=database_password,
                             database=database_name)
        
        with connection.cursor() as cursor:
            select_sql = "SELECT friend FROM users WHERE username = %s"
            cursor.execute(select_sql, (username,))
            result = cursor.fetchone()
            
            if result:
                current_friends = result[0] if result[0] else ''
                friends_list = current_friends.split(',')
                
                if friend in friends_list:
                    print(f"{friend} is already a friend of {username}.")
                    return "already_exists"
                else:
                    new_friend = f",{friend}"
                    update_sql = "UPDATE users SET friend = CONCAT(friend, %s) WHERE username = %s"
                    update_balanse = "UPDATE users SET balanse = balanse + 5000 WHERE username = %s"
                    affected_rows = cursor.execute(update_sql, (new_friend, username))
                    connection.commit()
                    
                    if affected_rows == 0:
                        print(f"No rows updated. Username {username} may not exist.")
                    else:
                        cursor.execute(update_balanse, (username,))
                        connection.commit()
                        print(f"Friend {friend} updated for username {username}.")
                        return "updated"
            else:
                print(f"Username {username} does not exist.")
                return "username_not_exist"
                
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
        return "error"
    
    finally:
        connection.close()
async def check_member(client, message):

    try:
        user_id = message.from_user.id
        user = await client.get_chat_member(data['Account']["chanell_link"], user_id)
        if user.status in ['member', 'creator', 'administrator']:
            return True
    except:
        
        join = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Subscribe Channel 🤙", url="https://t.me/{}".format(data['Account']["chanell_link"]))],[InlineKeyboardButton("Check Join ðŸ”", callback_data="check_join")]]
        )
        await message.reply("Welcome to AnzabCoin bot",user_id)
        await message.reply_text("""
        To use the bot, you must first join the channel 🥔🍟
        """, reply_markup=join)
        return False
async def join(user,mess):
    mark = ReplyKeyboardMarkup(
        keyboard=[
            ["Balnsce 💰","Withdraw 💳", "Invite 🔊"]
        ],
        resize_keyboard=True
    )
    inline_keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Play 🥔",
                    web_app=WebAppInfo(url=f"{data['URL']}/index.php?chat_id={user.id}&username={user.first_name}")

                )
            ],
            [
                InlineKeyboardButton(
                    text="Join Community 😍",
                    url="https://t.me/{}".format(data['Account']["chanell_link"])
                )
            ],
            [
                InlineKeyboardButton(
                    text="Support 🔊",
                    url="https://t.me/{}".format(data["Account"]["admin_username"])
                )
            ]
        ]
    )
    try:
        await mess.reply_text("Start Top-Top!!",reply_markup=mark)
        await mess.reply_photo('photos/anzabcoin.jpg',caption=f"Hey @{user.username}! Welcome to AnzabCoin🥔\n\n💪 Tap the AnzabCoin to see your balance grow.\n"
                 "AnzabCoin is the first Decentralized Application based on a unique model where the community decides "
                    "on which blockchain the token will be listed 💎 Ton, 🧬 Solana, or 🔹 Ethereum\nMaybe all of them? \n"
                    "The choice is yours!\nGot friends, relatives, co-workers?\nBring them all into the game.\nMore Mates - more coins",reply_markup=inline_keyboard)
    except:
        await mess.message.reply_text("Start Farming",reply_markup=mark)
        await mess.message.reply_photo('photos/anzabcoin.jpg',caption=f"Hey @{user.username}! Welcome to AnzabCoin🥔\\n\n💪 Tap the AnzabCoin to see your balance grow.\n"
                 "AnzabCoin is the first Decentralized Application based on a unique model where the community decides "
                    "on which blockchain the token will be listed 💎 Ton, 🧬 Solana, or 🔹 Ethereum\nMaybe all of them? \n"
                    "The choice is yours!\nGot friends, relatives, co-workers?\nBring them all into the game.\nMore Mates - more coins",reply_markup=inline_keyboard)
        

@app.on_message(filters.command("start"))
async def start(client, message):
    user = message.from_user
    text = message.text
    check_member_filter = await check_member(client, message)
    
    if text.startswith("/start "):
        text = text.replace("/start ", "")
        if int(text) != int(text):
            ref_info = await client.get_users(text)
            
            result = referral(user.id, ref_info.first_name)
            if result == "already_exists":
                await client.send_message(user.id, f"The user {text} is already a friend.")
            elif result == "updated":
                intvi(user.id)
                await client.send_message(text, f"Good news!!\nSomeone [@{user.username}] has been invited to the bot by you 🎉✨🎯")
            if check_member_filter is None:
                await join(user, message)

                
            
    if check_member_filter == None:
        await join(user,message)
        
        

@app.on_message(filters.text)
async def Intvite(client, message):
    user = message.from_user
    
    
    if message.text == "Invite 🔊":
        await message.reply("💸 Make mining a team effort! Invite your friends to AnzabCoin and earn 10% of their total mining amount as a bonus. Let's grow our community and wealth together! 🚀\n\n"f"Your exclusive referral link: https://t.me/{data['Account']['bot_link']}?start={user.id}\n\n""Start sharing and watch your earnings multiply! ❄",reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Share With Your Freinds 👀🤟", url="https://t.me/share/url?url=https://t.me/{}?start={}&text=Join%20me%20in%20AnzabCoin%20and%20start%20mining%20today!%20Let's%20earn%20together!".format(data['Account']["bot_link"],user.id))]]
        ))
    if message.text == "Withdraw 💳":
        await message.reply("Coming Soon Listed Coin 🥔",user.id)
    if message.text == "Balnsce 💰":
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                    "Withdraw 💳", callback_data="Withdraw")
                ]
            ]
        )
        if(balance(user.id)):
            await message.reply(f"Every 100,000 AnzabCoin equal = $10\nYour balance: {balance(user.id)[1]} 💸\n"
f"Number of invitations: {balance(user.id)[3]} 🎁\n"
f"Your exclusive referral link: https://t.me/{data['Account']['bot_link']}?start={user.id} 🎯\n",user.id,reply_markup=reply_markup)
        else:
            await message.reply("To receive inventory, first collect coins, then request inventory 🥔🍟")


@ app.on_callback_query()
async def buttons(bot, update):
    query = update.data
    info = update.from_user
    if query == "Withdraw":
        await update.message.edit_text("Pick up date \n 30/08/2024")
    elif query == "check_join":
        try:
            user = await bot.get_chat_member(data['Account']["chanell_link"], info.id)
            if user:
                await update.answer('Congratulations, you can now extract ')
                await join(info,update)
        except UserNotParticipant as e:
            await update.answer("🤝 You must be a member of the channel using the bot 🙏")


app.run()
