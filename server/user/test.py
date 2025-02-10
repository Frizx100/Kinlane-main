# import hashlib

# myHash = 1

# hash_a = hashlib.sha224(str(myHash).encode())
# a = hash_a.hexdigest()
# print(hash_a.hexdigest())
# print(a)
# print(len(a))

# import os
# path = '"C:/Users/amd/Downloads/ZoomInstallerFull.exe"'
# file_extension = os.path.basename(path).split('.')[1][:-1]
# print(file_extension)

# path = 'static\\media'
# full_path = os.path.join(path, 'dawawd', 'jiluh')
# print(full_path)

# from time import localtime, strftime
# time = '30.02.2024.22.14.00'
# time = time[:10] + " " + time[11:13] + ":" + time[14:16] + ":" + time[17:] 
# print(time)


# print(strftime('%d.%m.%Y.%H.%M.%S', localtime()))