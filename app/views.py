"""
File containing all of the flak endpoints, in charge of handling
user requests for managing documents a sections
"""

from werkzeug.exceptions import BadRequest, UnprocessableEntity
from app.models import documents_dict

def _get_section_from_path(path, strict=False):
    """
    This function returns a section from one of the stored documents
    that matches the path given byu parameter.

    Args:
        path (str): The path given for searching the desired section

    Raises:
        UnprocessableEntity: If path is not found and on strict mode

    Returns:
        dict: The document section corersponding to the given path
    """
    section_paths = path.split(".")
    if not all(section_paths):
        raise BadRequest("The path cannot have dots (.) together or at the end")

    root_path = section_paths.pop(0)
    document_root = documents_dict.get(root_path, {})
    if document_root:
        return _get_subsection_from_path(document_root, section_paths, strict=strict)
    else:
        if strict:
            raise UnprocessableEntity(
                f"Unable to find a document with the name: {root_path}"
            )
        return document_root


def _get_subsection_from_path(document_root: dict, section_paths: list, strict: bool = False):
    """
    This function gets the corresponding document subsection of a given
    path sequence.

    Args:
        document_root (dict): The document in which the search will take place
        section_paths (list[str]): The path as a sequence of section names 

    Raises:
        UnprocessableEntity: If the path is not found and on strict mode

    Returns:
        dict: The document section corresponding to the sequence path
    """
    current_root, path = document_root, None
    while section_paths:
        path = section_paths.pop(0)
        for section in current_root["sections"]:
            if section["name"] == path:
                current_root = section
                # path = section_paths.pop(0) if section_paths else None
                break
        else:
            if strict:
                raise UnprocessableEntity(
                    f"'{path}' not found on {current_root['name']} section"
                )
            current_root = {}
            break

    return current_root