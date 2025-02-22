from typing import Type, Dict
from .protocols import AIProvider
from .anthropic_provider import AnthropicProvider


class AIProviderFactory:
    _providers: Dict[str, Type[AIProvider]] = {"anthropic": AnthropicProvider}

    @classmethod
    def register_provider(cls, name: str, provider_class: Type[AIProvider]) -> None:
        """Register a new AI provider"""
        cls._providers[name.lower()] = provider_class

    @classmethod
    def create_provider(cls, provider_type: str, api_key: str) -> AIProvider:
        """Create an instance of the specified AI provider"""
        provider_class = cls._providers.get(provider_type.lower())
        if not provider_class:
            available = ", ".join(cls._providers.keys())
            raise ValueError(
                f"Unknown provider type: {provider_type}. Available providers: {available}"
            )

        return provider_class(api_key)
