import 'package:image_rotator/image_rotator.dart' as image_rotator;

const Map<String, double> imagesToRotate = {
  'resources/images/97-balstyrig.gif': 1.0,
  'resources/images/1109-hosskrift.gif': 1.15,
};

void main(List<String> arguments) {
  imagesToRotate.forEach((imagePath, rotationDegrees) {
    final outputPath = imagePath.replaceFirst('images', 'rotated');
    image_rotator.rotateImage(imagePath, outputPath, rotationDegrees);
  });
}
