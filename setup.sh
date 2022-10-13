#!/bin/bash

cd peekaboo/libpeekaboo
make
sudo make install
cd ..
cd peekaboo_dr
mkdir build
cd build
sudo apt-get install cmake g++ g++-multilib doxygen git zlib1g-dev libunwind-dev libsnappy-dev liblz4-dev -y
cd ..
cd ..
cd ..
cd dynamorio && mkdir build && cd build
cmake ..
make -j

