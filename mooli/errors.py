"""Contains all mooli exceptions."""


class MooliError(Exception):
    pass


class ProviderError(MooliError):
    pass


class ProviderNotFound(ProviderError):
    pass


class MultipleProvidersFound(ProviderError):
    pass
