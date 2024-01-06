const { inputPath, outputPath, processImages } = require("./lib/image-to-text");
import * as fs from "fs";

async function readAllImagesToText() {
  const allFiles = await fs.promises.readdir(inputPath);
  const imageFiles = allFiles.filter((file) => file.endsWith(".gif"));

  await processImages(imageFiles, outputPath);
}

readAllImagesToText();
