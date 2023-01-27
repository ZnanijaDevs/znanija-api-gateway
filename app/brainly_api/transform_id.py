import base64


def to_id(id_: int, prefix: str) -> str:
    """Encode to a GraphQL Base64 id"""
    encoded = base64.b64encode(
        bytes(f"{prefix}:{id_}", "utf-8")
    )

    return encoded.decode("utf-8")


def from_id(id_: str) -> int:
    """Decode a GraphQL Base64 id to int"""
    decoded = base64.b64decode(id_)

    decoded_id = decoded.decode("utf-8").split(":").pop()

    return int(decoded_id)
