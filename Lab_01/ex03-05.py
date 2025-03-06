def dem_so_xuat_hien(lst):
    count = {}
    for num in lst:
        if num in count:
            count[num] += 1
        else:
            count[num] = 1
    return count
intput_lst = input("Nhập danh sách các từ, cách nhau bằng dấu : ")

word_list = intput_lst.split()

so_lan_xuat_hien = dem_so_xuat_hien(word_list)
print("Số lần xuất hiện của mỗi từ: ", so_lan_xuat_hien)