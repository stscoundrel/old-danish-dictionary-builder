import 'package:image_rotator/image_rotator.dart' as image_rotator;

const Map<String, double> imagesToRotate = {
  'resources/images/2-adamsbid.gif': -0.4,
  'resources/images/97-balstyrig.gif': 1.0,
  'resources/images/1000-S. Hansbrod.gif': -1.4,
  'resources/images/1109-hosskrift.gif': 1.15,
  'resources/images/1817-metal.gif': -0.5,
  'resources/images/2387-røtte (rotte).gif': -2.33,
  'resources/images/3021-timesand.gif': 1.1,
};

void main(List<String> arguments) {
  imagesToRotate.forEach((imagePath, rotationDegrees) {
    final outputPath = imagePath.replaceFirst('images', 'rotated');
    image_rotator.rotateImage(imagePath, outputPath, rotationDegrees);
  });
}
