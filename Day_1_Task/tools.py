import ast
import operator
from config import COURSE_FEES


def get_course_fee(course_code):
    """Get the fee for one course."""
    course_code = course_code.strip().upper()

    fee = COURSE_FEES.get(course_code)

    if fee is None:
        return f"Unknown course code: {course_code}"

    return str(fee)


def get_all_courses():
    """Return all available courses and their fees."""
    return ", ".join(
        f"{course}: Rs. {fee}"
        for course, fee in COURSE_FEES.items()
    )


OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg
}


def evaluate(node):
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value

    if isinstance(node, ast.BinOp):
        operation = OPS.get(type(node.op))

        if operation is None:
            raise ValueError("Unsupported operation")

        return operation(
            evaluate(node.left),
            evaluate(node.right)
        )

    if isinstance(node, ast.UnaryOp):
        operation = OPS.get(type(node.op))

        if operation is None:
            raise ValueError("Unsupported operation")

        return operation(evaluate(node.operand))

    raise ValueError("Unsupported expression")


def calculator(expression):
    """Calculate basic arithmetic."""
    try:
        tree = ast.parse(expression, mode="eval")
        result = evaluate(tree.body)
        return str(result)

    except Exception as error:
        return f"Calculator error: {error}"


TOOL_FUNCTIONS = {
    "get_course_fee": get_course_fee,
    "get_all_courses": get_all_courses,
    "calculator": calculator
}


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_course_fee",
            "description": "Get the fee in rupees for one course code.",
            "parameters": {
                "type": "object",
                "properties": {
                    "course_code": {
                        "type": "string"
                    }
                },
                "required": ["course_code"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_all_courses",
            "description": "Get all available courses and their fees.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Calculate arithmetic expressions using +, -, *, / and brackets.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]


if __name__ == "__main__":
    print("AI202 fee:", get_course_fee("AI202"))
    print("All courses:", get_all_courses())
    print("Calculation:", calculator("(12000 + 18000) * 0.9"))