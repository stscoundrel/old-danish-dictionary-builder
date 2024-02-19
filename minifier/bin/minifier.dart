import 'dart:io';

import 'package:minifier/minifier.dart' as minifier;

void main() {
  final inputFile = File('resources/dictionary.json');
  final outputFile = File('resources/dictionary.json.gz');

  minifier.gzipCompressFile(inputFile, outputFile);
}
