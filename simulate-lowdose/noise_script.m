% This just adds poissons noise, reimplement in python

%% Load image and generate sinogram

% filename = 'test1.tif';
% image = imread(filename);
% image = imrotate(image, 90);            % Rotate to normal position

image = phantom(255);

number_projections = 1160;
angles = 0: (359/number_projections): 359;
sinogram = radon (image, angles);


%% Set hyperparametes
I = 5e3;                                % Incident level, which is the
                                        % relationship between low and high
                                        % dose
                                        
mu = -1000;                             % Electronic noise mean
sd = 20;                                % Electronic noise SD

%% Add noise
image_r = add_noise(image, angles, I);

% %% Reconstruction
% sinogram_ld = sinogram;
% image_r = iradon(sinogram_ld, angles);

%% Make figures
figure
subplot(2, 3, 1);
imshow(image, []);
title('Original Image');

subplot(2, 3, 2);
imshow(imresize(sinogram, 0.3), []);
xlabel('Angle');
ylabel('Index');
title('Original Sinogram')

subplot(2, 3, 4);
imshow(image_r, []);
title('Reconstructed Image')


%% Clean
%close('all')