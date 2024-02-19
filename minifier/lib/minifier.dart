import 'dart:convert';
import 'dart:io';

void gzipCompressFile(File inputFile, File outputFile) {
  final fileContent = _readFile(inputFile);
  final gzipped = _gzipCompress(fileContent);

  outputFile.writeAsBytesSync(gzipped);
}

String _readFile(File inputFile) {
  return inputFile.readAsStringSync();
}

List<int> _gzipCompress(String fileContent) {
  final compressedData = utf8.encode(fileContent);
  final gzippedData = gzip.encode(compressedData);

  return gzippedData;
}
