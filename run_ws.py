
if __name__ == "__main__":
    import asyncio
    from dotenv import load_dotenv
    from mobile import start_server
    load_dotenv()

    asyncio.run(start_server())