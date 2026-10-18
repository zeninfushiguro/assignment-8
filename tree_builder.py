class EmployeeNode:
    '''
    A class to represent a node in the binary tree.
    Attributes:
        name (str): The name of the employee.
        left (EmployeeNode): The left child node, representing the left subordinate.
        right (EmployeeNode): The right child node, representing the right subordinate.
    '''

    def __init__(self, name):
        self.name = name
        self.left = None
        self.right = None


class TeamTree:
    '''
    A class to represent a binary tree for managing a team structure.
    Attributes:
        root (EmployeeNode): The root node of the tree, representing the team lead.
    Methods:
        insert(manager_name, employee_name, side, current_node=None): Inserts a new employee under the specified manager.
        print_tree(node=None, level=0): Prints the tree structure starting from the given node.

    '''

    def __init__(self):
        self.root = None

    def insert(self, manager_name, employee_name, side, current_node=None):
        # A call with no current_node is the top-level call (not a recursive one)
        is_top_level = current_node is None
        if is_top_level:
            current_node = self.root
            if current_node is None:
                print("❌ The tree is empty. Add a team lead first.")
                return False

        if side not in ("left", "right"):
            print("❌ Side must be 'left' or 'right'.")
            return False

        if current_node.name == manager_name:
            if getattr(current_node, side) is not None:
                print(f"❌ The {side.upper()} side of {manager_name} is already taken.")
                return False
            setattr(current_node, side, EmployeeNode(employee_name))
            print(f"✅ {employee_name} added to the {side.upper()} of {manager_name}")
            return True

        # Not the manager: search each subtree that exists
        for child in (current_node.left, current_node.right):
            if child is not None and self.insert(manager_name, employee_name, side, child):
                return True

        if is_top_level:
            print(f"❌ Manager '{manager_name}' was not found.")
        return False

    def print_tree(self, node=None, level=0):
        if node is None:
            if level == 0:
                node = self.root
                if node is None:
                    print("The tree is empty.")
                    return
            else:
                return

        print("  " * level + "- " + node.name)
        self.print_tree(node.left, level + 1)
        self.print_tree(node.right, level + 1)


# Test your code here
# (run company_directory() below to test through the CLI)


# CLI functionality
def company_directory():
    tree = TeamTree()

    while True:
        print("\n📋 Team Management Menu")
        print("1. Add Team Lead (root)")
        print("2. Add Employee")
        print("3. Print Team Structure")
        print("4. Exit")
        choice = input("Choose an option (1–4): ")

        if choice == "1":
            if tree.root:
                print("⚠️ Team lead already exists.")
            else:
                name = input("Enter team lead's name: ")
                tree.root = EmployeeNode(name)
                print(f"✅ {name} added as the team lead.")

        elif choice == "2":
            manager = input("Enter the manager's name: ")
            employee = input("Enter the new employee's name: ")
            side = input("Should this employee be on the LEFT or RIGHT of the manager? ")
            side = side.lower()
            tree.insert(manager, employee, side)

        elif choice == "3":
            print("\n🌳  Current Team Structure:")
            tree.print_tree()

        elif choice == "4":
            print("Good Bye!")
            break
        else:
            print("❌ Invalid option. Try again.")

# DESIGN MEMO
#
# Recursive insertion works by treating every node as the root of its own smaller
# tree. insert() starts at the team lead and checks whether the current node's
# name matches the manager we want. If it does, the method checks whether the
# requested side is empty and, if so, attaches a new EmployeeNode there. If the
# name does not match, the method calls itself on the left child and then the
# right child, so the search keeps going down the structure until it either finds
# the manager or runs out of nodes. Each call only handles one employee and
# trusts the recursive calls to handle the rest.
#
# The hardest part was knowing when a search had failed. A recursive call on one
# branch can come back without finding the manager even though the manager lives
# in the other branch, so I could not print a "not found" error inside every
# call. I solved this by having insert() return True or False, and only printing
# the "manager not found" message from the top-level call after both branches
# were searched. I also had to avoid calling insert() on a child that was None,
# which would have crashed, and to make sure the default current_node=None meant
# "start at the root" only on the first call. Validating the side and refusing to
# overwrite an occupied side were smaller but important cases.
#
# Trees are preferable when data is naturally hierarchical or when fast search
# matters: file systems, HTML page structure, org charts, and category menus all
# nest this way. Balanced search trees and database indexes also use trees
# because they let you find, add, or remove items in logarithmic time instead of
# scanning a whole list.