def is_raspberry():
    try:
        with open("/sys/firmware/devicetree/base/model") as f:
            return "raspberry pi" in f.read().lower()
    except FileNotFoundError:
        return False