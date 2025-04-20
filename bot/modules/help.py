from ..helper.ext_utils.bot_utils import COMMAND_USAGE, new_task
from ..helper.ext_utils.help_messages import (
    YT_HELP_DICT,
    MIRROR_HELP_DICT,
    CLONE_HELP_DICT,
    beast_help,
)
from ..helper.telegram_helper.button_build import ButtonMaker
from ..helper.telegram_helper.message_utils import (
    edit_message,
    delete_message,
    send_message,
)
from ..helper.ext_utils.help_messages import help_string


@new_task
async def arg_usage(_, query):
    data = query.data.split()
    message = query.message
    await query.answer()
    if data[1] == "close":
        return await delete_message(message, message.reply_to_message)
    pg_no = int(data[3])
    if data[1] == "nex":
        if data[2] == "mirror":
            await edit_message(
                message, COMMAND_USAGE["mirror"][0], COMMAND_USAGE["mirror"][pg_no + 1]
            )
        elif data[2] == "yt":
            await edit_message(
                message, COMMAND_USAGE["yt"][0], COMMAND_USAGE["yt"][pg_no + 1]
            )
        elif data[2] == "clone":
            await edit_message(
                message, COMMAND_USAGE["clone"][0], COMMAND_USAGE["clone"][pg_no + 1]
            )
    elif data[1] == "pre":
        if data[2] == "mirror":
            await edit_message(
                message, COMMAND_USAGE["mirror"][0], COMMAND_USAGE["mirror"][pg_no + 1]
            )
        elif data[2] == "yt":
            await edit_message(
                message, COMMAND_USAGE["yt"][0], COMMAND_USAGE["yt"][pg_no + 1]
            )
        elif data[2] == "clone":
            await edit_message(
                message, COMMAND_USAGE["clone"][0], COMMAND_USAGE["clone"][pg_no + 1]
            )
    elif data[1] == "back":
        if data[2] == "m":
            await edit_message(
                message, COMMAND_USAGE["mirror"][0], COMMAND_USAGE["mirror"][pg_no + 1]
            )
        elif data[2] == "y":
            await edit_message(
                message, COMMAND_USAGE["yt"][0], COMMAND_USAGE["yt"][pg_no + 1]
            )
        elif data[2] == "c":
            await edit_message(
                message, COMMAND_USAGE["clone"][0], COMMAND_USAGE["clone"][pg_no + 1]
            )
    elif data[1] == "mirror":
        buttons = ButtonMaker()
        buttons.data_button("Back", f"help back m {pg_no}")
        button = buttons.build_menu()
        await edit_message(message, MIRROR_HELP_DICT[data[2]], button)
    elif data[1] == "yt":
        buttons = ButtonMaker()
        buttons.data_button("Back", f"help back y {pg_no}")
        button = buttons.build_menu()
        await edit_message(message, YT_HELP_DICT[data[2]], button)
    elif data[1] == "clone":
        buttons = ButtonMaker()
        buttons.data_button("Back", f"help back c {pg_no}")
        button = buttons.build_menu()
        await edit_message(message, CLONE_HELP_DICT[data[2]], button)
    elif data[1] == "beast":
        buttons = ButtonMaker()
        buttons.data_button("Back", "help back help 0")
        button = buttons.build_menu()
        await edit_message(message, beast_help, button)


@new_task
async def bot_help(_, message):
    buttons = ButtonMaker()
    buttons.data_button("👑 Beast Commands", "help beast beast 0")
    buttons.data_button("🔗 Our Links", "help links beast 0")
    buttons.data_button("🔍 All Commands", "help all beast 0")
    buttons.data_button("❌ Close", "help close beast 0")
    button = buttons.build_menu(2)
    await send_message(
        message, 
        f"<b>Welcome to Mirror Beast Help</b>\n\n<i>Select an option below to view help information:</i>", 
        button
    )


@new_task
async def help_cb(_, query):
    message = query.message
    data = query.data.split()
    await query.answer()
    
    if data[1] == "beast":
        buttons = ButtonMaker()
        buttons.data_button("Back", "help back help 0")
        button = buttons.build_menu()
        await edit_message(message, beast_help, button)
    elif data[1] == "links":
        buttons = ButtonMaker()
        buttons.url_button("📢 Channel", "https://t.me/MirrorBeast")
        buttons.url_button("💬 Support", "https://t.me/MirrorBeastSupport")
        buttons.url_button("🌐 Leech Group", "https://t.me/MirrorBeastGroup")
        buttons.url_button("🔗 Other Links", "https://t.me/MirrorBeastGateways/8")
        buttons.data_button("Back", "help back help 0")
        button = buttons.build_menu(2)
        text = "<b>Mirror Beast Links</b>\n\n<i>Access our network of services through these official links:</i>"
        await edit_message(message, text, button)
    elif data[1] == "all":
        await edit_message(message, help_string)
    elif data[1] == "back":
        buttons = ButtonMaker()
        buttons.data_button("👑 Beast Commands", "help beast beast 0")
        buttons.data_button("🔗 Our Links", "help links beast 0")
        buttons.data_button("🔍 All Commands", "help all beast 0")
        buttons.data_button("❌ Close", "help close beast 0")
        button = buttons.build_menu(2)
        await edit_message(
            message, 
            f"<b>Welcome to Mirror Beast Help</b>\n\n<i>Select an option below to view help information:</i>", 
            button
        )
    elif data[1] == "close":
        await delete_message(message, message.reply_to_message)
