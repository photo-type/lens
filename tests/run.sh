rm -rf screens/*.JPG
rm -rf boundaries/*.JPG
for line in `ls -l images | grep .JPG | awk '{ print $9}'`;
do
  echo "Noise removal and cropping: $line"
  ../bin/python crop_image.py $line
done
echo =======================
for line in `ls -l screens | grep .JPG | awk '{ print $9}'`;
do
  echo "Detecting boxes: $line"
  ../bin/python find_boxes.py $line
done
