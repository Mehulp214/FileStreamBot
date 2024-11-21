# # This file is a part of FileStreamBot

# import sys
# import asyncio
# import logging
# import logging.handlers as handlers
# from .vars import Var
# from aiohttp import web
# from pyrogram import idle
# from WebStreamer import utils
# from WebStreamer import StreamBot
# from WebStreamer.server import web_server
# from WebStreamer.bot.clients import initialize_clients


# logging.basicConfig(
#     level=logging.INFO,
#     datefmt="%d/%m/%Y %H:%M:%S",
#     format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
#     handlers=[logging.StreamHandler(stream=sys.stdout),
#               handlers.RotatingFileHandler("streambot.log", mode="a", maxBytes=104857600, backupCount=2, encoding="utf-8")],)

# logging.getLogger("aiohttp").setLevel(logging.ERROR)
# logging.getLogger("pyrogram").setLevel(logging.ERROR)
# logging.getLogger("aiohttp.web").setLevel(logging.ERROR)

# server = web.AppRunner(web_server())

# #if sys.version_info[1] > 9:
# #    loop = asyncio.new_event_loop()
# #    asyncio.set_event_loop(loop)
# #else:
# loop = asyncio.get_event_loop()

# async def start_services():
#     print()
#     print("-------------------- Initializing Telegram Bot --------------------")
#     await StreamBot.start()
#     bot_info = await StreamBot.get_me()
#     StreamBot.username = bot_info.username
#     print("------------------------------ DONE ------------------------------")
#     print()
#     print(
#         "---------------------- Initializing Clients ----------------------"
#     )
#     await initialize_clients()
#     print("------------------------------ DONE ------------------------------")
#     if Var.KEEP_ALIVE:
#         print("------------------ Starting Keep Alive Service ------------------")
#         print()
#         asyncio.create_task(utils.ping_server())
#     print("--------------------- Initializing Web Server ---------------------")
#     await server.setup()
#     await web.TCPSite(server, Var.BIND_ADDRESS, Var.PORT).start()
#     print("------------------------------ DONE ------------------------------")
#     print()
#     print("------------------------- Service Started -------------------------")
#     print("                        bot =>> {}".format(bot_info.first_name))
#     if bot_info.dc_id:
#         print("                        DC ID =>> {}".format(str(bot_info.dc_id)))
#     print(" URL =>> {}".format(Var.URL))
#     print("------------------------------------------------------------------")
#     await idle()

# async def cleanup():
#     await server.cleanup()
#     await StreamBot.stop()

# if __name__ == "__main__":
#     try:
#         loop.run_until_complete(start_services())
#     except KeyboardInterrupt:
#         pass
#     except Exception as err:
#         logging.error(err.with_traceback(None))
#     finally:
#         loop.run_until_complete(cleanup())
#         loop.stop()
#         print("------------------------ Stopped Services ------------------------")

# This file is a part of FileStreamBot

import sys
import asyncio
import logging
from logging.handlers import RotatingFileHandler
from aiohttp import web
from pyrogram import idle
from WebStreamer import utils
from WebStreamer import StreamBot
from WebStreamer.server import web_server
from WebStreamer.bot.clients import initialize_clients
from .vars import Var

logging.basicConfig(
    level=logging.INFO,
    datefmt="%d/%m/%Y %H:%M:%S",
    format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(stream=sys.stdout),
        RotatingFileHandler("streambot.log", mode="a", maxBytes=104857600, backupCount=2, encoding="utf-8"),
    ],
)

logging.getLogger("aiohttp").setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.ERROR)

server = web.AppRunner(web_server())
loop = asyncio.get_event_loop()

# Add a running flag to track the bot's state
StreamBot.running = False

async def start_services():
    try:
        print("\n-------------------- Initializing Telegram Bot --------------------")
        await StreamBot.start()
        StreamBot.running = True
        bot_info = await StreamBot.get_me()
        StreamBot.username = bot_info.username
        print(f"Bot initialized: {bot_info.first_name} (@{bot_info.username})")
        print("------------------------------ DONE ------------------------------\n")

        print("---------------------- Initializing Clients ----------------------")
        await initialize_clients()
        print("------------------------------ DONE ------------------------------")

        if Var.KEEP_ALIVE:
            print("------------------ Starting Keep Alive Service ------------------")
            asyncio.create_task(utils.ping_server())

        print("--------------------- Initializing Web Server ---------------------")
        await server.setup()
        await web.TCPSite(server, Var.BIND_ADDRESS, Var.PORT).start()
        print("------------------------------ DONE ------------------------------\n")

        print("------------------------- Service Started -------------------------")
        print(f"                        Bot: {bot_info.first_name}")
        if bot_info.dc_id:
            print(f"                        DC ID: {bot_info.dc_id}")
        print(f"                        URL: {Var.URL}")
        print("------------------------------------------------------------------")
        await idle()  # Keep the program running until interrupted
    except Exception as e:
        logging.error(f"Error during startup: {e}")
        await cleanup()  # Cleanup immediately if startup fails

async def cleanup():
    try:
        print("\n------------------------ Cleaning Up ------------------------")
        await server.cleanup()
        if StreamBot.running:
            await StreamBot.stop()
            StreamBot.running = False
        print("------------------------ Cleanup Completed ------------------------")
    except Exception as e:
        logging.error(f"Error during cleanup: {e}")

if __name__ == "__main__":
    try:
        loop.run_until_complete(start_services())
    except KeyboardInterrupt:
        print("\n------------------- Keyboard Interrupt -------------------")
    except Exception as err:
        logging.error(f"Unhandled error: {err}")
    finally:
        loop.run_until_complete(cleanup())
        loop.close()
        print("------------------------ Stopped Services ------------------------")

