---
title: "A Tagged Union in C"
tags: ['data structures', 'functional programming']
---

You should in general model data properly. We want the semantics of the data to be reflected in the data structures.If your data is text, it should be in utf8. If it is a timestamp, it should have a time zone, and be in appropriate resolution offset from an epoch (e.g. unix timestamp). Et cetera. 

Possibly my favorite modelling tool is alternatives. Something is *either* a big object (points to the heap) *or* it is a small thing (it lives on the stack). In rust such alternatives are called `enums`. In Haskell, they are `sum types`. In typescript, it is a `union` type. Java introduced `sealed classes` eventually. Python has `union` too. 
Of course, the ergonomics vary wildly between the languages, but the core idea is still there. 

Given that the basic idea is a clever and general one, it can be good to think about what it *really* means to have a union. Therefore, I hacked together a contrived example in C. 

```c
typedef enum { INT_PAIR, FLOAT } Tag;

typedef struct {
    Tag tag;
    union {
        float f;
        struct { int i; int j; } p;
    };
} Arg;

// if float; square it
// if int pait; flip them
Arg go(Arg arg) {
    if  (arg.tag == FLOAT) { return {.tag=FLOAT,   .f=arg.f * arg.f            };
    } else                 { return {.tag=INT_PAIR,.p={.i=arg.p.j,.j=arg.p.i } };
    }
}
```

The point is that the struct `Arg` is a sequence of memory that begins with  a `Tag` -  a couple of bytes indicating how to interpret the rest of the bytes -- and then the rest comes. This example also explains why it is called a Tagged Union sometimes. Because the tag might be needed at runtime to interpret the payload.

This example also shows that a good idea from one language can almost always be used in any other language. They are just tools. Use the ones you like.
