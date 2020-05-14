function writedcm(M, path, info) 
   switch nargin           
       case 2
           caso1(M, path);
       case 3
           
           caso2(M, path, info);
       otherwise
       waitfor(msgbox('Invalid number of arguments','Error','error'));
   end
end

function caso1(M, path)
    pb = waitbar(0,'Escribiendo');
    M = int16(M);
    for i = 1 : size(M, 3) - 2
        perc = i / size(M, 3);
        waitbar(perc,pb,strcat(int2str(perc * 100), '% escrito'));
        filename = strcat(path, '\im', num2str(i, '%03.f'), '.dcm');
        dicomwrite(M(:,:,i), filename);
    end
    close(pb);
end

function caso2(M, path, info)
    pb = waitbar(0, 'Escribiendo');
    M = int16(M);
    for i = 1 : size(M, 3) - 2
        perc = i / size(M, 3);
        waitbar(perc, pb, strcat(int2str(perc * 100), '% escrito'));
        filename=strcat(path, '\im', num2str(i, '%03.f'), '.dcm');
        dicomwrite(M(:, :, i) + 1e3, filename, info(i));
    end
    close(pb);
end