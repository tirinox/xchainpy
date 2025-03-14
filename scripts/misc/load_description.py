def load_description():
    """
    In setup call you do:
    long_description=load_description(),
    long_description_content_type="text/markdown",
    :return: text
    """
    from pathlib import Path
    this_directory = Path(__file__).parent
    long_description = (this_directory / "README.md").read_text()
    return long_description
