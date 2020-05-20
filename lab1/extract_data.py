import os
import sys

def main(folder):
    files = os.listdir(folder)
    with open ("relazione/sezioni/conclusioni.tex", 'a') as f:
        mst = ""
        time = []
        for file_name in files:
            if "time" in file_name:
                with open(folder + "/" + file_name, 'r') as f2:
                    for line in f2.readlines():
                        line=line.strip()
                        if line:
                            line=line.split(":")
                            time.append(str(round(float(line[1]),6)))
                f.write("\hline \r")
                graf = file_name.replace(".txt", "")
                f.write(graf + " & " + mst + " & " + time[0] + " & " + time[1] + " & " + time[2] + " \\ \r")

            elif "output_random" in file_name:
                with open(folder + "/" + file_name, 'r') as f2:
                    mst=f2.readline()



if __name__ == "__main__":
    main("mst-dataset")


