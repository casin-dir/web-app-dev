my_arr = [1, 2, 3, -10, 0, 35, 47, 0, 9];

def min_in_arr(arr):
    min = arr[0]
    for num in arr:
        if num < min:
            min = num
    return min

def average_in_arr(arr):
    sum = 0;
    for num in arr:
        sum+=num
    return sum/len(arr)

if __name__ == "__main__":
    print('min_in_arr:', min_in_arr(my_arr))
    print('average_in_arr:', average_in_arr(my_arr))
