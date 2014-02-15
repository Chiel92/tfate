"Module containing ActionWin class."""
import curses
from .win import Win


class ActionWin(Win):
    """Window containing the actiontree."""

    def __init__(self, width, height, x, y, session):
        Win.__init__(self, width, height, x, y, session)

    def draw(self):
        """Draw the current actiontree.
        It should look like this, where X is the current position:
        o-o-o-o-o-X-o-o-o
            |     | ↳ o-o-o-o-o
            |     ↳ o-o-o
            ↳ o-o-o
                ↳ o-o-o
        """
        actiontree = self.session.actiontree
        # We only have to print height/2 children branches
        # and parents branches, and width/2 children and parents

        # So first traverse upwards until exceed height or width
        upperbound = traverse_up(actiontree.current_node,
                                int((self.height - 1) * 2 / 3),
                                int((self.width - 1) * 2 / 3))
        # Then print tree downwards until exceed height or width
        string = '\n'.join(dump(upperbound, actiontree.current_node,
                                self.height, self.width))

        self.draw_line('History', curses.color_pair(17))

        #lines = [', '.join([str((i, j)) for j in range(100)]) for i in range(100)]
        #string = '\n'.join(lines)
        #string = self.crop(string, 3910)

        center = string.find('X')
        string = self.crop(string, center)
        self.draw_string(string)


def traverse_up(node, height, width):
    """Traverse upwards until exceed height or width."""
    parent = node.parent
    if not parent:# or height <= 0 or width <= 0:
        return node
    else:
        return traverse_up(parent, height - len(parent.children) + 1, width - 2)


def dump(node, current_node, height, width):
    """
    Return an array with the pretty printed lines of children
    of node, until we exceed height or width.
    """
    me = 'X' if node is current_node else 'o'

    if not node.children:  # or height <= 0 or width <= 0:
        return [me]

    result = []
    height -= 1
    for i, child in enumerate(node.children):
        child_dump = dump(child, current_node, height, width - 2)
        height -= len(child_dump)
        last_child = '|' if i < len(node.children) - 1 else ' '

        if i == 0:
            for j, line in enumerate(child_dump):
                if j == 0:
                    child_dump[j] = me + '-' + line
                else:
                    child_dump[j] = last_child + ' ' + line
        else:
            for j, line in enumerate(child_dump):
                if j == 0:
                    child_dump[j] = '↳ ' + line
                else:
                    child_dump[j] = last_child + ' ' + line

        result.extend(child_dump)
    return result
