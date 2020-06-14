
folder_id = '0613162951';
study_folder = strcat('C:\Master thesis\master\registration-params\studies\', folder_id,'\screenshots\');

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
    d.distance = str2double(text);
    
    result = [result, d];
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
