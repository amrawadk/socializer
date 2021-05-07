# pylint: disable=super-init-not-called
# TODO I don't think the super call is needed here, but should confirm.
class ContactGroupNotFound(RuntimeError):
    def __init__(self, group_name: str) -> None:
        self.group_name = group_name

    def __str__(self) -> str:
        return f"No Contact Group found for name: {self.group_name}"
