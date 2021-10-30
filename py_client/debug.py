def debug(log_info):
    global LOG_TOGGLE
    LOG_TOGGLE = True
    def decorator(func):
        def wrapper(*args):
            if LOG_TOGGLE:
                print(log_info + "...", end=" ")
                try: 
                    result = func(*args)
                except:
                    print("ERROR")
                else:
                    print("OK")
            else:
                result = func(*args)

            return result
        return wrapper
    return decorator