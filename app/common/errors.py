class DomainError(Exception):
    """Бизнес-ошибка доменного слоя."""


class PermissionDenied(DomainError):
    pass


class NotFound(DomainError):
    pass
