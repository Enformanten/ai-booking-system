from typing import Any

from prettytable import PrettyTable


def prettyparams(params: dict[str, Any]) -> PrettyTable:
    table = PrettyTable(field_names=("Parameter", "Value"))
    table.add_rows(params.items())
    return table
