from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Updater, Filters, CallbackQueryHandler
from telegram import ParseMode, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, ChatAction
import threading
from functools import wraps
from userdb import *
from mbot import * 
import random



JOIN_STATE, ONE, TWO, WALLET_STATE, GET_BONUS , SET_WALLET , GET_WALLET= range(7)

base_link = "URL_your_BOT"
Wallet_pay=00000000000
TOKEN="Your Token"

def show_chat_action(action):
    def decorator(func):
        @wraps(func)
        def command(update, context, *args, **kwargs):
            context.bot.send_chat_action(update.effective_chat.id, action=action)
            return func(update, context, *args, **kwargs)
        return command
    return decorator


@show_chat_action(ChatAction.TYPING)
def start(update, context):
    
    if context.args:
        context.user_data['args'] = context.args[0]
    x=random.randint(50,100)
    y=random.randint(0,50)
    context.user_data['verify']=x-y
    update.message.reply_text(f'Welcome to our robot 😘 \n Send the result of the following statement: \n {x}-{y} =?')
    return ONE
    
   

def menus(update,context):
    file_link=open('channel_link.txt','r+')
    file_link=file_link.read()
    link=file_link.split(",")
    button_list = []
    i=1
    for each in link:
        button_list.append(InlineKeyboardButton(f"Channel{i}", url = each))
        i+=1
        
   
    buttons=build_menu(button_list,n_cols=2)
    buttons.append([InlineKeyboardButton('I joined', callback_data=5)])
    reply_markup=InlineKeyboardMarkup(buttons) 
    context.bot.send_message(chat_id=update.message.chat_id, text='Please subscribe to the following channels:',reply_markup=reply_markup)

def build_menu(buttons,n_cols,header_buttons=None,footer_buttons=None):
  menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
  if header_buttons:
    menu.insert(0, header_buttons)
  if footer_buttons:
    menu.append(footer_buttons)
  return menu



@show_chat_action(ChatAction.TYPING)
def one(update, context):
    chat_id= update.effective_chat.id
    text=update.message.text

    if text==str(context.user_data['verify']):
        menus(update,context)
        return JOIN_STATE
    else:
        
        update.message.reply_text('You guessed wrong 😓 \n Send the correct amount again')
        
     





@show_chat_action(ChatAction.TYPING)
def join_state(update, context):
    chat_id= update.effective_chat.id
    query = update.callback_query
    if query.data == '5':
        file_id=open('channel_id.txt','r+')
        file_id=file_id.read()
        id=file_id.split(",")
        channels =[]
        for i in  id:
            channels.append(int(i))
        flag = True
        for channel in channels:
            
            result = context.bot.get_chat_member(channel, chat_id)
    
            if result.status != "member" and result.status != "administrator" and result.status != 'creator':
                flag = False
                
          
        if flag:
            if not select(chat_id):
                        insert(chat_id)
                        arg=context.user_data
                        if arg.get('args'):
                            flags = select(context.user_data['args'])
                            if flags:
                                    if add_sub_number(context.user_data['args']) and add_best_sub_number(context.user_data['args']) and set_balance(context.user_data['args']):
                                        r=str(select_ref(context.user_data['args'])[0])
                                        insert_ref(context.user_data['args'],r+','+str(chat_id))
                                        context.bot.send_message(context.user_data['args'], text=f"📎User <a href='https://t.me/{update.effective_chat.username}'>{update.effective_chat.first_name}</a> entered with your link ✅   ",parse_mode=ParseMode.HTML)
                 
        
            
            key = KeyboardButton('🔱Claim 50000 tokens🔱')
            reply_markup = ReplyKeyboardMarkup([[key]], resize_keyboard=True)
        
            context.bot.send_message(chat_id, "You can receive your gift using the button below❤️‍🔥",  reply_markup=reply_markup)
            return GET_BONUS                
           
        else:
            context.bot.send_message(chat_id, "You are not a member of channels yet")
            return JOIN_STATE
            
            

                     
    
@show_chat_action(ChatAction.TYPING)
def get_bonus(update, context):
    chat_id = update.effective_chat.id
    text=update.message.text
    if text=='🔱Claim 50000 tokens🔱':
        if select_bonus(chat_id)[0]==0 :
            insert_bonus(1,chat_id)
        
            clear_sub_number(chat_id,50000)
            show_buttons(update,context)
            return TWO
        elif select_bonus(chat_id)[0]==1:
        
            show_buttons(update,context)
            return TWO
        
@show_chat_action(ChatAction.TYPING)
def show_buttons(update, context):
   
    keys=[['User information👤'],['👨‍👩‍👧‍👦Referral','📥Withdrawal'],['💳Wallet💳']]

    reply_markup = ReplyKeyboardMarkup(keys, resize_keyboard=True)
    update.message.reply_text("Wellcome😍", reply_markup=reply_markup)

@show_chat_action(ChatAction.TYPING)
def two(update, context):
    txt = update.message.text
    chat_id = update.effective_chat.id
    query=update.callback_query
    if txt == 'User information👤':
        rs = select(chat_id)
        if rs:
            username = update.effective_chat.username
            name = update.effective_chat.first_name
            sub = int(rs[0][1])
            blc=rs[0][6]
            
            update.message.reply_text(f"🔰username: {username}\n👤name: {name}\n 📊Referral Statistics: {sub} \n 💰amount :{blc} SHIB")
    elif txt == '📥Withdrawal':
        rs = select(chat_id)
        if rs[0][1] >= 2 and rs[0][6]>=100000:
            if if_wallet_exist(chat_id): 
                keys = [['🔙Back']]
                reply_markup = ReplyKeyboardMarkup(keys, resize_keyboard=True)
                update.message.reply_text(f"Enter the withdrawal amount:", reply_markup=reply_markup)
                return WALLET_STATE
            else:
                update.message.reply_text("Your voltage is not set ❗️ First, set your voltage with the wallet button.")
        else:
            update.message.reply_text(f"You must have at least 2 subcategories and 100,000 shibs to withdraw.")
    elif txt=='🔙Back':
        show_buttons(update, context)
        return TWO
    elif txt == '👨‍👩‍👧‍👦Referral':
        link = "<a>"+base_link + str(chat_id)+"</a>"
       
        form= """Welcome to our airdrop🙂 \n Your Link:: \n """ + link
        context.bot.send_photo(chat_id, photo=open("index.jpg","rb"),caption=form,parse_mode='HTML')

    elif txt == '💳Wallet💳':
            wallt(update,context)
            return SET_WALLET
    
    elif txt=='/start' or txt=="start":
        show_buttons(update, context)
        return TWO
        
def wallt(update,context):    
        chat_id=update.effective_chat.id    
        w=if_wallet_exist(chat_id)
    
        if w:
            key = [['🧳Change wallet🧳'],['🔙Back']]
            reply_markup = ReplyKeyboardMarkup(key, resize_keyboard=True)
            
            update.message.reply_text(f'Your wallet is already registered \n `{w[0]}` \n If you want to change it, use the small button',reply_markup=reply_markup,parse_mode=ParseMode.MARKDOWN_V2)

        else:
            key = [['🧳Set wallet🧳'],['🔙Back']]
            reply_markup = ReplyKeyboardMarkup(key, resize_keyboard=True)
            update.message.reply_text("Your voltage is not set. You can set your voltage using the button below.",reply_markup=reply_markup)
                    
        
@show_chat_action(ChatAction.TYPING)
def wallet_state(update, context):
    blc = update.message.text
    chat_id = update.effective_chat.id
    if blc == '🔙Back':
        show_buttons(update, context)
        return TWO
    else:
        row = if_wallet_exist(chat_id)[0]
        bc=select_balance(chat_id)[0]
        flagm=True
        try:
            file_id=open('channel_id.txt','r+')
            file_id=file_id.read()
            id=file_id.split(",")
            channels =[]
            for i in  id:
                channels.append(int(i))
            for channel in channels:
                result = context.bot.get_chat_member(channel, chat_id).status
                if result.status != "member" and result.status != "administrator" and result.status != 'creator' and result.status !='restricted':
                    flagm = False       
                    
            if flagm :
                if bc>=int(blc):
                    if int(blc)>=100000:
                        sub_1 = bc-int(blc)
                        msg=f"""📥withdrawal request \n 👤 User ::{update.effective_chat.username}  \n 💰 Wallet address :: \n {row} \n  💰the amount of:: {blc} shib \n  ✅Paying ... """
                        update.message.reply_text("Your address has been registered correctly \n The deposit takes between 10 minutes and 10 hours \n Thank you for your patience.")
                        context.bot.send_message(Wallet_pay, msg)
                        clear_sub_number(chat_id,sub_1)
                        show_buttons(update, context)
                        return TWO     
                    else:
                        update.message.reply_text('The minimum withdrawal is 100,000 Shib.')
                        
                else:
                    update.message.reply_text('The amount entered is greater than your balance')
            elif not flagm :
                if bc>=int(blc):
                    if int(blc)>=100000:    
                        sub_1 = bc-int(blc) 
                        update.message.reply_text("No deposit will be made for you due to boasting from robot channels. \n Contact support")
                        msg = f""" 📥withdrawal request \n 👤 User ::  {update.effective_chat.username} \n  💰 Wallet address:: \n {row} \n  💰the amount of :: {blc}  \n not paid ❌ \n Reason: leaving the channels"""
                        context.bot.send_message(Wallet_pay, msg)
                        clear_sub_number(chat_id,sub_1)
                        show_buttons(update, context)
                        return TWO
                    else:
                            update.message.reply_text('The minimum withdrawal is 100,000 Shib')
                        
        except Exception as e:
            update.message.reply_text('There is a problem. If you entered the wrong value, try again')
 
             
         
@show_chat_action(ChatAction.TYPING)        
def set_wallet(update, context):
    wallet = update.message.text
    chat_id=update.effective_chat.id
    if wallet=='🔙Back':
        show_buttons(update,context)
        return TWO
    elif wallet == '🧳Change wallet🧳' or wallet=='🧳Set wallet🧳':
        update.message.reply_text('Send your Wallet:')
        return GET_WALLET
        
def get_wallet(update,context):
    wallet = update.message.text
    chat_id=update.effective_chat.id
    if wallet :
        if wallet[0]=='0' and wallet[1]=='x' and len(wallet)>28:
            insert_wallet(wallet,chat_id)
            update.message.reply_text('Done✅')
            show_buttons(update,context)
            return TWO
        else:
            update.message.reply_text('The sent address is not valid')

            
updater = Updater(TOKEN)

def shotdown():
    updater.stop()
    updater.is_idle= False
    
def error_handler(update, context):
    error = context.error

async def stoped():
    pass   
        
    
def main():
    
    dp = updater.dispatcher
    conv = ConversationHandler( 
        entry_points=[CommandHandler('start', start)],
    
        states= {
            
             JOIN_STATE:[CallbackQueryHandler(join_state)],
             ONE:[MessageHandler(Filters.text & ~Filters.command , one)],
            GET_BONUS:[MessageHandler(Filters.text ,get_bonus)],
            TWO:[MessageHandler(Filters.text , two),CallbackQueryHandler(set_wallet)],
            WALLET_STATE:[MessageHandler(Filters.text & ~Filters.command, wallet_state)],
            SET_WALLET:[MessageHandler(Filters.text & ~Filters.command,set_wallet)],
            GET_WALLET:[MessageHandler(Filters.text & ~Filters.command,get_wallet)]
            
            

        },
        fallbacks=[CommandHandler('stoped', stoped)]
    )

    conv2 = ConversationHandler(
        entry_points=[CommandHandler('admin', startm)],
        states={
            NAME_STATE:[MessageHandler(Filters.text & ~Filters.command, name_state)],
            PASS_STATE:[MessageHandler(Filters.text &~ Filters.command, pass_state)],
            MAIN_STATE:[CallbackQueryHandler(main_state)],
            GET_MESSAGE_STATE:[MessageHandler(Filters.text &~ Filters.command, get_message_state)],
            GET_IMAGE_STATE:[MessageHandler(Filters.photo, get_image_state)],
            NUMBER_USER:[MessageHandler(~Filters.command,number_user)],
            GET_MESSAGE_STATE_CHATID:[MessageHandler(Filters.text &~ Filters.command, support_answer)],
            SEND_MESSAGE_SUPPORT:[MessageHandler(Filters.text &~ Filters.command,send_msg_support)],
           
            ConversationHandler.TIMEOUT:[MessageHandler(Filters.all, time_out)]
        },
        fallbacks=[CommandHandler('done', done)],
        conversation_timeout=TIMEOUT_VALUE
    )
   
    dp.add_handler(conv2)
    dp.add_handler(conv)
    dp.add_error_handler(error_handler)
    updater.start_polling()
    updater.idle()

if __name__  == "__main__":
    main()

