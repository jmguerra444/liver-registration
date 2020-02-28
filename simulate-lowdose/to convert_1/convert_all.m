file_list = dir('*.tif');

for i = 1 : length(file_list)
    name_in = file_list(i).name;
    name_out = name_in + ".dcm";
    image2dcm(name_in, name_out)
end