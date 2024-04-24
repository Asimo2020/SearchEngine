import os
import zipfile
# -----------------get_user_input-----------------
def get_user_input():
    """
    Get user input
    """
    user_input = input("Please enter your query: ").lower()
    return user_input


# -----------------extract_zip-----------------
def extract_zip(path):
    """
    Extracts a zip file to a new directory.
    """
    with zipfile.ZipFile(path, 'r') as zip_ref:
        new_path = os.path.splitext(path)[0]
        os.makedirs(new_path, exist_ok=True)  # Create the directory if it doesn't exist
        zip_ref.extractall(new_path)
        print(f"{zip_ref.filename} extracted to {new_path}.")
    return new_path


# -----------------search_for_query-----------------
def search_for_query_in_file(file_path, user_query, context_words=2):
    """
    Searches for user query in a file and returns the number of matches and other information.
    """
    results = []
    with open(file_path, "r", encoding='UTF-8') as f:
        contents = f.read()
        lines = contents.split('\n')
        for line_num, line in enumerate(lines, 1):
            line_lower = line.lower()
            if user_query in line_lower:
                start_index = line_lower.index(user_query)
                end_index = start_index + len(user_query)
                before_query = line[start_index - (context_words * 20):start_index].strip().split()[-2:]
                after_query = line[end_index:end_index + (context_words * 20)].strip().split()[:2]
                results.append({
                    "file_name": os.path.basename(file_path),
                    "file_path": file_path,
                    "matches": contents.lower().count(user_query),
                    "line_number": line_num,
                    "before_query": ' '.join(before_query),
                    "after_query": ' '.join(after_query)
                })
    return results


def search_for_query_in_folder(path, user_query):
    """
    Searches for user query in all txt files in a folder and its subfolders.
    """
    results = []
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.splitext(file_path)[1] == ".txt":
                results.extend(search_for_query_in_file(file_path, user_query))
    return results


def search_for_query(path, user_query):
    """
    Searches for user query in a file, a folder, or a zip file.
    """
    if not os.path.exists(path):
        print('Path not found.')
        return []
    elif os.path.isdir(path):  # path is a folder
        results = search_for_query_in_folder(path, user_query)
    elif os.path.splitext(path)[1] == ".zip":
        new_path = extract_zip(path)
        results = search_for_query_in_folder(new_path, user_query)
    elif os.path.splitext(path)[1] == ".txt":
        results = search_for_query_in_file(path, user_query)
    else:
        print("Path not valid.")
        return []
    return results


# -----------------show_results-----------------
def show_results(results):
    """
    Prints the search results.
    """
    if not results:
        print("No results found.")
        return
    sorted_results = sorted(results, key=lambda x: x['matches'],reverse=True)
    header = ['File Name','matches', 'Line Number', 'Before Query', 'After Query']
    format_str = "{:<30} {:<15} {:<15} {:<30} {:<30}"
    print(format_str.format(*header))
    print("-" * 110)
    for result in sorted_results:
        file_name = result['file_name']
        matches = result['matches']
        line_number = result['line_number']
        before_query = result['before_query']
        after_query = result['after_query']
        print(format_str.format(file_name,matches, line_number, before_query, after_query))
    print("-" * 110)
    print("Total matches found:", len(results))


# -----------------main-----------------
if __name__ == "__main__":
    path = input("Please enter the path: ")
    user_query = get_user_input()
    results = search_for_query(path, user_query)
    show_results(results)
