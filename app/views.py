"""
File containing all of the flak endpoints, in charge of handling
user requests for managing documents a sections
"""
from flask import request
from werkzeug.exceptions import BadRequest, UnprocessableEntity

from app import app
from app.models import CreateDocumentSectionSchema, documents_dict

create_document_section_schema = CreateDocumentSectionSchema()


@app.route("/document", methods=["GET", "POST"])
def handle_document_request():

    if request.method == 'GET':
        path = request.args.get("section", default="", type=str)
        return get_document_section(path)


def get_document_section(path):
    """
    This endpoint handles the requests for consulting a document, or a
    section from a document, according to a specified path.

    Args:
        path (str): Query parameter from the request being processed

    Raises:
        BadRequest: If the request is missing the path

    Returns:
        Response: Document or section that matches the path
    """
    if path:
        section = _get_section_from_path(path, strict=True)
        return section, 200
    else:
        raise BadRequest("Missing required parameter(s): 'section'")


def _add_section_to_document(path, name, text):

    section = dict(name=name, text=text, sections=[])
    parent_section = _get_section_from_path(path)

    if parent_section:
        current_subsection = _get_subsection_from_path(
            parent_section, [name], strict=False
        )
        if current_subsection:
            raise UnprocessableEntity(
                f"The section '{path}.{name}' already exists"
            )
        else:
            parent_section["sections"].append(section)
    elif "." not in path:
        documents_dict[path] = dict(
            name=path, text="", sections=[section]
        )
    else:
        raise UnprocessableEntity(
            f"Unable to create section with path '{path}'"
        )

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
