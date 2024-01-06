import * as fs from "fs";
import Tesseract from "tesseract.js";
import { chunkArray } from "skilja";

export const inputPath = "./resources/images";
export const outputPath = "./resources/text";

const WORKERS_COUNT = 6;
const BATCH_SIZE = 30;

const getWorker = async (): Promise<Tesseract.Worker> => {
  const worker = await Tesseract.createWorker("dan");

  worker.setParameters({
    preserve_interword_spaces: "1",
  });

  return worker;
};

const getScheduler = async (): Promise<Tesseract.Scheduler> => {
  const scheduler = Tesseract.createScheduler();

  const workers = await Promise.all(
    [...Array(WORKERS_COUNT)].map(async (_) => await getWorker()),
  );

  workers.forEach((worker) => scheduler.addWorker(worker));

  return scheduler;
};

export async function processImages(
  imageFiles: string[],
  inputLocation: string,
  outputLocation: string,
) {
  try {
    const batches: string[][] = chunkArray(imageFiles, BATCH_SIZE);
    const scheduler = await getScheduler();

    for (let i = 0; i < batches.length; i += 1) {
      // Read images.
      const imageProcessingPromises = batches[i].map(async (file) => {
        const imagePath = `${inputLocation}/${file}`;

        // Perform OCR on the current image
        const {
          data: { text },
        } = await scheduler.addJob("recognize", imagePath);

        console.log(
          `Batch ${i + 1}: ${scheduler.getQueueLen()} images to be processed `,
        );

        return [file, text];
      });

      const imageResults = await Promise.all(imageProcessingPromises);

      console.log(
        `Read batch ${i + 1} out of ${
          batches.length
        }. Waiting to create text files...`,
      );

      // Store results as text.
      const fileSavePromises = imageResults.map(async ([fileName, text]) => {
        const outputFilePath = `${outputLocation}/${fileName}.txt`.replace(
          ".gif",
          "",
        );
        return await fs.writeFile(outputFilePath, text, () => {});
      });

      await Promise.all(fileSavePromises);

      console.log(
        `Batch ${i + 1} out of ${batches.length} processed successfully.`,
      );
    }

    await scheduler.terminate();
  } catch (error) {
    console.error("Error processing images:", error);
  }
}

export default {};
