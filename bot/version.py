def get_version() -> str:
    """
    Returns the version details of Mirror Beast.

    :return: The version details in the format 'vMAJOR.MINOR.PATCH-STATE'
    :rtype: str
    """
    MAJOR = "1"
    MINOR = "0"
    PATCH = "1"
    STATE = "beast"
    return f"v{MAJOR}.{MINOR}.{PATCH}-{STATE}"


def get_changelog() -> str:
    """
    Returns the changelog for the current version.
    
    :return: The changelog text
    :rtype: str
    """
    return """
• Rebranded to Mirror Beast with improved UI
• Updated command trigger to 'beast'
• Added link to public leech group
• Improved error messages for non-authorized users
• Fixed various bugs from the base code
"""


if __name__ == "__main__":
    print(f"Mirror Beast {get_version()}")
    print("Changelog:")
    print(get_changelog())
