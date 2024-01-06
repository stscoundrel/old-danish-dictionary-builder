import * as fs from "fs";
const { processImages } = require("./lib/image-to-text");

const imageInoutPath = "./resources/rotated";
const outputTextPath = "./resources/rotated-text";

async function readRotatedImagesToText() {
  const allFiles = await fs.promises.readdir(imageInoutPath);
  const imageFiles = allFiles.filter((file) => file.endsWith(".gif"));

  await processImages(imageFiles, imageInoutPath, outputTextPath);
}

readRotatedImagesToText();
