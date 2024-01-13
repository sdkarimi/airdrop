from cmath import exp
from distutils.log import error
from http.client import BAD_REQUEST, UNAUTHORIZED
from select import select
import telegram
from telegram.ext import (
    Updater, MessageHandler,\
    CallbackQueryHandler, ConversationHandler,\
    CommandHandler, Filters
)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ChatAction, TelegramError
from admin_db import is_exist
from functools import wraps
from userdb import all_user,select,delete_user, set_sub_number ,select_ref , select_sub_ref


NAME_STATE, PASS_STATE, MAIN_STATE, GET_MESSAGE_STATE, GET_IMAGE_STATE,NUMBER_USER , GET_MESSAGE_STATE_CHATID,SEND_MESSAGE_SUPPORT,SET_SUB_CHATID , GET_SUB_CHATID = range(10)
TIMEOUT_VALUE = 900

channels_id=[]
channels_link=[]

def show_chat_action(action):
    def decorate_func(func):
        @wraps(func)
        def command_func(update, context, *args, **kwargs):
            context.bot.send_chat_action(update.effective_chat.id, action=action)
            return func(update, context, *args, **kwargs)
        return command_func
    return decorate_func

def start_m(update,context):
    text = update.message.text
    chat_id=update.effective_chat.id
    if text :
        context.bot.send_message(chat_id ,"ربات خاموش شد \n منتظر راند بعدی ما باشید . ")
@show_chat_action(ChatAction.TYPING)
def startm(update, context):
    update.message.reply_text("Hello\nPlease enter your username: ")
    return NAME_STATE

@show_chat_action(ChatAction.TYPING)
def name_state(update, context):
    username = update.message.text
    context.user_data['username'] = username
    update.message.reply_text("Please enter your password: ")
    return PASS_STATE

@show_chat_action(ChatAction.TYPING)
def pass_state(update, context):
    password = update.message.text
    context.user_data['password'] = password
    if is_exist(context.user_data['username'], password):
        update.message.reply_text("Welcome")
        users = [user[0] for user in all_user()]
        context.user_data['users'] = users
        show_button(update, context)
        return MAIN_STATE
    else:
        update.message.reply_text("Username or Password isn't correct: ")
        clear_data(context)
        update.message.reply_text("Please enter your username: ")
        return NAME_STATE

@show_chat_action(ChatAction.TYPING)
def main_state(update, context):
    chat_id = update.effective_chat.id
    query = update.callback_query
    if query.data == '0':
        context.bot.send_message(chat_id, "Please enter your message: ")
        return GET_MESSAGE_STATE
    elif query.data == '1':
        context.bot.send_message(chat_id, "Please enter your image: ")
        return GET_IMAGE_STATE
    elif query.data=="2":
        context.bot.send_message(chat_id, "Please wait...")
        return NUMBER_USER
    elif query.data=='3':
        context.bot.send_message(chat_id, "Please enter your user chat id: ")
        return GET_MESSAGE_STATE_CHATID
 
       


@show_chat_action(ChatAction.TYPING)
def get_message_state(update, context):
    counter=0
    msg = update.message.text
    for user in context.user_data['users']:
        try :
            context.bot.send_message(user, msg)
        except Exception as e:
            print(e.with_traceback)
            update.message.reply_text(f"user: {user} blocked")
            
        else:
            counter+=1
    update.message.reply_text(f"your message successfully sent {counter}")
    show_button(update, context)
    return MAIN_STATE
    



@show_chat_action(ChatAction.TYPING)
def get_image_state(update, context):
    counter=0
    file_id = update.effective_message.photo[0].file_id
    caption = update.effective_message.caption
    

    if caption:
        for user in context.user_data['users']:
            try :

                context.bot.send_chat_action(user, action=ChatAction.UPLOAD_PHOTO)
                context.bot.send_photo(user, file_id, caption=caption)
            except Exception as e:
                print(e.with_traceback)
                update.message.reply_text(f"user: {user} deleted")
            
            else:
                counter+=1
    else:
        for user in context.user_data['users']:
            try :
                context.bot.send_chat_action(user, action=ChatAction.UPLOAD_PHOTO)
                context.bot.send_photo(user, file_id)
            except Exception as e:
                print(e.with_traceback)
                update.message.reply_text(f"user: {user} deleted")
            
            else:
                counter+=1
    update.message.reply_text(f"your image successfully sent{counter}")
    show_button(update, context)
    return MAIN_STATE

@show_chat_action(ChatAction.TYPING)
def number_user(update,context):
    
    max=0
    chat_id = update.effective_chat.id
    a=len(all_user())
    s=f"تعداد کاربران :{a}"
    ms="کاربر\n "
    
    for user in context.user_data['users']:
        U=select(user)[0][3]
        if U>max:
            max =U
    for user in context.user_data['users'] :
        U=select(user)[0][3]
        if U==max :
            maximum=select(user)[0][0] 
            ms=ms + f'{maximum}:{U}\n'
           
    context.bot.send_message(chat_id,f"{s}\n{ms}")           
    show_button(update, context)
    return MAIN_STATE



s_chat_id=[]
def support_answer(update,context):
    chat_id = update.effective_chat.id
    chat_id_user = update.message.text
    try:
        if chat_id:
            s_chat_id.append(int(chat_id_user))
        context.bot.send_message(chat_id, "Please enter your user message: ")    
        return SEND_MESSAGE_SUPPORT
    except Exception as e:
             print(e.with_traceback)
             update.message.reply_text(" مشکلی پیش اومد")
             show_button(update, context)
             return MAIN_STATE
             
def send_msg_support(update,context):
    text=update.message.text
    try:
            chat_id=s_chat_id[0]
            context.bot.send_message(chat_id,text)
            update.message.reply_text(f"your image successfully sent")
            s_chat_id.clear()
            show_button(update, context)
            return MAIN_STATE
            
    except Exception as e:
             print(e.with_traceback)
             update.message.reply_text(" مشکلی پیش اومد")
             show_button(update, context)
             return MAIN_STATE






            

@show_chat_action(ChatAction.TYPING)
def time_out(update, context):
    update.message.reply_text("The robot was not used for a long time. That's why it was stopped")
    clear_data(context)
    return ConversationHandler.END

@show_chat_action(ChatAction.TYPING)
def done(update, context):
    update.message.reply_text("The robot was stopped at your request")
    clear_data(context)
    return ConversationHandler.END

@show_chat_action(ChatAction.TYPING)
def show_button(update, context):
    keys = [
        [
            InlineKeyboardButton("Send message", callback_data=0),
            InlineKeyboardButton("Send image", callback_data=1),
        ],
        [
            InlineKeyboardButton("number users", callback_data=2),
            InlineKeyboardButton("send msg with id", callback_data=3)
        ]
    
    ]

    reply_markup = InlineKeyboardMarkup(keys)
    update.message.reply_text("Please choose your command: ", reply_markup=reply_markup)
def clear_data(context):
    context.user_data.clear()

def error_handler(update, context):
    error = context.error
    
    print(error)
def main():
    #
    updater = Updater("5359297975:AAH1MkunGAlOMumUJpiANsQa6GeOejkRaP4")
    dp = updater.dispatcher

    conv = ConversationHandler(
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

    convm=CommandHandler("start",start_m)
    
    dp.add_error_handler(error_handler)
    dp.add_handler(convm)
    dp.add_handler(conv)
    
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()