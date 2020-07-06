results = [];
root = 'C:\Master thesis\master\registration-params\studies\completed\v8\';
folder_ids = getFolders(root);

for i = 1 : length(folder_ids)
    f = folder_ids{i};
    n.name = f(1 : end - 11);
    
    r = process_folder(f, root);
    n.result = r;
    
    results = [results, n];
end

function result = process_folder(folder_id, root)
    disp(folder_id)
    study_folder = strcat(root, folder_id, '\screenshots\');

    list = dir(strcat(study_folder, '\*.png'));

    result = [];

    for i = 1 : length(list)
        image_filename = list(i).name;
        path = absolute_path(image_filename, study_folder);

        image = rgb2gray(imread(path));
        image = image(537:553, 1688:1770);
        image = imresize(image, 30);
        text = ocr(image);
        text = text.Text;
        text = parse_text(text);

        d.name = strrep(image_filename, '.png', '');
        d.(folder_id) = str2double(text);

        result = [result, d];
    end
end

function path = absolute_path(relative_path, parent)
    path = strcat(parent, relative_path);
end

function text = parse_text(old_text)
    text = old_text;
    text = strrep(text, 'mm', '');
    text = strrep(text, 'S', '5');
    text = strrep(text, ' ', '');
end

function folder_ids = getFolders(root)
    
    v = dir(root);
    v = v(3:end);
    folder_ids = {};
    
    for i = 1 : length(v)
        folder_ids{end + 1} = v(i).name;
    end
end