from starlette.requests import Request

def get_base_url(request: Request) -> str:
    """Get base URL with respect of APIRouter prefix."""
    app = request.app
    # Normalize base_url_str by removing any trailing slash for consistent comparison and construction
    base_url_str = str(request.base_url).rstrip("/")

    if not app.state.router_prefix:
        # If there's no router_prefix, just return the base_url (ensuring it has a trailing slash)
        return base_url_str + "/"
    else:
        # Normalize router_prefix to ensure it starts with a slash and has no trailing slash
        normalized_router_prefix = "/" + app.state.router_prefix.strip("/")

        # Check if the (already ROOT_PATH-inclusive) base_url_str ends with the normalized_router_prefix
        if base_url_str.endswith(normalized_router_prefix):
            # If it does, ROOT_PATH and router_prefix are likely the same or router_prefix is a suffix of ROOT_PATH.
            # In this case, the prefix is already effectively included.
            return base_url_str + "/"  # Just ensure a trailing slash
        else:
            # If not, append the normalized_router_prefix.
            # This handles cases where router_prefix is genuinely an additional path component.
            return base_url_str + normalized_router_prefix + "/"
