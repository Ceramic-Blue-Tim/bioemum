load_app() {
    if lsmod | grep -q "dma_proxy"; then
        sudo rmmod dma_proxy
    fi
    if [ "$BIOEMUM_TARGET" = "vpk120" ]; then
        sudo fpgautil -R -n full
        sudo fpgautil -b "/lib/firmware/xilinx/$BIOEMUM_TARGET-bioemum/$BIOEMUM_TARGET-bioemum.pdi" -o "/lib/firmware/xilinx/$BIOEMUM_TARGET-bioemum/$BIOEMUM_TARGET-bioemum.dtbo" -f Full -n "full"
    else
        sudo xmutil unloadapp
        sudo xmutil loadapp "$BIOEMUM_TARGET-bioemum"
    fi
}

load_driver() {
    distro=$(lsb_release -i | awk '{print $3}')
    plinux_release=$(uname -r)

    if [ "$distro" = "Ubuntu" ]; then
        sudo insmod "$BIOEMUM_PATH/drivers/dma_proxy/dma-proxy.ko"
    elif [ "$distro" = "petalinux" ]; then
        sudo insmod "/lib/modules/$plinux_release/extra/dma-proxy.ko"
    else
        echo "$TAG Error: No driver available for $distro"
    fi
}

load_app
load_driver