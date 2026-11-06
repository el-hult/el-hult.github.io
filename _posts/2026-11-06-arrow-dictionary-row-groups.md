---
title: "I made Arrow better!"
tags: ['arrow', 'parquet', 'open source', 'ai']
---

I recently got a pull request merged into [Apache Arrow](https://arrow.apache.org/), a library I use almost every day. The fix itself is tiny, but I'm still proud of it. 

## Background

In 2024, I received a batch of CSV files with data from a healthcare provider. As usual with CSV, they were a mess. Broken line breaks, file encoding differed between files, and floats and datetime stored as a strings. That makes files slow to read and takes a lot of extra space. I have [complained about CSV exports before]({% post_url 2025-10-07-on-csv-exports %}).

So I did some cleaning and saved everything as Parquet files using pyarrow.

One part of the data was diagnoses. As in the Swedish patient registry, the source had columns `diagnosis1`, `diagnosis2`, and so on up to `diagnosis30`, most of them empty. I normalized these into a single column of type `list<dictionary<int32, utf8>>`, in Arrow terms. Each value is a variable-length list of diagnoses, and each diagnosis is stored as an integer that maps to an ICD code string through a dictionary. It is compact, and it captures the semantics well: ICD codes are codes from a fixed set, not general prose.

## The bug

Parquet files are split into *row groups*, which can be read independently of each other. For that to work, each row group stores its own dictionary. So when you read a whole file, you get one chunk per row group, and each chunk has a different dictionary.

In pyarrow this works fine, because pyarrow reads files through the Dataset API, which is built to combine many independent pieces. But the `ReadTable` API, refused with `Nested data conversions not implemented for chunked array outputs`.
The R arrow package uses that code path by default. So my colleagues working in R could not open the files I sent them. I [reported the issue](https://github.com/apache/arrow/issues/32723) and went back to `list<utf8>`. On disk the difference is small, since Parquet has its own dictionary encoding for strings. But in memory it is less efficient, and the semantics are worse.

## The fix

Two years later, the issue got some new activity, and I decided to try fixing it myself with the help of an AI agent. I had held back before, since I am not that good at writing complex C++ code.

The Arrow project explicitly accepts AI-assisted contributions, but requires transparency about how AI was used. That matches my own view. I use AI, but I take responsibility for what I submit. So the PR description says plainly that Claude wrote the code, and that I wrote the description and reviewed everything.

The fix turned out to be easy. The reader already had a function that turns a chunked array into a single array. It handled zero or one chunk, and returned `NotImplemented` for more. The fix is to concatenate the chunks using a function Arrow already has:

```cpp
default: {
  ARROW_ASSIGN_OR_RAISE(std::shared_ptr<Array> array,
                        ::arrow::Concatenate(chunked.chunks(), pool));
  return array->data();
}
```

This is the tiny patch of [PR #55351](https://github.com/apache/arrow/pull/55351).

There is one known limitation. Concatenation fails if the merged data overflows the array's offset type, which in practice means more than 2 GiB of data in a single column. I did the math for my use case, and I will not get anywhere close to that. So I left it unfixed, and the error is passed on to the user.

Claude did write a fix for the overflow case too, and it did so quickly. But that version was harder to read and involved some hairy memory management. I did not feel I could take responsibility for it, so I left it out. If I ever hit that limit, at least I know it can be solved.

## Conclusion

I am proud to have helped a little with a project I rely on every day. AI tools have lowered the threshold for contributing. A fix like this one would have taken me much longer to find on my own in an unfamiliar C++ codebase. But the threshold for *responsibility* stays the same. Whether you write the code yourself or have an AI write it, you have to understand what you submit and stand behind it.


**P.S.** The outline and final editing of this post were done by me, a human. Claude Code helped turn the outline into prose.
