class ContactGroupNotFound(RuntimeError):
    def __init__(self, group_name: str) -> None:
        self.group_name = group_name

    def __str__(self) -> str:
        return f"No Contact Group found for name: {self.group_name}"
