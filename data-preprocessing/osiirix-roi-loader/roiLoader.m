%% Define Settings
thisComputer = getenv('COMPUTERNAME');

settings.loadRad320Images = true;
settings.loadMedicalDecathlonImages = false;

% For RAD320 dataset
settings.datasetsNames = {'01', '08', '09', '11', '12', '15', '15-2', '16', '16-2', '17', '17-2', '18', '18-2'};


if (thisComputer == 'JORGEGUERRA')
    settings.xmlOrigin = 'G:/master-thesis-data/selected-rad320-data/xml-regions';
    settings.dcmOrigin = 'G:/master-thesis-data/selected-rad320-data/dcm-volumes';
    settings.matDestination = 'G:/master-thesis-data/selected-rad320-data/mat-result';
end

%% RAD320 dataset

for i = 1:length(settings.datasetsNames)
    disp(strcat(num2str(i), '/',  num2str(length(settings.datasetsNames))));
    
    xmlName = strcat(settings.xmlOrigin, '/',  settings.datasetsNames{i}, '.xml');
    dcmPath = strcat(settings.dcmOrigin, '/',  settings.datasetsNames{i});
    matDestination= strcat(settings.matDestination, '/', settings.datasetsNames{i}, '.mat');
    
    mask = read_xml_roi(xmlName,dcmPath);   
    save(matDestination, 'mask');
end


%% Function repository
function [mask,vol] = read_xml_roi(fname,dcmpath)

    addpath(genpath('../slice-viewer'))
    vol =  load_dcm(dcmpath);
    xml = loadXMLPlist(fname);
    
    labels = [];
    for i = 1:size(xml.Images, 2)
         for j = 1:xml.Images{1, i}.NumberOfROIs
            my_label = xml.Images{1, i}.ROIs{1, j}.Name;
            labels = [labels; my_label];
         end
    end

    labels = unique(labels);
    for i=1:length(labels); disp(labels(i) + " is labeled with " + num2str(i*50)); end
    logical_masks = zeros(size(vol, 1), size(vol, 2), size(vol, 3), length(labels), 'logical');

    for i=1:size(xml.Images, 2)
            image_index = 1 + xml.Images{1, i}.ImageIndex;
         for j=1:xml.Images{1, i}.NumberOfROIs
            my_points_cell = xml.Images{1, i}.ROIs{1, j}.Point_px;
            my_label = xml.Images{1, i}.ROIs{1,j}.Name;
            my_points = zeros(size(my_points_cell, 2), 2);

            for k=1:size(my_points,1)
                [x, y] = get_coord_from_point(my_points_cell{1, k});
                my_points(k, :) = [x, y];
            end
            xs = my_points(:, 1)';
            ys = my_points(:, 2)';
            bw = poly2mask(xs, ys, size(vol, 1), size(vol, 2));
            for m=1:length(labels)
                if strcmp(my_label, labels(m))
                    logical_masks(:, :, image_index, m) = bw;
                end
            end    
         end
    end
    disp("Done!")
    mask = zeros(size(vol));

    for i=1:length(labels)
        mask(logical_masks(:, :, :, i)) = i*50;
    end
    dcmshow(mask, [])
end


function [x,y] = get_coord_from_point(my_points_string)
    my_points_string = erase(my_points_string,'(');
    my_points_string = erase(my_points_string,')');
    coordinates = strsplit(my_points_string,',');
    x = int16(str2double(coordinates(1)))';
    y = int16(str2double(coordinates(2)))';
end