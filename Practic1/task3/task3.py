from statistics import mean

def read_file():
    with open('third_task.txt', encoding="utf-8") as file:
        return file.readlines()

def processing_lines(lines):
    resultsArray = []
    for line in lines:
        numberArray = line.strip().split(' ')
        for i, number in enumerate(numberArray):
            if number == 'N/A':
                numberArray[i] = mean([int(numberArray[i - 1]), int(numberArray[i + 1])])
        resultsArray.append(mean([int(i) for i in numberArray if int(i) % 5 == 0]))

    return resultsArray

def write_result_to_file(resultArray):
    with open('third_task_result.txt', 'w', encoding="utf-8") as file:
        for number in resultArray:
            file.write(str(number) + "\n")

print(processing_lines(read_file()))
write_result_to_file(processing_lines(read_file()))