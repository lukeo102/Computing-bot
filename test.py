
import sys, os
try:
    pass
    #print(hello)
    
except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(f"File: {fname}, Line: {exc_tb.tb_lineno}, Error: {e}")