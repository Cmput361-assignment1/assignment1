import subprocess

collections = ["good", "bad1", "bad2", "bad3", "bad4", "bad5", "bad6"]



for collection in collections:
    try:
        output = subprocess.check_output(["python3", "./code/read_answers.py", collection], stderr=subprocess.STDOUT, text=True)
        print(f"{collection} NO ERROR")
    except subprocess.CalledProcessError as e:
        error_message = e.output.strip().split("\n")[-1]  # Capture last error line
        print(error_message)


