import asyncio
from aiogram import Dispatcher
import uvicorn

from init_bot import bot
from handlers.user_handlers import router as user_router
from handlers.admin_handlers import router as adm_router
from database.database import init_db

import logging


async def run_app():
    config = uvicorn.Config('postback.init_app:app')
    server = uvicorn.Server(config=config)
    await server.serve()


async def main():
    logging.basicConfig(level=logging.INFO)
    
    await init_db()
    
    await bot.delete_webhook(drop_pending_updates=True)
    
    dp = Dispatcher()
    dp.include_routers(adm_router, user_router)
    
    bot_task = asyncio.create_task(dp.start_polling(bot))
    app_task = asyncio.create_task(run_app())
    
    await asyncio.gather(
        bot_task,
        app_task
    )


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass