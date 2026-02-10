from functions.get_files_info import get_files_info

# Manually test get_files_content_info with various valid and invalid inputs
print(get_files_info("calculator", "."))
print(get_files_info("calculator", "pkg"))
print(get_files_info("calculator", "/bin"))
print(get_files_info("calculator", "../"))
