folder_ids = {
    'n_affine_mi_0616014924'
    'n_affine_ncc_0616021035'
    'n_affine_ssd_0616023146'
    'n_rigid_mi_0616004549'
    'n_rigid_ncc_0616010701'
    'n_rigid_ssd_0616012811'
    't_affine_mi_0617053946'
    't_affine_ncc_0617072244'
    't_affine_ssd_0617090541'
    't_rigid_mi_0617003056'
    't_rigid_ncc_0617021353'
    't_rigid_ssd_0617035649'
    };

results = [];
for i = 1 : length(folder_ids)
    f = folder_ids{i};
    n.name = f(1 : end - 11);
    
    r = process_folder(f);
    n.result = r;
    
    results = [results, n];
end

function result = process_folder(folder_id)
    disp(folder_id)
    study_folder = strcat('C:\Master thesis\master\registration-params\studies\completed\', folder_id,'\screenshots\');

    list = dir(strcat(study_folder, '\*.png'));

    result = [];

    for i = 1 : length(list)
        image_filename = list(i).name;
        path = absolute_path(image_filename, study_folder);

        image = rgb2gray(imread(path));
        image = image(537:553, 1688:1770);
        image = imresize(image, 20);
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