import os
import importlib

# 현재 디렉토리 내 모든 .py 파일을 찾아 모듈로 임포트
module_files = [f[:-3] for f in os.listdir(os.path.dirname(__file__)) 
                if f.endswith(".py") and f != "__init__.py"]

for module in module_files:
    module_obj = importlib.import_module(f".{module}", package=__name__)
    globals().update({name: getattr(module_obj, name) for name in dir(module_obj) if not name.startswith("_")})
