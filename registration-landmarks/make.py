import os

mri_pats = [
    6,
    7,
    8,
    10,
    11,
    13,
    20,
    21,
    22,
    23,
    25,
    26,
    28,
    30,
    34,
    36,
    37,
    40,
    41,
    42,
    44,
    46,
    49,
    50,
    55,
    56,
    62,
    66,
    67,
    69,
    70,
    71,
    74,
    75,
    78,
    79,
    80,
    81,
    82,
    83,
    86,
    88,
    90,
    91,
    92,
    93,
    94,
    95,
    96,
    97,
    98,
    99,
    100,
    102,
    103
]


for i in mri_pats:
    name = "{:03d}".format(i)
    os.mkdir(name)
    # os.chdir(name)
    # # os.mkdir("mr")
    # # os.mkdir("lowdose")
    # # os.mkdir("diag")
    # os.chdir("..")
    print(name)


print(os.getcwd())