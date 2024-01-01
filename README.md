# Old Danish Dictionary Builder

Build machine-readable version of Otto Kalkar's "Dictionary of the Old Danish Language".

Currently work-in-progress, but the goal is to offer JSON dataset with normalized dictionary data. It might very well end up being a slow process which requires a lot of manual labor, but we'll see how far we can get with code alone.

## Current features:
- Downloads all scanned pages.
- Feeds images to image-to-text (OCR) library.

## Upcoming features
- Parse ORC results to machine-readable structured formats.


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


### About "Dictionary of the Old Danish Language"

_"Ordbog til det ældre danske Sprog"_ dictionary was published in late 1800s by Otto Kalkar. Old Danish is an ancestor language of Danish, which developed from Old East Norse, the eastern dialect of Old Norse, at the end of the Viking Age. The dictionary itself is called "the dictionary of elder Danish speech" and it covers time period of 1300 - 1700.

Despite its name, Kalkars dictionary is not exactly a dictionary of "Old Danish" _(=olddansk, often included in umbrella of "Old Norse")_, as it covers period from Middle Danish _(=gammeldansk)_ to early Modern Danish _(=ældre nydansk)_. Due to the large timespan of the dictionary, the oldest vocabulary would be close to the language spoken by Late Viking Age danes, whilst newest entries would not differ much from Danish of the 1800's.
