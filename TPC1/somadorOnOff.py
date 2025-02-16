import sys

def main():
    total_sum, current_num = 0, 0
    is_summing = True
    activate_buffer = ""
    deactivate_buffer = ""
    
    for line in sys.stdin:
        for char in line:
            if char == "\n":
                continue
            
            activate_buffer = (activate_buffer + char).lower()[-2:]
            deactivate_buffer = (deactivate_buffer + char).lower()[-3:]
            
            if deactivate_buffer == "off":
                is_summing = False
            elif activate_buffer == "on":
                is_summing = True
            
            if char.isdigit() and is_summing:
                current_num = current_num * 10 + int(char)
            else:
                total_sum += current_num
                current_num = 0
            
            if char == "=":
                print(f">{total_sum}")
    
    print(f"Total is: {total_sum}")

if __name__ == "__main__":
    main()