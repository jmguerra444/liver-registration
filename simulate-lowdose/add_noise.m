function y = add_noise(x, theta, lambda)

% Modified from ADDPOISSON JCRG 2010 CT CIC

y = zeros(size(x));
[M, ~, L] = size(x);

for i=1:L
    
    % Adds poisson noise
    x1 = x(:, :, i) / 100;
    proj = radon(x1, theta);                    %create projections
    N = poissrnd( lambda .* exp(-proj));  %Poisson Noise 
    proj_noise = log(lambda ./ (N + 0.1));     %Add Noise
    
    % Adds Gaussian noise
    
    y(:,:,i) = iradon(proj_noise, theta, M) * 100; %Go back to image space again
end




