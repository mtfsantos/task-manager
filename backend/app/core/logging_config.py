import logging

def setup_logging():
    """Configures application-wide logging."""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Prevent adding handlers multiple times if reloaded (e.g., by uvicorn --reload)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
