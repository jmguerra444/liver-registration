function image2dcm(filename_in, filename_out)
    image = imread(filename_in);
    dicomwrite(int16(image), filename_out)
end