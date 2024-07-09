def process_txt(input_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    grouped_data = {}
    flag = 1
    init_value = 1000

    # Group data based on the first value in each line
    for line in lines:
        values = line.split()
        if values:
            if flag:
                init_value = int(values[0])
                flag = 0
            first_value = int(values[0])
            group_number = (first_value - init_value) // 80000
            if group_number not in grouped_data:
                grouped_data[group_number] = []
            grouped_data[group_number].append(line)

    # Create and save files for each group
    for group_number, data_lines in grouped_data.items():
        output_file = input_file.replace('/gs.txt', f"/ev_rs_{(group_number+1):03d}.txt")
        with open(output_file, 'w') as file:
            for line in data_lines:
                values = line.split()
                if values:
                    values[0] = str(int(values[0]) * 1000)  # Multiply the first value by 1000
                    new_line = ' '.join(values)
                    file.write(new_line + '\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='event path')
    parser.add_argument('--folder_path', '-path', type=str, default="./chair_blink", help='folder path.')

    args = parser.parse_args()
    input_file_path = args.folder_path + '/gs.txt'
    process_txt(input_file_path)
