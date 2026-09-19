# Chapter 12. Conclusion

# What You’ve Learned

After reading this book, you are now familiar with several advanced C programming concepts. When looking at larger code examples, you now know why the code looks the way it does. You now know the reasoning behind the design decisions made in that code. For example, in the Ethernet driver sample code presented in the [Preface](Preface.md) of this book, you now understand why there is an explicit `driverCreate` method and why there is a `DRIVER_HANDLE` that holds state information. The patterns from [Part I](Part_01_C_Patterns.md) guided the decisions made in this example and many others discussed throughout the book.

The pattern stories from [Part II](Part_02_Pattern_Stories.md) showed you the benefits of applying the patterns from this book and how to grow code bit by bit through the application of patterns. When facing your next C programming problem, review the problem sections of the patterns and see whether one of them matches your problem. In that case, you are very lucky because then you can benefit from the guidance provided by the patterns.

# Further Reading

This book helps C programming novices to become advanced C programmers. Here are some other books that particularly helped me improve my C programming skills:

- *Clean Code: A Handbook of Agile Software Craftsmanship* by Robert C. Martin (Prentice Hall, 2008) discusses the basic principles of how to implement high-quality code that lasts over time. It is a good read for any programmer and covers topics like testing, documentation, code style, and others.

- *Test-Driven Development for Embedded C* by James W. Grenning (Pragmatic Bookshelf, 2011) uses a running example to explain how to implement unit-tests with C in the context of hardware-near programs.

- *Expert C Programming* by Peter van der Linden (Prentice Hall, 1994) is an early book on advanced C programming guidance. It describes how the C syntax works in detail and how to avoid common pitfalls. It also discusses concepts like C memory management and tells you how the linker works.

- Closely related to my book is the book *Patterns in C* by Adam Tornhill (Leanpub, 2014). It also presents patterns and focuses on how to implement the Gang of Four design patterns with C.

# Closing Remarks

Compared to a C programmer fresh out of their studies, you now have advanced knowledge on which techniques to use to compose larger-scale and industrial-strength C code. You can now:

- perform error handling, even though you don’t have a mechanism like exceptions

- manage your memory, even though you don’t have a garbage collector and you don’t have destructors to clean up the memory

- implement flexible interfaces, even though you don’t have native abstraction mechanisms

- structure files and code, even though you don’t have classes or packages

You are now able to work with C, despite it lacking some of the conveniences of modern programming languages.

