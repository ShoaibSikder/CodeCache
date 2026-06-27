"""
Constants used across the CodeCache platform.
"""

# User Roles
class UserRole:
    SUPER_ADMIN = 'super_admin'
    ADMIN = 'admin'
    EDITOR = 'editor'
    USER = 'user'

    CHOICES = [
        (SUPER_ADMIN, 'Super Admin'),
        (ADMIN, 'Admin'),
        (EDITOR, 'Editor'),
        (USER, 'User'),
    ]


# Content Item Types
class ContentType:
    HEADING = 'heading'
    PARAGRAPH = 'paragraph'
    CODE = 'code'
    TABLE = 'table'
    NOTE = 'note'
    WARNING = 'warning'
    TIP = 'tip'
    IMAGE = 'image'
    OUTPUT = 'output'
    DIVIDER = 'divider'

    # Future types
    QUIZ = 'quiz'
    MCQ = 'mcq'
    ROADMAP = 'roadmap'
    VIDEO = 'video'
    DOWNLOAD = 'download'

    CHOICES = [
        (HEADING, 'Heading'),
        (PARAGRAPH, 'Paragraph'),
        (CODE, 'Code'),
        (TABLE, 'Table'),
        (NOTE, 'Note'),
        (WARNING, 'Warning'),
        (TIP, 'Tip'),
        (IMAGE, 'Image'),
        (OUTPUT, 'Output'),
        (DIVIDER, 'Divider'),
    ]

    FUTURE_CHOICES = [
        (QUIZ, 'Quiz'),
        (MCQ, 'MCQ'),
        (ROADMAP, 'Roadmap'),
        (VIDEO, 'Video'),
        (DOWNLOAD, 'Download'),
    ]

    ALL_CHOICES = CHOICES + FUTURE_CHOICES


# Entity Status
class Status:
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    DRAFT = 'draft'
    ARCHIVED = 'archived'

    CHOICES = [
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
        (DRAFT, 'Draft'),
        (ARCHIVED, 'Archived'),
    ]


# Permission Actions
class PermissionAction:
    ADD_LANGUAGE = 'add_language'
    EDIT_LANGUAGE = 'edit_language'
    DELETE_LANGUAGE = 'delete_language'
    MANAGE_USERS = 'manage_users'
    MANAGE_CONTENT = 'manage_content'
    VIEW_ANALYTICS = 'view_analytics'


# Permission Matrix
PERMISSION_MATRIX = {
    UserRole.SUPER_ADMIN: [
        PermissionAction.ADD_LANGUAGE,
        PermissionAction.EDIT_LANGUAGE,
        PermissionAction.DELETE_LANGUAGE,
        PermissionAction.MANAGE_USERS,
        PermissionAction.MANAGE_CONTENT,
        PermissionAction.VIEW_ANALYTICS,
    ],
    UserRole.ADMIN: [
        PermissionAction.ADD_LANGUAGE,
        PermissionAction.EDIT_LANGUAGE,
        PermissionAction.DELETE_LANGUAGE,
        PermissionAction.MANAGE_CONTENT,
        PermissionAction.VIEW_ANALYTICS,
    ],
    UserRole.EDITOR: [
        PermissionAction.EDIT_LANGUAGE,
        PermissionAction.MANAGE_CONTENT,
    ],
    UserRole.USER: [],
}


# Pagination
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100


# Search Settings
SEARCH_MIN_QUERY_LENGTH = 2
SEARCH_MAX_RESULTS = 50
