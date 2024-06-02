# Old Danish Dictionary Builder

Build machine-readable version of Otto Kalkar's "Dictionary of the Old Danish Language".

Currently work-in-progress, but the goal is to offer JSON dataset with normalized dictionary data. It might very well end up being a slow process which requires a lot of manual labor, but we'll see how far we can get with code alone.

## Implementations using the output of the builder

- [TypeScript / Node.js library](https://github.com/stscoundrel/old-danish-dictionary)

## Current features:
- Downloads all scanned pages.
- Rotates images that are too skewed for good ORC results.
- Feeds images to image-to-text (OCR) library.
- Parse OCR'd text to json.

## Steps to produce the final json

### 1. Run scraper to download page images.

Setup Maven & run `mvn install` inside the `scraper` subfolder. Best of luck with that.

To run the scraper script:

`mvn spring-boot:run`

Images will be downloaded to `scraper/resources/images` folder.

### 2. Run script to rotate pages

Some pages are too skewed in their scan to provide reliable OCR results. We need to rotate problematic ones first.

Setup Dart. Move files to be rotated to `image-rotator/resources/images`. There is mapping of files needing rotation in `image-rotator/bin/image_rotator.dart`

To run the rotator script:

`dart run`

### 3. Run OCR to turn images to text

Setup Node.js 20+ (eg. via NVM) & run `npm/yarn install` inside the `image-to-text` subfolder.

Copy `images` folder from step one to `image-to-text/resources` folder. Add empty `text` folder to the same resources folder.

To run the images-to-text script:

`yarn images-to-text`

or

`npm run images-to-text`

This is likely to take long, possibly hours.

Text files will be generated to `image-to-text/resources/text` folder.

### 4. Parse OCR'd text to JSON.

Setup Python 3.11. Copy OCR'd text files to `parser/resources/text` folder.

Run the Python script inside the parser folder. For example `python3 run main.py`. It generates `dictionary.json` file containing structured json representation of all the scanned text.

### 5. Compress outputted json for programmatic use

The produced dictionary is quite hefty, close to 20MB. To ship it more effectively as part of library, you can compress it.

Setup Dart. Add generated `dictionary.json` to `minifier/resources`. 

To generate compressed versions:

`dart run` inside minifier folder.

Currently only generates gzipped output, around 6mb instead of 18mb.

## Additional tools for development

### Scan rotator

Some scans are skewed / in odd angle, which means the OCR result may be less than optimal. This is mostly due to OCR issues about defining where the line really starts and ends, if they're not horizontal enough.

`image-rotator` is a Dart app that can rotate images based on mapping. Problematic ones can be added to mapping, resaved as rotated images & then read again with OCR step.

To run it

`dart run`

### OCR result analyzer

`analyzer` contains Kotlin/Gradle script for analyzing OCR results and trying to identify possibly skewed scan results. When accurate, it can point out pages that could benefit from rotation & another round of OCR for better results.

To run it:

`./gradlew run`


## Quality of output

The quality of output is a matter to be improved. Some scans should be rotated, some malformatted text should be manually improved, some edge cases should be ironed out with application logic. All in all, it will probably never be perfect, but considering the sheer size of the original work, it is somewhat impressive that it even works at all.

## About "Dictionary of the Old Danish Language"

_"Ordbog til det ældre danske Sprog"_ dictionary was published in late 1800s by Otto Kalkar. Old Danish is an ancestor language of Danish, which developed from Old East Norse, the eastern dialect of Old Norse, at the end of the Viking Age. The dictionary itself is called "the dictionary of elder Danish speech" and it covers time period of 1300 - 1700.

Despite its name, Kalkars dictionary is not only a dictionary of "Old Danish", as it covers period from Middle Danish _(=gammeldansk)_ to early Modern Danish _(=ældre nydansk)_. The book covers vocabulary from 1300 - 1700, while the "Old Danish" period stops at 1500s. Due to the large timespan of the dictionary, the oldest vocabulary would be close to the language spoken by Late Viking Age danes, whilst newest entries would not differ much from Danish of the 1800's.

The term "Old Danish" in itself covers multiple periods in Danish language, namely:

- Runic Danish 800 - 1100 (olddansk in Danish. Often included in "Old Norse")
- Early Middle Danish 1100 - 1350 (yngre gammeldansk/middeldansk in Danish)
- Late Middle Danish 1350 - 1525 (ældre gammeldansk/middeldansk in Danish)
