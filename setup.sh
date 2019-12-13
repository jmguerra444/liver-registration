# Start a VM and deploy our 2d-unet example for CT

# Install miniconda
sudo wget "https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"
sudo bash Miniconda3-latest-Linux-x86_64.sh
sudo chown -R jorgemguerrag ~/miniconda3

# Install other dependencies
sudo apt-get update
sudo apt-get upgrade
sudo apt install git-all
git config --global credential.helper store                     # Save git credentials

sudo apt-get install nano

# Get our repository
git clone https://gitlab.lrz.de/ga53koj/master-thesis.git
cd master-thesis/simple-2d-unet/
git checkout develop
conda env create -f environment.yml
conda activate master-thesis

# Install cuda
sudo apt-get install gcc g++ libxi6 libglu1-mesa libglu1-mesa-dev libxmu6 linux-source
wget http://developer.download.nvidia.com/compute/cuda/10.2/Prod/local_installers/cuda_10.2.89_440.33.01_linux.run
sudo sh cuda_10.2.89_440.33.01_linux.run
nvidia-smi          # Check GPU and installed cuda

# Download data
pip install gdown
gdown https://drive.google.com/uc?id=1jyVGUGyxKBXV6_9ivuZapQS8eUJXCIpu

# Extract train datasets
tar -xvf Task03_Liver.tar Task03_Liver/imagesTr
tar -xvf Task03_Liver.tar Task03_Liver/labelsTr
mv Task03_Liver decathlon-data       # rename
rm Task03_Liver.tar
cd ~
mkdir scan

# 

# Do some cleanup
cd ..
rm Miniconda3-latest-Linux-x86_64.sh
rm cuda_10.2.89_440.33.01_linux.run
rm -r NVIDIA_CUDA-10.2_Samples/