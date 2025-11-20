from dotenv import load_dotenv
import os, sys, traceback

env_path = os.path.join(os.path.dirname(__file__), 'pizzaria_api_pkg', '.env')
load_dotenv(env_path)

try:
    import importlib
    importlib.import_module('pizzaria_api_pkg.main')
    print('imported OK')
except Exception:
    traceback.print_exc()
    sys.exit(1)
