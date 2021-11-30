from typing import Tuple

import click
from click.core import ParameterSource


class RangeInputOption(click.Option):
    """
    Handle a range of integers

    Accepts a csv of numbers (1,2,6) or a range (1-6).
    """

    def consume_value(self, ctx, opts) -> Tuple[set, ParameterSource]:

        highlight_exception_base = "Invalid value!"
        value, source = super().consume_value(ctx, opts)

        if not value:
            return value, source

        try:

            if "-" in value:
                input_list = value.split("-")

                if len(input_list) > 2:
                    raise click.ClickException(
                        f"{highlight_exception_base} Could not convert {value} to a valid range."
                    )

                input_list = list(map(int, input_list))

                if input_list[0] > input_list[1]:
                    raise click.ClickException(
                        f"{highlight_exception_base} {input_list[0]} is greater than {input_list[1]}."
                    )

                value = list(range(input_list[0], input_list[1] + 1))

                if len(value) == 0:
                    value = input_list[0]

            else:
                value = list(map(int, value.split(",")))

        except ValueError as e:
            raise click.ClickException(
                f"{highlight_exception_base} {e} is not a valid integer range."
            )

        return value, source
