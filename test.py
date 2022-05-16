
import sys, os
try:
    raise NameError
except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    err_name = str(type(e)).split()[1].strip("> '")
    log.append_log(f"{err_name}: File: {fname}, Line: {exc_tb.tb_lineno}, Error: {e}")