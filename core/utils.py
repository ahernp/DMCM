from subprocess import Popen, PIPE

from django.db import models
from django.contrib.postgres.search import Value, Func


def run_shell_command(command, cwd):
    p = Popen(command, shell=True, cwd=cwd, stdout=PIPE)
    stdout = p.communicate()[0]
    if stdout:
        stdout = str(stdout.strip(), "utf-8")
    return stdout


class Headline(Func):
    """ Show postgresql text search matches in context """

    function = "ts_headline"

    def __init__(self, field, query, config=None, options=None, **extra):
        expressions = [field, query]
        if config:
            expressions.insert(0, Value(config))
        if options:
            expressions.append(Value(options))
        extra.setdefault("output_field", models.TextField())
        super().__init__(*expressions, **extra)


def highlight_matching_substring(string, substring, delimiter="b", max_length=100):
    delimiters_length = len(f"<{delimiter}></{delimiter}>")
    lowercase_string = string.casefold()
    lowercase_substring = substring.casefold()
    substring_position = lowercase_string.find(lowercase_substring)

    if substring_position < 0:
        return f"{string[:max_length]}..." if len(string) > max_length else string

    if (substring_position + len(substring) + delimiters_length) > max_length:
        previous_newline_position = lowercase_string.rfind("\n", 0, substring_position)
        if (
            previous_newline_position > -1
            and (substring_position - previous_newline_position) < max_length
        ):
            string = string[previous_newline_position + 1 :]
        else:
            previous_space_position = lowercase_string.rfind(" ", 0, substring_position)
            if (
                previous_space_position > -1
                and (substring_position - previous_space_position) < max_length
            ):
                string = string[previous_space_position + 1 :]
            else:
                string = string[substring_position:]
        lowercase_string = string.casefold()
        substring_position = lowercase_string.find(lowercase_substring)

    substring_end = substring_position + len(substring)
    highlighted_string = (
        f"{string[:substring_position]}<{delimiter}>{string[substring_position:substring_end]}</{delimiter}>{string[substring_end:]}"
    )

    if len(highlighted_string) > (max_length + delimiters_length):
        return f"{highlighted_string[:max_length + delimiters_length]}..."
    return highlighted_string
