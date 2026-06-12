from pydantic import ValidationError


def format_validation_errors(errors: list[dict]) -> str:
    """Return compact validation errors suitable for API responses."""
    messages = []
    for issue in errors:
        location_parts = [str(part) for part in issue.get("loc", ()) if part not in ("body", "query", "path")]
        location = ".".join(location_parts)
        message = issue.get("msg", "Invalid value")
        messages.append(f"{location}: {message}" if location else message)
    return "; ".join(messages)


def format_validation_error(error: ValidationError) -> str:
    return format_validation_errors(error.errors())
