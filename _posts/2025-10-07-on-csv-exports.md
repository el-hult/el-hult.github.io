---
title: "On CSV Exports"
tags: ['csv-files', 'data management']
---

CSV files are great. They are simple to inspect in a text editor. You can process them with command-line tools like `grep`, `awk`, and `sed`. You can import them everywhere. You can export them from anywhere. They compress nicely with 7zip, .zip, or gzip or whatever. What’s not to like about them?  
Actually, there’s a lot not to like about them!

The problem is that there are many conventions around CSV files, and they are not always compatible. At some point, RFC-4180 tried to make everything standardized, but the spec is both too strict and too loose at the same time, so no one really follows it exactly.  
It does have some good ideas, so it’s worth being aware of.

So while not trying to standardize anything, below is a collection of what I find to be good and bad things to do with CSV files.

#### Good practices

- Use UTF-8 character encoding. This way, strange characters (like the Swedish åäö) will be properly encoded, and if other strangeness occurs (e.g. Turkish, Chinese, or French names or whatever), it won’t break. On top of that, some CSV readers (like Polars) have a super-optimized UTF-8 reader, and it is much faster than the Latin-1 version.  
- Use BOM. A byte-order mark is some special bytes at the start of the file. With BOM, Microsoft Excel will identify the file as UTF-8. Without it, it may guess and fail. So if you or your collaborators use Excel, make sure to encode with UTF-8-BOM.  
- Define the decimal point. Internationally, you use a full stop ⟨.⟩, but in Swedish orthography you use a comma ⟨,⟩. The choice is not so important—but you must define it!  
- Define the field separator. The normal choice is the comma ⟨,⟩ (as in “comma-separated values”), but tabs or semicolons are quite common too. All are fine, as long as you specify it. If you have a decimal comma, don’t use a comma as a field separator. I recommend against using tabs for field separation because it often looks odd in text editors.  
- Define the newline delimiter. It should be `\r\n` or `\n`. Most software libraries can handle either, but it’s good to be explicit. You shouldn’t use any other separator than these two.  
- Use quoting if your field contains special characters (newlines or field separators). Quoting means that if a field contains the newline delimiter or the field separator, you must indicate that *this* time, it’s part of the value. This is done by putting the value in quotation marks. If the quoted value contains quotation marks, they are escaped by an extra quotation mark. Only use double quotes for this. This is RFC-4180 compliant.  
- Use quoting when you need it. You can quote all fields, all fields that need it, or only the field/row combinations that need it. I think the last option is best, because it looks the nicest when you open the file in a text editor.  
- Compress the files to save space instead of trying to be clever about compression. Cutting off decimals in floats may save a few bytes, but it will cause rounding errors on the other end. Just serialize with a lot of precision, and compress the CSV afterward.  
- Use a standardized timestamp format with time zone indication. I think the best one is ISO-8601 compliant with fixed decimal-second precision (e.g. `2022-12-28T13:23:41.123456789+0200`) since it is unambiguous and can encode down to nanoseconds, which is more than enough for every use case I’ve seen. It’s often verbose, but not really a problem in practice. Use zipping to save space if you need to!  
- Use decimal points in float columns, even when not needed. Let’s say the first 100 lines have values like `10` and `21`, and on line 101 there’s a `201.12`. Your software might have guessed that this column only contains integers, and now it’s mad. By writing `10.0` and `21.0`, you ensure detection algorithms work out of the box in most cases.  
- Only use CSV for tabular, normalized data. Each line should have the same number of fields, and each field should have a fixed data type. If there’s a nested data structure, use another format—JSON, Parquet, multiple CSV files (like in a normalized database), or, in the worst case, JSON fields inside the CSV.  
- Place metadata in a separate file. Sometimes there’s a header section before the tabular data, and while this is nice when reading the file in a text editor, it’s generally cleaner to have a separate file containing the header. If you really want to ship it as one file, bundle it in a tarball or zip file.
- Indicate missing data with an empty field. That is `,,`. Never quote an empty value, since `,"",` may be interpreted as an empty string sometimes, which is different from no-data marker.

#### Unclear practices
- Use quotation on all string fields, even when not needed. This can make it nicer to read in a text editor and may help datatype-guessing algorithms. It’s not really a guarantee though, so I’m on the fence about it. Should `"10,0"` be deserialized as a string, a floating-point number, or an integer? Unclear. If the comma ⟨,⟩ is both the decimal point and the field separator, this can be really confusing.

#### Bad practices
- Inventing clever schemes to save bytes, e.g. rounding off floats in decimal precision. Use compression by zipping the file at the end instead.  
- Replacing special characters (commas, newlines, åäö) just to make serialization work. That’s simply destroying the data!  
- Having timestamps in local time zones.  
- Splitting date and time into separate columns. In that case, the time zone info is often forgotten. You can have that in a separate column, which is fine, but a single standardized timestamp is neater.  
- Using Unix timestamps for timestamps. It can be ambiguous whether they represent milliseconds or nanoseconds, and whether the standard epoch (1970-01-01) or a special one (e.g. 2000-01-01) is used.  
- Using fixed-width formats (e.g. 12 bytes for field 1, 16 bytes for field 2, etc.). It can sometimes speed up I/O, but if speed is a concern, you should use a binary format, not CSV.  
- Using ragged lines. A “ragged” line is where some lines have more or fewer fields than others. This typically occurs when different lines have different “types” and thus different fields. This is very error-prone. It also occurs when omitted field separators imply some field is `None`. Also very confusing and overall bad.
