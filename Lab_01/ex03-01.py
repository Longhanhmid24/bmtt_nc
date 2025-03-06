def tinh_tong_chan(lst):
    tong =0
    for num in lst:
        if num % 2 == 0:
            tong += num
    return tong

input_lst = input ("Nhập danh sách các số, cách nhau bằng dấy phẩy: ")
numbers = list(map(int, input_lst.split(',')))

tong_chan = tinh_tong_chan(numbers)
print(f"Tổng các số chẵn trong danh sách là: {tong_chan}")