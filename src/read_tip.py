import textwrap
import shutil


def snip(file_name: str) -> str:
    
    if not isinstance(file_name, str):

        raise TypeError("File name must be string.")

    try:

        with open(file_name, "r") as file:

            snippet = []

            caption = ""

            tip_num = int(file.readline().strip("pos: "))

            tip_count = 0

            it = iter(file)

            for line in it:

                if line.rstrip() == "***":
                    tip_count += 1

                if tip_count == tip_num and line.rstrip() != "***":

                    sub_strs = (lambda z: [
                                x + "\n" for x in textwrap.fill(z, 62).split("\n")] if len(z) > 82 else z)(line)

                    if line.startswith("$Cap$"):

                        caption = line.strip("$Cap$")
                              
                    elif isinstance(sub_strs, list) and sub_strs[0].startswith("#"):

                        for i in sub_strs:

                            if i.startswith("#"):

                                snippet.append(i)

                            else:

                                snippet.append("#"+i)

                    elif isinstance(sub_strs, list):

                        for i in sub_strs:

                            snippet.append(i)

                    else:

                        snippet.append(line)
            
            
            incr_pos(file_name)

            return [caption, ''.join(snippet)]

    except FileNotFoundError:
        
        print("File does not exist")



def incr_pos(file_name: str):


    with open(file_name, "r+") as file:

        line = next(file)

        position = int(line.strip("pos: ").rstrip())

        print(position)

        position += 1

        file.seek(0)

        file.write(line.replace(line, f"pos: {str(position).zfill(32)}"))
