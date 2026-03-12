"""MCP tools: weather, temperature, and author lookup."""

from typing import Literal


def get_weather(
    location: str,
    units: Literal["celsius", "fahrenheit"] = "celsius",
    include_forecast: bool = False,
) -> str:
    """Get current weather and optional 5-day forecast for a location."""
    temp = 22 if units == "celsius" else 72
    result = f"Current weather in {location}: {temp} degrees {units[0].upper()}"
    if include_forecast:
        result += "\nNext 5 days: Sunny"
    return result


def get_temp(
    location: str,
    units: Literal["celsius", "fahrenheit"] = "celsius",
) -> str:
    """Get the current temperature for a location."""
    temp = 22 if units == "celsius" else 72
    return f"Temperature in {location}: {temp}°{units[0].upper()}"


def get_author_name(book_or_work: str) -> str:
    """Get the author name for a book, article, or other work."""
    return f"Author of \"{book_or_work}\": Vikash"
