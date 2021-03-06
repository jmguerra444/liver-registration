
% study_name = 'gn-simple-v1';
% study_name = 'gn-linear-v1';
% study_name = 'gn-ffd-v2';
study_name = 'v4';

% root = 'D:\jorge\OneDrive\OneDrive - SurgicEye GmbH\thesis\experiments\registration-studies\';
% root = 'C:\Users\Jorgue Guerra\OneDrive - SurgicEye GmbH\thesis\experiments\registration-studies\';
root = 'C:\Users\jmgue\OneDrive - SurgicEye GmbH\thesis\experiments\registration-studies\';

root = strcat(root , study_name, '\'); 
folder_ids = getFolders(root);

results = [];
b.name = 'Patients';
b.data = get_patient_list(strcat(root, folder_ids{1}, '\screenshots\'));
results = [results, b];
for i = 1 : length(folder_ids)
    f = folder_ids{i};
    n.name = f(1 : end - 11);
    
    r = process_folder(f, root);
    n.data = r;
    
    results = [results, n];
end

[data, headers] = postprocess_results(results);
xlswrite("output.xls", data');
xlswrite("headers.xls", headers');

%%
function result = process_folder(folder_id, root)
    disp(folder_id)
    study_folder = strcat(root, folder_id, '\screenshots\');

    list = dir(strcat(study_folder, '\*.png'));

    result = [];

    for i = 1 : length(list)
        image_filename = list(i).name;
        path = absolute_path(image_filename, study_folder);

        image = rgb2gray(imread(path));
        image = image(653:666, 1607:1637);
        image = imresize(image, 30);
        text = ocr(image);
        text = text.Text;
        text = parse_tre(text);
        
        disp(text);
        
        d = str2double(text);
        result = [result, d];
    end
end


function path = absolute_path(relative_path, parent)
    path = strcat(parent, relative_path);
end

function text = parse_tre(old_text)
    text = old_text;
    text = strrep(text, 'mm', '');
    text = strrep(text, 'S', '5');
    text = strrep(text, ' ', '');
    text = strrep(text, '%', '');
end

function folder_ids = getFolders(root)
    
    v = dir(root);
    v = v(3:end);
    folder_ids = {};
    
    for i = 1 : length(v)
        folder_ids{end + 1} = v(i).name;
    end
end

function patients = get_patient_list(folder)
    list = dir(strcat(folder, '\*.png'));
    patients = [];
    for i = 1 : length(list)
         image_filename = list(i).name;
         patient = strrep(image_filename, '.png', '');
         patient = str2double(patient);
         patients = [patients, patient];
    end
end

function [d, headers] = postprocess_results(results)
    
    l = length(results);
    headers = {};
    d = zeros(length(results(1).data), l);
    
    for i = 1 : l
        headers{i} = results(i).name;
        d(:, i) = results(i).data;
    end
  
end