import 'dart:io';

import 'package:image_rotator/image_rotator.dart' as image_rotator;
import 'package:test/test.dart';

void main() {
  test('Generates rotated images', () async {
    // Expected sample page to be rotated.
    final testInputFilePath = "resources/images/97-balstyrig.gif";
    final testOutputFilePath = "resources/rotated/97-balstyrig.gif";

    await image_rotator.rotateImage(testInputFilePath, testOutputFilePath, 0.5);

    // Assert that the output file was created
    expect(File(testOutputFilePath).existsSync(), isTrue);
  });
}
