import os
import re

core_folder = "byte-of-python"

result = open("dataset.txt", "w", encoding="UTF8")


files = [file for file in os.listdir(core_folder) if file[-3:] == ".md"]

for file in files:
    print(file)
    with open(os.path.join(core_folder, file), "rt", encoding="UTF8") as f:
        current_text = f.read()
        # remove *
        # remove #        
    current_text = re.sub("\#+ +(.+?)\\n", "\g<1>!", current_text)
    current_text = current_text.replace("*", "")     
    
    # delete []()
    current_text = re.sub("\[.+?\]\(.+?\)", "", current_text)
    # remove all between <pre> </pre>
    current_text = re.sub("\<pre\>.+?\<\/pre\>", "", current_text)
    current_text = current_text.replace(".\n", ". ")
    current_text = current_text.replace("\n", "")
    
    current_text = re.sub("\`\`\`.+?\`\`\`", "", current_text)
    
    current_lines = re.split("[\.\!\?]\s", current_text)
    result.write("\n".join(current_lines))
        
result.close()

        
