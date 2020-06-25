l = dir('C:\Master thesis\master\kri-evaluation\compute-dices-teddy\*\*.png');

result = [];

for i = 1 : length(l)
    path = strcat(l(i).folder,'\' , l(i).name);
    
    image = rgb2gray(imread(path));
    image = image(137:150, 1631:1658);
    image = imresize(image, 40);
    text = ocr(image);
    text = text.Text;
    number = parse_text(text);

    d.name = l(i).name;
    d.dice = number;
    d.text = text;

    result = [result, d];
end



function number = parse_text(old_text)
    text = old_text;
    text = strrep(text, '‘’/c', '');
    text = strrep(text, '°/c', '');
    text = strrep(text, 'c', '');
    text = strrep(text, 'mm', '');
    text = strrep(text, 'mm', '');
    text = strrep(text, 'mm', '');
    text = strrep(text, 'S', '5');
    text = strrep(text, ' ', '');
%     disp(text)
    number = str2double(text);
    disp(number)
end