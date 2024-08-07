cd C:\Users\drew.bennett\Documents\cores_app\fast_api_backend
rem fastapi dev main.py
uvicorn main:app --reload --reload-include="*.html" --reload-include="*.css" --reload-include="*.js"
rem watches these files and does hot reload when changed.
cmd /k
