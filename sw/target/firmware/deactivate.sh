sudo rmmod dma_proxy

if [ "$BIOEMUM_TARGET" = "vpk120" ]; then
    sudo fpgautil -R -n Full
else
    sudo xmutil unloadapp
    sudo xmutil loadapp k26-starter-kits
fi