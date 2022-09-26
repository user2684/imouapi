"""Abstract class representing an entity attached to an Imou device."""
from abc import ABC, abstractmethod


class ImouEntity(ABC):
    """A representation of a sensor within an IMOU Device."""

    @abstractmethod
    async def async_update(self, **kwargs):
        """Update the entity."""

    @abstractmethod
    def get_device_id(self) -> str:
        """Get device id."""

    @abstractmethod
    def get_name(self) -> str:
        """Get name."""

    @abstractmethod
    def get_description(self) -> str:
        """Get description."""

    @abstractmethod
    def get_icon(self) -> str:
        """Get icon."""

    @abstractmethod
    def set_enabled(self, value: bool) -> None:
        """Set enable."""
