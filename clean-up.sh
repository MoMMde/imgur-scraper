echo "Cleaning... "
DIRECTORY="${1:-./output/}"
echo "Target Directory: ${DIRECTORY}"
echo "Executing: rm -rf $DIRECTORY/*.jpg"
# isn't working -- needs fix
rm -rf $DIRECOTRY/*.jpg

