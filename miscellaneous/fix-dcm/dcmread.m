function  [M,info]=dcmread(directorio)
%       Es una función que recibe un directorio con archivos .dcm
%       y los carga en una matriz de 3 dimensiones en forma volumétrica.
%       Las dimensiones de la matriz son anchoImagen x altoImagen x #Cortes
%       
%       Realizada por
%       Jorge Mario Guerra

    h= dir(directorio);
    nombre=h(3).name;
    map=dicomread(strcat(directorio,'/',nombre));
    info=dicominfo(strcat(directorio,'/',nombre));
    M=zeros(size(map,1),size(map,2),length(h));
    M(:,:,1)=map;
    pb = waitbar(0,'loading...');
    if (length(h)>3)
        for i = 4 : length(h)
            perc = i / length(h);
            waitbar(perc,pb,strcat(int2str(perc*100),'% cargando'));
            nombre = h(i).name;
            map = dicomread(strcat(directorio,'/',nombre));
            info2 = dicominfo(strcat(directorio,'/',nombre));
            M(:,:,i-2)=map;
            info=[info;info2]; %#ok<*AGROW>
        end
    end
    M=M-1024;
    close(pb);
end
