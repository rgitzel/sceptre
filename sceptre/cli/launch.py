import click

from sceptre.cli.helpers import catch_exceptions, get_stack_or_stack_group
from sceptre.cli.helpers import confirmation
from sceptre.stack_status import StackStatus
from sceptre.plan.plan import SceptrePlan


@click.command(name="launch")
@click.argument("path")
@click.option(
    "-y", "--yes", is_flag=True, help="Assume yes to all questions."
)
@click.pass_context
@catch_exceptions
def launch_command(ctx, path, yes):
    """
    Launch a stack or stack_group.

    Launch a stack or stack_group for a given config PATH.
    """
    action = "launch"

    stack, stack_group = get_stack_or_stack_group(ctx, path)
    if stack:
        confirmation(action, yes, stack=path)
        plan = SceptrePlan(path, action, stack)
        response = plan.execute()
        if response != StackStatus.COMPLETE:
            exit(1)
    elif stack_group:
        confirmation(action, yes, stack_group=path)
        plan = SceptrePlan(path, action, stack_group)
        response = plan.execute()
        if not all(
            status == StackStatus.COMPLETE for status in response.values()
        ):
            exit(1)
