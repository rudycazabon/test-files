#!/bin/bash

DEFAULT=$PS1
ender="\033[01;34m" # \w\[\033[00m\]\$"
inversvid="\0033[7m"
resetvid="\0033[0m"
redback="\0033[1;37;41m"
greenback="\0033[1;37;42m"
blueback="\0033[1;37;44m"

function get_additional_depends() {
    sudo apt install -y libxinerama-dev libxcursor-dev libglfw3-dev cmake-curses-gui
}

function clone_irtk_git_repos() {
    cd ~/Projects
    echo -e $greenback "Cloning OSPCommon from Github" $ender
        git clone https://github.com/ospray/ospcommon.git
    echo -e $blueback "Done" $ender

    echo -e $greenback "Cloning Embree from Github" $ender
        git clone https://github.com/embree/embree.git
    echo -e $blueback "Done" $ender

    echo -e $greenback "Cloning OspRay from Github" $ender
        git clone --recursive https://github.com/ospray/ospray.git
    echo -e $blueback "Done" $ender

    echo -e $greenback "Cloning OpenImageDenoise from Github" $ender
            git clone --recursive https://github.com/OpenImageDenoise/oidn.git
    echo -e $blueback "Done" $ender

    echo -e $greenback "Cloning OpenVKL from Github" $ender
        git clone https://github.com/openvkl/openvkl.git
    echo -e $blueback "Done" $ender


    cd ~
}

function get_ispc_compiler() {

    cd ~/Tools

    wget https://github.com/ispc/ispc/releases/download/v1.12.0/ispc-v1.12.0b-linux.tar.gz

    tar xvf *.tar.gz

    sudo cp ispc-v1.12.0-linux/bin/ispc /usr/bin

    cd ~

}


function build_ospcommon(){
    cd ~/Projects/ospcommon
    [ ! -d build/ ] && mkdir build
    cd build
    cmake -DCMAKE_CXX_COMPILER=clang++ -DCMAKE_C_COMPILER=clang ..
    make -j$(nproc)
    sudo make install
    cd ~     
}

function build_embree() {
    cd ~/Projects/embree
    [ ! -d build/ ] && mkdir build
    cd build
    cmake .. -DCMAKE_CXX_COMPILER=clang++ -DISPC_EXECUTABLE=$(which ispc) -DEMBREE_ISPC_SUPPORT=ON -DEMBREE_TASKING_SYSTEM=ON
    make -j$(nproc)
    sudo make install
    cd ~

}

function build_openvkl(){
    cd ~/Projects/openvkl
    [ ! -d build/ ] && mkdir build
    cd build
    cmake -DCMAKE_CXX_COMPILER=clang++ -DCMAKE_C_COMPILER=clang ..
    make -j$(nproc)
    sudo make install
    cd ~    
}

function build_oidn(){
    cd ~/Projects/oidn
    [ ! -d build/ ] && mkdir build
    cd build
    cmake -DCMAKE_CXX_COMPILER=clang++ -DCMAKE_C_COMPILER=clang ..
    make -j$(nproc)
    sudo make install
    cd ~     
}

function build_ospray(){
    cd ~/Projects/ospray
    [ ! -d build/ ] && mkdir build
    cd build
    cmake -DCMAKE_CXX_COMPILER=clang++ -DCMAKE_C_COMPILER=clang ..
    make -j$(nproc)
    sudo make install
    cd ~     
}

clone_irtk_git_repos
get_additional_depends
get_ispc_compiler
build_ospcommon
build_embree
build_openvkl
build_oidn
build_ospray