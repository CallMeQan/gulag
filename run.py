if __name__ == '__main__':
    from dotenv import load_dotenv
    from run_flask import run_flask
    from run_ws import run_ws
    from threading import Thread
    import time
    import logging
    load_dotenv()
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting Flask server...")
    flask_thread = Thread(target=run_flask)
    flask_thread.start()
    
    time.sleep(5)  # Give Flask some time to start
    
    logging.info("Starting WebSocket server...")
    ws_thread = Thread(target=run_ws)
    ws_thread.start()
    flask_thread.join()
    ws_thread.join()
    logging.info("Both servers have been started.")