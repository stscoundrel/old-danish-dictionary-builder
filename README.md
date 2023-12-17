# Old Danish Dictionary Builder

Build machine-readable version of Otto Kalkar's "Dictionary of the Old Danish Language".

Currently work-in-progress, but the goal is to offer JSON dataset with normalized dictionary data. It might very well end up being a slow process which requires a lot of manual labor, but we'll see how far we can get with code alone.

## Current features:
- Downloads all scanned pages.
- Feeds images to image-to-text (OCR) library.

## Upcoming features
- Parse ORC results to machine-readable structured formats.

### About "Dictionary of the Old Danish Language"

_"Ordbog til det ældre danske Sprog"_ dictionary was published in late 1800s by Otto Kalkar. Old Danish is an ancestor language of Danish, which developed from Old East Norse, the eastern dialect of Old Norse, at the end of the Viking Age. The dictionary itself is called "the dictionary of elder Danish speech" and it covers time period of 1300 - 1700.

Despite its name, Kalkars dictionary is not exactly a dictionary of "Old Danish" _(=olddansk, often included in umbrella of "Old Norse")_, as it covers period from Middle Danish _(=gammeldansk)_ to early Modern Danish _(=ældre nydansk)_. Due to the large timespan of the dictionary, the oldest vocabulary would be close to the language spoken by Late Viking Age danes, whilst newest entries would not differ much from modern Danish.
