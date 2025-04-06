def run_ws():
    import asyncio
    from mobile import start_server
    asyncio.run(start_server())

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    run_ws()