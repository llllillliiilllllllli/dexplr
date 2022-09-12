from typing import Any, Tuple
import sys
import inspect
from Styles import Color 
from Utils import Log

def execute(selection: Tuple[Any, Any]) -> None:
    Log.info(f"Execute command: {selection[0].__name__}.{selection[1].__name__}")

    try: 
        selection[1]()
    except Exception as ex:
        Log.error(ex)

    return None
