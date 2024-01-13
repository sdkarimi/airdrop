from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Updater, Filters, CallbackQueryHandler
from telegram import ParseMode, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, ChatAction
import threading
from functools import wraps
from userdb import *
import re
from mbot import * 
import random



JOIN_STATE, ONE, TWO, WALLET_STATE, GET_BONUS , SET_WALLET , GET_WALLET= range(7)

base_link = "URL_your_BOT"


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
    global a
    a=x-y
    update.message.reply_text(f'به ربات ما خوش اومدی 😘 \n حاصل عبارت ریز رو بفرست:  \n {x}-{y} =?')
    return ONE
    
   

def menus(update,context):
    file_link=open('channel_link.txt','r+')
    file_link=file_link.read()
    link=file_link.split(",")
    button_list = []
    i=1
    for each in link:
        button_list.append(InlineKeyboardButton(f"کانال{i}", url = each))
        i+=1
        
    button_list.append(InlineKeyboardButton(f"YOURCHANNEL(CHANNEL_PAID)", url = "URL_CHANNEL"))
    buttons=build_menu(button_list,n_cols=2)
    buttons.append([InlineKeyboardButton('I joined', callback_data=5)])

    reply_markup=InlineKeyboardMarkup(buttons) 
    context.bot.send_message(chat_id=update.message.chat_id, text='Please join the following groups:',reply_markup=reply_markup)


def build_menu(buttons,n_cols,header_buttons=None,footer_buttons=None):
  menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)   ]
  if header_buttons:
    menu.insert(0, header_buttons)
  if footer_buttons:
    menu.append(footer_buttons)
  return menu


@show_chat_action(ChatAction.TYPING)
def one(update, context):
    chat_id= update.effective_chat.id
    text=update.message.text
  
    if a==int(text):

        menus(update,context)
        return JOIN_STATE
    else:
        
        update.message.reply_text('You guessed wrong 😓 \n Send the correct amount again')
        return ONE
     





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
            result = context.bot.get_chat_member(channel, chat_id).status
            if result.status != "member" and result.status != "administrator" and result.status != 'creator' and result.status !='restricted':
                flag = False
                print(flag)
          
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
    print(select_bonus(chat_id)[0])
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
   
    keys=[['User information👤'],['لینک زیرمجموعه‌گیری🚸','📥برداشت'],['💳کیف پول💳']]

    reply_markup = ReplyKeyboardMarkup(keys, resize_keyboard=True)
    update.message.reply_text("میتونی شروع کنی😍", reply_markup=reply_markup)

@show_chat_action(ChatAction.TYPING)
def two(update, context):
    txt = update.message.text
    chat_id = update.effective_chat.id
    query=update.callback_query
    if txt == 'اطلاعات کاربر👤':
        rs = select(chat_id)
        if rs:
            username = update.effective_chat.username
            name = update.effective_chat.first_name
            sub = int(rs[0][1])
            blc=rs[0][6]
            
            update.message.reply_text(f"🔰آیدی: {username}\n👤کاربر: {name}\n 📊تعداد زیرمجموعه‌ها: {sub} \n 💰موجودی  :{blc} SHIB")
    elif txt == '📥برداشت':
        rs = select(chat_id)
        if rs[0][1] >= 2 and rs[0][6]>=100000:
            if if_wallet_exist(chat_id): 
            #تعداد زیر مجموعه برای برداشت و مقدار موجودی برای یرداشت
                keys = [['بازگشت']]
                reply_markup = ReplyKeyboardMarkup(keys, resize_keyboard=True)
                update.message.reply_text(f"مقدار برداشت را وارد کنید:", reply_markup=reply_markup)
                return WALLET_STATE
            else:
                update.message.reply_text("ولت شما تنظیم نشده است❗️ ابتدا ولت خود را با دکمه کیف پول تنظیم کنید .")
        else:
            update.message.reply_text(f"برای حداقل برداشت باید   2 زیرمجموعه و 100000 shib  داشته باشید.")
    elif txt == "بازگشت" or txt=='بازگشت🔙':
        show_buttons(update, context)
        return TWO
    elif txt == 'لینک زیرمجموعه‌گیری🚸':
        link = "<a>"+base_link + str(chat_id)+"</a>"
       
        form= """به ایردراپ ما خوش اومدید 🙂 \n لینک شما:: \n """ + link
        context.bot.send_photo(chat_id, photo=open("index.jpg","rb"),caption=form,parse_mode='HTML')

    elif txt == '💳کیف پول💳':
            
            wallt(update,context)
            return SET_WALLET
    
    elif txt=='/start' or txt=="start":
        show_buttons(update, context)
        return TWO
 
    if query.data == 9:
        print('yes')
        
def wallt(update,context):    
        chat_id=update.effective_chat.id    
        w=if_wallet_exist(chat_id)
        if w:
            key = [['🧳تغییر ولت🧳'],['بازگشت🔙']]
            reply_markup = ReplyKeyboardMarkup(key, resize_keyboard=True)
            update.message.reply_text(f'کیف پول شما قبلا ثبت شده \n `{w[0]}` \n  اگر قصد تغییر آن را دارید از دکمه ریز استفاده کنید',reply_markup=reply_markup,parse_mode=ParseMode.MARKDOWN_V2)
        
        else:
            key = [['تنظیم ولت🧳'],['بازگشت🔙']]
            reply_markup = ReplyKeyboardMarkup(key, resize_keyboard=True)
            update.message.reply_text("ولت شما تنظیم نشده است با استفاده از دکمه زیر میتونید ولت خود را تنظیم کنید.",reply_markup=reply_markup)
                    
        
@show_chat_action(ChatAction.TYPING)
def wallet_state(update, context):
    blc = update.message.text
    chat_id = update.effective_chat.id
    if blc == 'بازگشت':
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
                if result != "member" and result != "administrator" and result != 'creator':
                    flagm = False       
                    
            if flagm :
                if bc>=int(blc):
                    if int(blc)>=100000:
                        sub_1 = bc-int(blc)
                        msg=f"""📥درخواست برداشت \n 👤کاربر ::{update.effective_chat.username}  \n 💰آدرس کیف پول :: \n {row} \n  مقدار:: {blc} shib \n  ✅در حال واریز ... """
                        update.message.reply_text("ادرس شما به درستی ثبت شد \n واریز بین 10 دقیقه تا 10ساعت طول میکشد \n از صبوری شما متشکریم ")
                        context.bot.send_message(-1001772946056, msg)
                        #ایدی عددی ربات پرداخت را در بالا بزارید دقت کنید حتما اولش -100 باشه 
                        
                        clear_sub_number(chat_id,sub_1)
                        show_buttons(update, context)
                        return TWO     
                    else:
                        update.message.reply_text('حداقل برداشت 100000 shib  میباشد')
                        
                else:
                    update.message.reply_text('مقدار وارد شده بیشتر از موجودی شما است')
            elif not flagm :
                if bc>=int(blc):
                    if int(blc)>=100000:    
                        sub_1 = bc-int(blc) 
                        update.message.reply_text(" به دلیل لف دادن از کانالهای ربات واریز برای شما انجام نخواهد شد. \n با پشتیبانی در تماس باشید ")
                        msg = f""" درخواست برداشت 📥 \n کاربر ::  {update.effective_chat.username} \n  آدرس کیف پول :: \n {row} \n  مقدار :: {blc}  \n واریز نشد. ❌ \n دلیل :لف دادن از کانالها """
                        context.bot.send_message(-1001772946056, msg)
                        #ایدی عددی ربات پرداخت را در بالا بزارید دقت کنید حتما اولش -100 باشه 
                        clear_sub_number(chat_id,sub_1)
                        show_buttons(update, context)
                        return TWO
                    else:
                            update.message.reply_text('حداقل برداشت 100000 shib  میباشد')
                        
        except Exception as e:
            update.message.reply_text('مشکلی پیش اومده اگر مقدار را اشتباه وارد کردید دوباره تلاش کنید')
 
             
         
@show_chat_action(ChatAction.TYPING)        
def set_wallet(update, context):
    wallet = update.message.text
    chat_id=update.effective_chat.id
    
    if wallet=='بازگشت🔙':
        show_buttons(update,context)
        return TWO
    elif wallet == '🧳تغییر ولت🧳' or wallet=='تنظیم ولت🧳':
        update.message.reply_text('ولت خود را بفرستید :')
        return GET_WALLET
        
def get_wallet(update,context):
    wallet = update.message.text
    chat_id=update.effective_chat.id
    if wallet :
        if wallet[0]=='0' and wallet[1]=='x' and len(wallet)>28:
            insert_wallet(wallet,chat_id)
            update.message.reply_text('ولت ثبت شد ✅')
            show_buttons(update,context)
            return TWO
        else:
            update.message.reply_text('ادرس ارسال شده معتبر نیست')

            
updater = Updater("5605389073:AAEEvqSQeLPWF4qsSsHGM8hH9e0mwsBgN7s")
#به جای TOKEN توکن ربات خود را بزارید

def shotdown():
    updater.stop()
    updater.is_idle= False
    
@show_chat_action(ChatAction.TYPING)
def stop(update,context):
    threading.Thread(target=shotdown).start()

def error_handler(update, context):
    error = context.error

def main():
    
    dp = updater.dispatcher
    conv = ConversationHandler( 
        entry_points=[CommandHandler('start', start)],
    
        states= {
            
             JOIN_STATE:[CallbackQueryHandler(join_state)],
             ONE:[
                    MessageHandler(Filters.text & ~Filters.command , one)
                ],
            GET_BONUS:[MessageHandler(Filters.text ,get_bonus)],
            TWO:[MessageHandler(Filters.text , two),CallbackQueryHandler(set_wallet)],
            WALLET_STATE:[MessageHandler(Filters.text & ~Filters.command, wallet_state)],
            SET_WALLET:[MessageHandler(Filters.text & ~Filters.command,set_wallet)],
            GET_WALLET:[MessageHandler(Filters.text & ~Filters.command,get_wallet)]
            
            

        },
        fallbacks=[CommandHandler('stop', stop)]
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
    dp.add_handler(CommandHandler("sdstop",stop))
    dp.add_error_handler(error_handler)
    updater.start_polling()
    updater.idle()

if __name__  == "__main__":
    main()

