sudo apt-get update && sudo apt-get upgrade
sudo dpkg --configure -a
sudo apt-get update && sudo apt-get upgrade

sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-key 421C365BD9FF1F717815A3895523BAEEB01FA116
sudo apt-get update && sudo apt-get upgrade
sudo apt-get install ros-indigo-desktop-full
sudo rosdep init
rosdep update
echo "source /opt/ros/indigo/setup.bash" >> ~/.bashrc
source ~/.bashrc

sudo apt-get install python-rosinstall

makedir home\catkin_ws
cd catkin_ws/
chmod -R 755 *
catkin_make && catkin_make install
sudo apt-get install git-core python-argparse python-wstool python-vcstools python-rosdep ros-indigo-control-msgs ros-indigo-joystick-drivers
sudo apt-get install ros-indigo-joint* ros-indigo-actionlib*
chmod -R 755 *
catkin_make && catkin_make install
source devel/setup.bash

catkin_make && catkin_make install

