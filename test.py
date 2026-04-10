import argparse


parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

def main():
    if args.verbose:
        print(args.user_prompt)

if __name__ == "__main__":
    main()