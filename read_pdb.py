def read_line(file_name):
    DBREF_COUNT = 0
    DBREF_INF_LIST = []
    result = {}
    for line in file_name:
        if line.startswith("DBREF"):
            DBREF_COUNT += 1
            if "INS_HUMAN" in line:
                DBREF_INF_LIST.append(line[12:14].strip())
        if line.startswith("ATOM") and line[21:32].strip() in DBREF_INF_LIST:


            result[line[21:32].strip()] =


