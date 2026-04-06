import ast


def print_ast(expr: str) -> None:
	tree = ast.parse(expr, mode="eval")
	print(f"Expression: {expr}")
	print(ast.dump(tree, indent=2, include_attributes=False))
	print()


def main() -> None:
	print_ast("not x")
	print_ast("a and b and c")
	print_ast("a and b or c")
	print_ast("a and not b")
	print_ast("y < 3")


if __name__ == "__main__":
	main()
