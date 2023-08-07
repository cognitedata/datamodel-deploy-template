import argparse
import json
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
        "--space", required=True,
        type=str)
    parser.add_argument(
        "--version", required=True,
        type=str)
    parser.add_argument(
        "--model-external-id", required=True,
        type=str)
    return parser.parse_args()


def process_file(filename, space, version, model_id):
    with open(filename, 'r') as file :
        filedata = file.read()
    
    newdata = filedata.replace('$SPACE', space)
    newdata = newdata.replace('$VERSION', version)
    newdata = newdata.replace('$MODEL_EXTERNAL_ID', model_id)
    

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
                process_file(filename=f"{dir_path}/{file}", space=args.space, version=args.version, model_id=args.model_external_id)
    elif args.file:
                    process_file(filename=args.file, space=args.space, version=args.version, model_id=args.model_external_id)
    else:
        print("--path or --file required")

if __name__ == "__main__":
    main()
