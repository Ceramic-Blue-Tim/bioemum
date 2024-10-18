#!/bin/bash
TAG_COLOR="\e[95m"
END_COLOR="\e[0m"
TAG_NAME="Bioemum"
TAG="[$TAG_COLOR$TAG_NAME$END_COLOR]"

echo -e "$TAG Setup environment variables and scripts permissions"

# Check command-line argument
case $1 in
    kr260|kv260|vpk120)
        export BIOEMUM_TARGET=$1
        ;;
    *)
        echo "Invalid option: $1"
        echo "Usage: $0 [kr260|kv260|vpk120]"
        exit 1
        ;;
esac

# Initialize BIOEMUM_PATH if not set
if [ -z "$BIOEMUM_PATH" ]; then
    DIR="$( cd "$( dirname -- "$0" )" && pwd )"
    export BIOEMUM_PATH="$DIR"
fi

# Set execute permissions for scripts
chmod +x "$BIOEMUM_PATH"/*.sh
chmod +x "$BIOEMUM_PATH"/app/*.sh
chmod +x "$BIOEMUM_PATH"/firmware/*.sh

# Check if .init.bak file exists, if not, create it and update ~/.bashrc
if [ ! -e "$BIOEMUM_PATH/.init.bak" ]; then
    cp "$BIOEMUM_PATH/init.sh" "$BIOEMUM_PATH/.init.bak"
    echo "export BIOEMUM_PATH=$BIOEMUM_PATH" >> ~/.bashrc
    echo "source $BIOEMUM_PATH/init.sh $BIOEMUM_TARGET" >> ~/.bashrc
fi