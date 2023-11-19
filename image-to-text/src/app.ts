import * as fs from "fs";
import Tesseract from "tesseract.js";
import { chunkArray } from "skilja";

const inputPath = "./resources/images";
const outputPath = "./resources/text";

const getWorker = async (): Promise<Tesseract.Worker> => {
  const worker = await Tesseract.createWorker("dan");

  worker.setParameters({
    preserve_interword_spaces: "1",
  });

  return worker;
};

async function processImages() {
  try {
    const allFiles = await fs.promises.readdir(inputPath);
    const batches = chunkArray(allFiles, 5);

    for (let i = 0; i <= batches.length; i += 1) {
      const imageProcessingPromises = batches[i].map(async (file) => {
        const imagePath = `${inputPath}/${file}`;

        const worker = await getWorker();

        // Perform OCR on the current image
        const {
          data: { text },
        } = await worker.recognize(imagePath);

        // Output the extracted text to a file
        const outputFilePath = `${outputPath}/${file}.txt`.replace(".gif", "");
        await fs.writeFileSync(outputFilePath, text);
        console.log(`Saved ${outputFilePath}`);
      });

      console.log(
        `Read batch ${i + 1} out of ${
          batches.length
        }. Waiting to create text files...`,
      );
      await Promise.all(imageProcessingPromises);
      console.log(
        `Batch ${i + 1} out of ${batches.length} processed successfully.`,
      );
    }
  } catch (error) {
    console.error("Error processing images:", error);
  }
}

processImages();
