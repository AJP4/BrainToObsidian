from dataclasses import dataclass


@dataclass(frozen=True)
class ThoughtKind:
    """
    Types of thoughts.
    """

    THOUGHT: int = 1
    TYPE: int = 2
    TAG: int = 4
    FORGOTTEN: int = 99


@dataclass(frozen=True)
class ThoughtAccessType:
    """
    Access types for thoughts.
    """

    PUBLIC: int = 0
    PRIVATE: int = 1


@dataclass(frozen=True)
class LinkKind:
    """
    Types of links.
    """

    NORMAL_LINK: int = 1
    LINK_TYPE: int = 2


@dataclass(frozen=True)
class LinkMeaning:
    """
    Meaning of links.
    """

    NOTTHING: int = 0
    THOUGHT_TO_THOUGHT: int = 1
    TYPE_TO_THOUGHT: int = 2
    TYPE_TO_TYPE: int = 3
    TAG_TO_THOUGHT: int = 5
    TAGS_TO_TAGS: int = 7


@dataclass(frozen=True)
class LinkRelation:
    """
    Relationship types for links.
    """

    NO_VALUE: int = 0
    PARENT_TO_CHILD: int = 1
    PARENT: int = 2
    JUMP: int = 3
    SIBLING: int = 4


@dataclass(frozen=True)
class LinkDirection:
    """
    Direction of links.
    """

    DEFAULT: int = -1
    REVERSE: int = 3
    ONEWAY_NORMAL: int = 5
    ONEWAY_REVERSE: int = 7
    DIRECTIONAL_IN_NORMAL_DIRECTION: int = 9


@dataclass(frozen=True)
class AttachmentType:
    """
    Types of attachments.
    """

    INTERNAL_FILE: int = 1
    EXTERNAL_FILE: int = 2
    EXTERNAL_URL: int = 3
    NOTES_V9: int = 4
    ICON: int = 5
    NOTES_ASSET: int = 6
    INTERNAL_DIRECTORY: int = 7
    EXTERNAL_DIRECTORY: int = 8
    SUB_FILE: int = 9
    SUB_DIRECTORY: int = 10
    SAVED_REPORT: int = 11
    MARKDOWN_IMAGE: int = 12


@dataclass(frozen=True)
class AttachmentNoteType:
    """
    Types of notes.
    """

    ATTACHMENT: int = 0
    NOTES_MD: int = 4


@dataclass(frozen=True)
class AttachmentSourceType:
    """
    Source types for attachments.
    """

    WALLPAPER: int = 1
    ATTACHMENT: int = 2
