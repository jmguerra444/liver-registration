% This script just removes metadata from dicom file

[vol, info] = dcmread('ct_re');
try
    rmdir('ct_fixed');
    disp("Folder removed");
catch
    disp("Nothing removed");
end
mkdir('ct_fixed');
writedcm(vol, 'ct_fixed');


function fixtags()
    
end