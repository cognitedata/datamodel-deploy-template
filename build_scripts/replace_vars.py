import argparse
import os


def parse_args():
    parser = argparse.ArgumentParser(description="Upload graphql datamodels to CDF")
    parser.add_argument(
        "--file", required=False,
        type=str)
    parser.add_argument(
        "--path", required=False,
        type=str)
    parser.add_argument(
        "--information-space", required=True,
        type=str)
    parser.add_argument(
        "--solution-space", required=True,
        type=str)
    return parser.parse_args()


def process_file(filename,  information_space: str, solution_space: str):
    with open(filename, 'r') as file :
        filedata = file.read()
    
    newdata = filedata.replace("<INFORMATION_SPACE>", information_space)
    newdata = newdata.replace("<PUMP_SOLUTION_SPACE>", solution_space)

    if filedata != newdata:
        print(f"Updated {filename}")
        with open(filename, 'w') as file:
            file.write(newdata)
    else:
        print(f"No updates for {filename}")


def main():
    args = parse_args()

    if args.path:
        for (dir_path, dir_names, file_names) in os.walk(args.path):
            for file in file_names:
                process_file(filename=f"{dir_path}/{file}", information_space=args.information_space, solution_space=args.solution_space)
    elif args.file:
                    process_file(filename=args.file, information_space=args.information_space, solution_space=args.solution_space)
    else:
        print("--path or --file required")


if __name__ == "__main__":
    main()
