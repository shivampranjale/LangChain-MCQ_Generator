"""
Utility functions for the MCQ Generator.
"""


def print_header(text: str):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f" {text}")
    print("=" * 70 + "\n")


def print_section(text: str):
    """Print a formatted section title."""
    print(f"\n--- {text} ---\n")


def save_output(content: str, filename: str) -> None:
    """
    Save output to a file.

    Args:
        content (str): Content to save
        filename (str): Output filename
    """
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Output saved to {filename}")
