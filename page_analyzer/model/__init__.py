from . import db, urls, checks, analyzer  # noqa: F401


class ModelError(Exception):
    pass


class UrlCheckError(ModelError):
    pass


class DbConnecionError(ModelError):
    pass


class IncorrectUrlName(ModelError):
    pass


class UrlAlreadyExists(ModelError):
    pass


class DbConsistanceError(ModelError):
    pass


class UrlIdIsNone(DbConsistanceError):
    pass


class UrlIdNotFound(DbConsistanceError):
    pass
