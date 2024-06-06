from typing import (Any, Dict, 
                    ItemsView, KeysView,
                    Literal, ValuesView, TypeAlias, Union, MutableMapping)
from loguru import logger
import datetime

Key:TypeAlias = Union[str, int]


class State(MutableMapping[Key, Any]):
    """Implement all methods of streamlit.SessionState
     'clear', 'get', 'items', 'keys', 'pop', 'popitem', 
     'setdefault', 'to_dict', 'update', 'values'
    """
    _instance = None

    def __new__(cls, at: Literal["cli", "web"]):
        if cls._instance is None:
            cls._instance = super(State, cls).__new__(cls)
            cls._instance._init_state(at)
        return cls._instance

    def _init_state(self, at: Literal["cli", "web"]):
        self._session_id = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        logger.add(f"logs/{self._session_id}.log", rotation="10 MB")
        if at == "cli":
            self._state = {}
        elif at == "web":
            import streamlit as st
            self._state = st.session_state

    def __getitem__(self, key: Key) -> Any:
        return self._state[key]

    def __setitem__(self, key: Key, value: Any):
        self._state[key] = value
        logger.info(f"Set {key} = {value}")

    def __delitem__(self, key: Key):
        del self._state[key]
        logger.info(f"Deleted {key}")

    def __getattr__(self, key: Key) -> Any:
        try:
            return self._state[key]
        except KeyError:
            raise AttributeError(f"'State' object has no attribute '{key}'")

    def __setattr__(self, key: Key, value: Any):
        if key in ["_state", "_session_id", "_at"]:
            super().__setattr__(key, value)
        else:
            self._state[key] = value
            logger.info(f"Set {key} = {value}")

    def __delattr__(self, key: Key):
        try:
            del self._state[key]
            logger.info(f"Deleted {key}")
        except KeyError:
            raise AttributeError(f"'State' object has no attribute '{key}'")

    def __iter__(self):
        return iter(self._state)

    def __len__(self):
        return len(self._state)

    def clear(self):
        self._state.clear()
        logger.info("Cleared all state")

    def get(self, key: Key, default: Any = None) -> Any:
        return self._state.get(key, default)

    def items(self) -> ItemsView[Key, Any]:
        return self._state.items()

    def keys(self) -> KeysView[Key]:
        return self._state.keys()

    def pop(self, key: Key, default: Any = None) -> Any:
        value = self._state.pop(key, default)
        logger.info(f"Popped {key} = {value}")
        return value

    def popitem(self) -> Any:
        item = self._state.popitem()
        logger.info(f"Popped item {item}")
        return item

    def setdefault(self, key: Key, default: Any = None) -> Any:
        value = self._state.setdefault(key, default)
        logger.info(f"Set default {key} = {value}")
        return value

    def to_dict(self) -> Dict[Key, Any]:
        return dict(self._state)

    def update(self, *args, **kwargs):
        self._state.update(*args, **kwargs)
        logger.info(f"Updated state with {args}, {kwargs}")

    def values(self) -> ValuesView[Any]:
        return self._state.values()


def initialize_state(at: Literal["cli", "web"]) -> State:
    return State(at)

# Initialize the global state
state: State = initialize_state("cli")