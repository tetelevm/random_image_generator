import re
import json
import asyncio
import logging
from functools import partial
from io import BytesIO
from multiprocessing import Process, Queue, Manager
from queue import Empty
from pathlib import Path
from typing import Tuple, Dict, Callable, Coroutine

from telegram import Update, Chat
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext
from telegram.ext.filters import ChatType, TEXT

from implementers import Generator


def _get_bot_args():
    """
    Reads envs from the file.
    """

    envs_file = Path().absolute() / ".envs"
    try:
        with open(envs_file, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        raise ValueError("Requires the settings file `.envs` in the root of the project")


def _get_logger():
    """
    Returns the configured logger.
    """

    logger_ = logging.Logger("logger", level=logging.INFO)
    handler = logging.FileHandler("logs.log", mode='a')
    handler.setFormatter(logging.Formatter("{asctime:<23} >>| {msg}", style='{'))
    logger_.addHandler(handler)
    return logger_


def log(text):
    """
    Outputs messages to where you want them printed.
    """
    print(text)
    logger.info(text)


args = _get_bot_args()
logger = _get_logger()


class Bot:
    """
    Bot class. Works in 2 processes and 2 coroutines:
    - coroutine of receiving signals
    - coroutine with a loop to send results
    - process of generating small images
    - process of generating large images
    """

    def __init__(self, token: str):
        self.token = token
        self.generator = Generator()
        self.callbacks: Dict[int, Tuple[Callable, Coroutine]] = dict()

        manager = Manager()
        self.queue_small = manager.Queue()
        self.queue_big = manager.Queue()
        self.queue_ready = manager.Queue()

        self.process_generation_small = Process(
            target=self._generation_process_func,
            args=(self.queue_small,),
            daemon=True
        )
        self.process_generation_big = Process(
            target=self._generation_process_func,
            args=(self.queue_big,),
            daemon=True
        )
        self.process_generation_small.start()
        self.process_generation_big.start()

    def _generate_image(self, text: str, size: int) -> BytesIO:
        """
        Generates an image from text and writes it in byte form.
        """

        complexity = Generator.get_complexity(text)
        image = self.generator.create_image(text, complexity, size)
        byte_io = BytesIO()
        image.save(byte_io, 'png')
        byte_io.seek(0)
        return byte_io

    def _generation_process_func(self, queue: Queue):
        """
        A generation function that is placed in a separate process.
        It reads parameters from a special queue, generates an image and
        puts it in the queue for ready results.
        """

        while True:
            (user_id, text, size) = queue.get()
            log(f" F start generation <{size}>/<{text}>")

            try:
                bytes_image = self._generate_image(text, size)
                msg = f" F generated <{size}>/<{text}>"
                succ = True
            except:
                bytes_image = b""
                msg = f"ERROR! Not generated image <{size}>/<{text}>"
                succ = False

            log(msg)
            self.queue_ready.put_nowait((user_id, bytes_image, text, succ))

    @staticmethod
    async def _send_image_as_photo(chat: Chat, bytes_png, text):
        """
        Sends the image as a photo (with compression).
        """
        await chat.send_photo(bytes_png, caption=text)

    @staticmethod
    async def _send_image_as_document(chat: Chat, bytes_png, text):
        """
        Sends the image as a document (without compression).
        """
        filename = re.sub(r"[^\wА-ЯЁа-яё \-]", "", text)[:20]
        filename = (filename or "image") + ".png"
        await chat.send_document(bytes_png, caption=text, filename=filename)

    async def _send_error_message(self, chat: Chat):
        """
        Sends an error message to the desired chat room.
        """
        await chat.send_message(self.messages["error"])

    # =================================================================

    messages = {
        "start": (
            "🇦🇶 Hi! I am a bot that can generate random images from a phrase.\n"
            "✏️ Write me something and you'll get an image."
        ),
        "help": (
            "🇦🇶 Send a message and get a picture.\n"
            "\n"
            "🌄 To get small images (128px) you just have to write a message,"
            " to get a big image (512px) you have to reply to your own message"
            " with the &lt;<code>/big</code>&gt; command.\n"
            "The small image is of poor quality, but it is generated quickly,"
            " so you can use it to preview the result.\n"
            "The large one takes a very long time to generate, but is of normal"
            " quality.\n"
            "\n"
            "🐙 There is no much help, the source code is "
            f"<a href=\"{args['GITHUB']}\">here.</a>"
        ),
        "busy": "🕓 I'm already generating, wait for the result.",
        "no_reply": "🐞 You need to reply to a message with a text!",
        "error": "🐞 An error occurred during generation.",
    }

    async def command_start(self, update: Update, context: CallbackContext):
        """
        Standard welcome for the bot.
        """
        await update.effective_chat.send_message(self.messages["start"])

    async def command_help(self, update: Update, context: CallbackContext):
        """
        Standard help for the bot.
        """
        await update.effective_chat.send_message(
            self.messages["help"],
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )

    async def get_small_image(self, update: Update, context: CallbackContext):
        """
        Image generation by text.
        The image is generated small and sent with compression to make it
        faster and more visible.
        """

        user_id = update.effective_chat.id
        if user_id in self.callbacks:
            await update.effective_chat.send_message(self.messages["busy"])
            return

        text = update.message.text
        self.queue_small.put_nowait((user_id, text, 128))

        callback = partial(self._send_image_as_photo, update.effective_chat)
        error_coro = self._send_error_message(update.effective_chat)
        self.callbacks[user_id] = (callback, error_coro)

    async def get_big_image(self, update: Update, context: CallbackContext):
        """
        Generating a lossless large size image. To generate, you must
        reply to a message with the text to generate with the `/big`
        command.
        """

        if (
                not update.message.reply_to_message
                or not update.message.reply_to_message.text
        ):
            await update.effective_chat.send_message(self.messages["no_reply"])
            return

        user_id = update.message.from_user.id
        if user_id in self.callbacks:
            await update.effective_chat.send_message(self.messages["busy"])
            return

        text = update.message.reply_to_message.text
        self.queue_big.put_nowait((user_id, text, 512))

        callback = partial(self._send_image_as_document, update.effective_chat)
        error_coro = self._send_error_message(update.effective_chat)
        self.callbacks[user_id] = (callback, error_coro)

    async def start_bot(self):
        """
        Bot initialization and start function. All interactions happen
        in private chat by text.
        """

        app = Application.builder().token(self.token).build()
        filter_ = TEXT & ChatType.PRIVATE
        app.add_handler(CommandHandler("start", self.command_start, filter_, block=False))
        app.add_handler(CommandHandler("help", self.command_help, filter_, block=False))
        app.add_handler(CommandHandler("big", self.get_big_image, filter_, block=False))
        app.add_handler(MessageHandler(filter_, self.get_small_image, block=False))

        await app.initialize()
        updates = [Update.MESSAGE, Update.POLL_ANSWER]
        await app.updater.start_polling(allowed_updates=updates)
        await app.start()
        log("Bot has started")

    async def response_loop(self):
        """
        A special loop that checks to see if there are results ready to
        send. If there are ready, it sends them.
        """

        while True:
            await asyncio.sleep(1)
            try:
                (user_id, image, text, succ) = self.queue_ready.get_nowait()
            except Empty:
                continue

            callback, error_coro = self.callbacks.pop(user_id)
            if succ:
                asyncio.create_task(callback(image, text))
                error_coro.close()
            else:
                asyncio.create_task(error_coro)


async def run_bot(*coros: Coroutine):
    """
    Just a small extra function that run all the necessary coroutines of
    the bot and does not let the program stop.
    """

    await asyncio.gather(*coros)
    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    TOKEN = args["TOKEN"]
    bot = Bot(TOKEN)
    pull_coro = bot.start_bot()
    response_coro = bot.response_loop()
    asyncio.run(run_bot(pull_coro, response_coro))
