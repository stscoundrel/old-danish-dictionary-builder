import 'dart:io';
import 'package:image/image.dart' as img;

Future<void> rotateImage(
    String inputFilePath, String outputFilePath, double rotationDegrees) async {
  try {
    // Read the input image
    final fileBytes = await File(inputFilePath).readAsBytes();
    final image = img.decodeGif(fileBytes);

    if (image != null) {
      // Rotate the image
      final rotatedImage = img.copyRotate(image, angle: rotationDegrees);

      // Save the rotated image to a new file
      await File(outputFilePath).writeAsBytes(img.encodeGif(rotatedImage));

      print(
          'Image rotation completed. Check the output file at: $outputFilePath');
    } else {
      print('Failed to decode the input image.');
    }
  } catch (e) {
    print('Error: $e');
  }
}
