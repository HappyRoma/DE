def read_file():
    with open('second_task.txt', encoding="utf-8") as file:
        return file.readlines()

def sum_lines(lines):
    resultsArray = []
    for line in lines:
        numberArray = line.strip().split(" ")
        sum = 0
        for number in numberArray:
            if int(number) < 0:
                sum += int(number)
        resultsArray.append(abs(sum))

    return resultsArray

def write_result_to_file(resultArray):
    with open('second_task_result.txt', 'w', encoding="utf-8") as file:
        for number in resultArray:
            file.write(str(number) + "\n")
        file.write(f"\n{sum(resultArray)}")


print(sum_lines(read_file()))
write_result_to_file(sum_lines(read_file()))

