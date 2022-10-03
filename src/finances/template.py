# -*- coding: utf-8 -*-
from __future__ import annotations

from abc import ABC
from pprint import pformat
from typing import Type, TypeVar, final, get_origin, get_type_hints

T = TypeVar("T", bound="_Template")


class _Template(ABC):
    _repr_format = dict(
        depth=2,
        sort_dicts=False,
        width=120,
        compact=True,
    )

    def __repr__(self):
        return "<{0} at {1}>\n{2}".format(
            self.objname,
            hex(id(self)),
            pformat(vars(self), **self._repr_format),
        )

    @classmethod
    def factory(cls: Type[T], **kwargs) -> T:
        """Override this factory to instantiate other Template objects if required"""
        return cls(**kwargs)

    @classmethod
    @final
    def from_config(cls: Type[T], config: dict) -> T:
        return cls.factory(**config)

    @classmethod
    @final
    def get_config(cls: Type[T], recursive=True, as_dict=False) -> dict | tuple[T, dict]:
        factory = get_type_hints(cls.factory)
        factory.pop("cls", None)
        factory.pop("return", None)

        init = get_type_hints(cls.__init__)
        init.pop("return", None)

        config = init | factory
        for key, hint in init.items():
            if key in factory:
                if recursive and get_origin(hint) is None and issubclass(hint, _Template):
                    config[key] = hint.get_config(as_dict=as_dict)
                elif not as_dict:
                    config[key] = hint, config[key]

        return config if as_dict else (cls, config)

    @property
    def objname(self) -> str:
        name = self.__class__.__name__

        if hasattr(self, "name"):
            name = f"{name} {self.name}"

        return name
