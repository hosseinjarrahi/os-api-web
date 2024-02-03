x = b'0239{"cmd":10,"resp":0,"pan":"603799**3144","rrn":"805227482139","terminal":"99028391","trace":"450674","serial":"000016","amount":"10000","settlement":"10000","discount":"0","data1":"BK003\xe3\xe1\xedDT012240203124712RL0011FP0012SP0011T9009236475393"}'
x = x.decode('latin-1')

# Convert the string to bytes
bytes_object = x.encode()

# Decode the bytes using 'utf-8' codec
decoded_string = bytes_object.decode('utf-8')

# Print the decoded string
print(decoded_string)