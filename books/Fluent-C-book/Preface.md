# Preface

You picked up this book to move your programming skills one step forward. That is good, because you’ll definitely benefit from the hands-on knowledge provided in this book. If you have a lot of experience programming in C, you’ll learn the details of good design decisions and about their benefits and drawbacks. If you are fairly new to C programming, you’ll find guidance about design decisions, and you’ll see how these decisions are applied bit by bit to running code examples for building larger scale programs.

The book answers questions such as how to structure a C program, how to cope with error handling, or how to design flexible interfaces. As you learn more about C programming, questions often pop up, such as the following:

- Should I return any error information I have?

- Should I use the global variable `errno` to do that?

- Should I have few functions with many parameters or the other way around?

- How do I build a flexible interface?

- How can I build basic things like an iterator?

For object-oriented languages, most of these questions are answered to a great extent by the Gang of Four book *Design Patterns: Elements of Reusable Object-Oriented Software* by Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides (Prentice Hall, 1997). Design patterns provide a programmer with best practices on how objects should interact and which object owns which other kinds of objects. Also, design patterns show how such objects can be grouped together.

However, for procedural programming languages like C, most of these design patterns cannot be implemented in the way described by the Gang of Four. There are no native object-oriented mechanisms in C. It is possible to emulate inheritance or polymorphism in the C programming language, but that might not be the first choice, because such emulation makes things unfamiliar for programmers who are used to programming C and are not used to programming with object-oriented languages like C++ and using concepts like inheritance and polymorphism. Such programmers may want to stick to their native C programming style that they are used to. However, with the native C programming style, not all object-oriented design patterns guidance is usable, or at least the specific implementation of the idea presented in a design pattern is not provided for non-object-oriented programming languages.

And that is where we stand: we want to program in C, but we cannot directly use most of the knowledge documented in design patterns. This book shows how to bridge this gap and implement hands-on design knowledge for the C programming language.

# Why I Wrote This Book

Let me tell you why the knowledge gathered in this book turned out to be very important for me and why such knowledge is hard to find.

In school I learned C programming as my first programming language. Just like every new C programmer, I wondered why arrays start with index 0, and I first rather randomly tried out how to place the operators `*` and `&` in order to finally get the C pointer magic working.

At university I learned how C syntax actually works and how it translates to bits and bytes on the hardware. With that knowledge I was able to write small programs that worked very well. However, I still had trouble understanding why longer code looked the way it did, and I certainly wouldn’t have come up with solutions like the following:

```
typedef struct INTERNAL_DRIVER_STRUCT* DRIVER_HANDLE;
typedef void (*DriverSend_FP)(char byte);
typedef char (*DriverReceive_FP)();
typedef void (*DriverIOCTL_FP)(int ioctl, void* context);

struct DriverFunctions
{
  DriverSend_FP fpSend;
  DriverReceive_FP fpReceive;
  DriverIOCTL_FP fpIOCTL;
};

DRIVER_HANDLE driverCreate(void* initArg, struct DriverFunctions f);
void driverDestroy(DRIVER_HANDLE h);
void sendByte(DRIVER_HANDLE h, char byte);
char receiveByte(DRIVER_HANDLE h);
void driverIOCTL(DRIVER_HANDLE h, int ioctl, void* context);
```

Looking at code like that prompted many questions:

- Why have function pointers in the `struct`?

- Why do the functions need that `DRIVER_HANDLE`?

- What is an IOCTL, and why would I not have separate functions instead?

- Why have explicit create and destroy functions?

These questions came up as I began writing industrial applications. I regularly came across situations where I realized I did not have the C programming knowledge, for example, to decide how to implement an iterator or to decide how to cope with error handling in my functions. I realized that although I knew C syntax, I had no clue how to apply it. I tried to achieve something but just managed to do it in a clumsy way or not at all. What I needed were best practices on how to achieve specific tasks with the C programming language. For example, I needed to know things like the following:

- How can I acquire and release resources in an easy way?

- Is it a good idea to use `goto` for error handling?

- Should I design my interface to be flexible, or should I simply change it when the need arises?

- Should I use an `assert` statement, or should I return an error code?

- How is an iterator implemented in C?

It was very interesting for me to realize that while my experienced work colleagues had many different answers for these questions, nobody could point me to anything that documented these design decisions and their benefits and drawbacks.

So next I turned to the internet, and yet again I was surprised: it was very hard to find sound answers to these questions even though the C programming language has been around for decades. I found out that while there is much literature on the C programming language basics and its syntax, there’s not much on advanced C programming topics or how to write beautiful C code that holds up to industrial applications.

And that is exactly where this book comes in. This book teaches you how to advance your programming skills from writing basic C programs to writing larger-scale C programs that consider error handling and that are flexible regarding certain future changes in requirements and design. This book uses the concept of design patterns to provide you bit by bit with design decisions and their benefits and drawbacks. These design patterns are applied to running code examples that teach you how code like the earlier example evolves and why it ends up looking the way it does.

The presented patterns can be applied to any C programming domains. As I come from the domain of embedded programming in a multithreaded real-time environment, some of the patterns are biased towards that domain. Anyways, you’ll see that the general idea of the patterns can be applied to other C programming domains and even beyond the scope of C programming.

# Patterns Basics

The design guidance in this book is provided in the form of patterns. The idea of presenting knowledge and best practices in the form of patterns comes from the architect Christopher Alexander in *The Timeless Way of Building* (Oxford University Press, 1979). He uses small pieces of well-proven solutions to tackle a huge problem in his domain: how to design and construct cities. The approach of applying patterns was adopted by the software development domain, where pattern conferences like the conference on Pattern Languages of Programs (PLoP) are held to extend the body of knowledge of patterns. In particular, the book *Design Patterns: Elements of Reusable Object-Oriented Software* by the Gang of Four (Prentice Hall, 1997) had a significant impact and made the concept of design patterns well known to software developers.

But what exactly is a pattern? There are many definitions out there, and if you are deeply interested in the topic, then the book *Pattern-Oriented Software Architecture: On Patterns and Pattern Languages* by Frank Buschmann et al. (Wiley, 2007) can provide you with accurate descriptions and details. For the purposes of this book, a pattern provides a well-proven solution to a real-life problem. The patterns presented in this book have the structure shown in [Table P-1](#tab_pattern_sections).

| Pattern section | Description |
|----|----|
| Name | This is the name of the pattern, which should be easy to remember. The aim is that this name will be used by programmers in their everyday language (as is the case with the Gang of Four patterns, where you hear programmers say, “And the Abstract Factory creates the object”). Pattern names are capitalized in this book. |
| Context | The context section sets the scene for the pattern. It tells you under which circumstances this pattern can be applied. |
| Problem | The problem section gives you information about the issue you want to tackle. It starts with the major problem statement written in bold font type and then adds details on why the problem is hard to solve. (In other pattern formats, these details go into a separate section called “forces.”) |
| Solution | This section provides guidance on how to tackle the problem. It starts with stating the main idea of the solution written in bold font type and continues with details about the solution. It also provides a code example in order to give very concrete guidance. |
| Consequences | This section lists the benefits and drawbacks of applying the described solution. When applying a pattern, you should always confirm that the consequences that arise are OK with you. |
| Known uses | The known uses give you evidence that the proposed solution is good and actually works in real-life applications. They also show you concrete examples to help you understand how to apply the pattern. |

Table P-1. How patterns are broken down in this book

A major benefit of presenting design guidance in the form of patterns is that these patterns can be applied one after another. If you have a huge design problem, it’s hard to find the one guidance document and the one solution that addresses exactly that problem. Instead, you can think of your huge and very specific problem as a sum of many smaller and more generic problems, and you can tackle these problems bit by bit by applying one pattern after the other. You simply check the problem descriptions of the patterns and apply the one that fits your problem and that has consequences you can live with. These consequences might lead to another problem that you can then address by applying another pattern. That way you incrementally design your code instead of trying to come up with a complete up-front design before even writing the first line of code.

# How to Read This Book

You should already know C programming basics. You should know the C syntax and how it works—for example, this book won’t teach you what a pointer is or how to use it. This book delivers hints and guidance on advanced topics.

The chapters in this book are self-standing. You can read them in an arbitrary order, and you can simply pick out the topics you are interested in. You’ll find an overview of all patterns in the next section, and from there you can jump to the patterns you are interested in. So if you know exactly what you are looking for, you can start right there.

If you are not looking for one particular pattern, but instead want to get an overview of possible C design options, read through [Part I](Part_01_C_Patterns.md) of the book. Each chapter there focuses on a particular topic, starting with basic topics like error handling and memory managment, and then moving to more advanced and specific topics like interface design or platform-independent code. The chapters each present patterns related to that topic and a running code example that shows bit by bit how the patterns can be applied.

[Part II](Part_02_Pattern_Stories.md) of this book shows two larger running examples that apply many of the patterns from [Part I](Part_01_C_Patterns.md). Here you can learn how to build up some larger piece of software bit by bit through the application of patterns.

# Overview of the Patterns

You’ll find an overview of all patterns presented in this book in Tables [P-2](#tab1a) through [P-10](#tab1i). The tables show a short form of the patterns that only contains a brief description of the core problem, followed by the keyword “Therefore,” followed by the core solution.

| Pattern name | Summary |
|----|----|
| [“Function Split”](Chapter_01_Error_Handling.md) | The function has several responsibilities, which makes the function hard to read and maintain. Therefore, split it up. Take a part of a function that seems useful on its own, create a new function with that, and call that function. |
| [“Guard Clause”](Chapter_01_Error_Handling.md) | The function is hard to read and maintain because it mixes pre-condition checks with the main program logic of the function. Therefore, check if you have mandatory pre-conditions, and immediately return from the function if these pre-conditions are not met. |
| [“Samurai Principle”](Chapter_01_Error_Handling.md) | When returning error information, you assume that the caller checks for this information. However, the caller can simply omit this check and the error might go unnoticed. Therefore, return from a function victorious or not at all. If there is a situation for which you know that an error cannot be handled, then abort the program. |
| [“Goto Error Handling”](Chapter_01_Error_Handling.md) | Code gets difficult to read and maintain if it acquires and cleans up multiple resources at different places within a function. Therefore, have all resource cleanup and error handling at the end of the function. If a resource cannot be acquired, use the `goto` statement to jump to the resource cleanup code. |
| [“Cleanup Record”](Chapter_01_Error_Handling.md) | It is difficult to make a piece of code easy to read and maintain if this code acquires and cleans up multiple resources, particularly if those resources depend on one another. Therefore, call resource acquisition functions as long as they succeed, and store which functions require cleanup. Call the cleanup functions depending on these stored values. |
| [“Object-Based Error Handling”](Chapter_01_Error_Handling.md) | Having multiple responsibilities in one function, such as resource acquisition, resource cleanup, and usage of that resource, makes that code difficult to implement, read, maintain, and test. Therefore, put initialization and cleanup into separate functions, similar to the concept of constructors and destructors in object-oriented programming. |

Table P-2. Patterns for error handling

| Pattern name | Summary |
|----|----|
| [“Return Status Codes”](Chapter_02_Returning_Error_Information.md) | You want to have a mechanism to return status information to the caller, so that the caller can react to it. You want the mechanism to be simple to use, and the caller should be able to clearly distinguish between different error situations that could occur. Therefore, use the Return Value of a function to return status information. Return a value that represents a specific status. Both of you as the callee and the caller must have a mutual understanding of what the value means. |
| [“Return Relevant Errors”](Chapter_02_Returning_Error_Information.md) | On the one hand, the caller should be able to react to errors; on the other hand, the more error information you return, the more your code and the code of your caller have to deal with error handling, which makes the code longer. Longer code is harder to read and maintain and brings in the risk of additional bugs. Therefore, only return error information to the caller if that information is relevant to the caller. Error information is only relevant to the caller if the caller can react to that information. |
| [“Special Return Values”](Chapter_02_Returning_Error_Information.md) | You want to return error information, but it’s not an option to explicitly Return Status Codes because that implies that you cannot use the Return Value of the function to return other data. You’d have to return that data via Out-Parameters, which would make calling your function more difficult. Therefore, use the Return Value of your function to return the data computed by the function. Reserve one or more special values to be returned if an error occurs. |
| [“Log Errors”](Chapter_02_Returning_Error_Information.md) | You want to make sure that in case of an error you can easily find out its cause. However, you don’t want your error-handling code to become complicated because of this. Therefore, use different channels to provide error information that is relevant for the calling code and error information that is relevant for the developer. For example, write debug error information into a log file and don’t return the detailed debug error information to the caller. |

Table P-3. Patterns for returning error information

| Pattern name | Summary |
|----|----|
| [“Stack First”](Chapter_03_Memory_Management.md) | Deciding the storage class and memory section (stack, heap, …) for variables is a decision every programmer has to make often. It gets exhausting if for each and every variable, the pros and cons of all possible alternatives have to be considered in detail. Therefore, simply put your variables on the stack by default to profit from automatic cleanup of stack variables. |
| [“Eternal Memory”](Chapter_03_Memory_Management.md) | Holding large amounts of data and transporting it between function calls is difficult because you have to make sure that the memory for the data is large enough and that the lifetime extends across your function calls. Therefore, put your data into memory that is available throughout the whole lifetime of your program. |
| [“Lazy Cleanup”](Chapter_03_Memory_Management.md) | Having dynamic memory is required if you need large amounts of memory and memory where you don’t know the required size beforehand. However, handling cleanup of dynamic memory is a hassle and is the source of many programming errors. Therefore, allocate dynamic memory and let the operating system cope with deallocation by the end of your program. |
| [“Dedicated Ownership”](Chapter_03_Memory_Management.md) | The great power of using dynamic memory comes with the great responsibility of having to properly clean that memory up. In larger programs, it becomes difficult to make sure that all dynamic memory is cleaned up properly. Therefore, right at the time when you implement memory allocation, clearly define and document where it’s going to be cleaned up and who is going to do that. |
| [“Allocation Wrapper”](Chapter_03_Memory_Management.md) | Each allocation of dynamic memory might fail, so you should check allocations in your code to react accordingly. This is cumbersome because you have many places for such checks in your code. Therefore, wrap the allocation and deallocation calls, and implement error handling or additional memory management organization in these wrapper functions. |
| [“Pointer Check”](Chapter_03_Memory_Management.md) | Programming errors that lead to accessing an invalid pointer cause uncontrolled program behavior, and such errors are difficult to debug. However, because your code works with pointers frequently, there is a good chance that you have introduced such programming errors. Therefore, explicitly invalidate uninitialized or freed pointers and always check pointers for validity before accessing them. |
| [“Memory Pool”](Chapter_03_Memory_Management.md) | Frequently allocating and deallocating objects from the heap leads to memory fragmentation. Therefore, hold a large piece of memory throughout the whole lifetime of your program. At runtime, retrieve fixed-size chunks of that memory pool instead of directly allocating new memory from the heap. |

Table P-4. Patterns for memory management

| Pattern name | Summary |
|----|----|
| [“Return Value”](Chapter_04_Returning_Data_from_C_Functions.md) | The function parts you want to split are not independent from one another. As usual in procedural programming, some part delivers a result that is then needed by some other part. The function parts that you want to split need to share some data. Therefore, simply use the one C mechanism intended to retrieve information about the result of a function call: the Return Value. The mechanism to return data in C copies the function result and provides the caller access to this copy. |
| [“Out-Parameters”](Chapter_04_Returning_Data_from_C_Functions.md) | C only supports returning a single type from a function call, and that makes it complicated to return multiple pieces of information. Therefore, return all the data with a single function call by emulating by-reference arguments with pointers. |
| [“Aggregate Instance”](Chapter_04_Returning_Data_from_C_Functions.md) | C only supports returning a single type from a function call, and that makes it complicated to return multiple pieces of information. Therefore, put all data that is related into a newly defined type. Define this Aggregate Instance to contain all the related data that you want to share. Define it in the interface of your component to let the caller directly access all the data stored in the instance. |
| [“Immutable Instance”](Chapter_04_Returning_Data_from_C_Functions.md) | You want to provide information held in large pieces of immutable data from your component to a caller. Therefore, have an instance (for example, a `struct`) containing the data to share in static memory. Provide this data to users who want to access it and make sure that they cannot modify it. |
| [“Caller-Owned Buffer”](Chapter_04_Returning_Data_from_C_Functions.md) | You want to provide complex or large data of known size to the caller, and that data is not immutable (it changes at runtime). Therefore, require the caller to provide a buffer and its size to the function that returns the large, complex data. In the function implementation, copy the required data into the buffer if the buffer size is large enough. |
| [“Callee Allocates”](Chapter_04_Returning_Data_from_C_Functions.md) | You want to provide complex or large data of unknown size to the caller, and that data is not immutable (it changes at runtime). Therefore, allocate a buffer with the required size inside the function that provides the large, complex data. Copy the required data into the buffer and return a pointer to that buffer. |

Table P-5. Patterns for returning data from C functions

| Pattern name | Summary |
|----|----|
| [“Stateless Software-Module”](Chapter_05_Data_Lifetime_and_Ownership.md) | You want to provide logically related functionality to your caller and make that functionality as easy as possible for the caller to use. Therefore, keep your functions simple and don’t build up state information in your implementation. Put all related functions into one header file and provide the caller this interface to your software-module. |
| [“Software-Module with Global State”](Chapter_05_Data_Lifetime_and_Ownership.md) | You want to structure your logically related code that requires common state information and make that functionality as easy as possible for the caller to use. Therefore, have one global instance to let your related functions share common resources. Put all functions that operate on this instance into one header file, and provide the caller this interface to your software-module. |
| [“Caller-Owned Instance”](Chapter_05_Data_Lifetime_and_Ownership.md) | You want to provide multiple callers or threads access to functionality with functions that depend on one another, and the interaction of the caller with your functions builds up state information. Therefore, require the caller to pass an instance, which is used to store resource and state information, along to your functions. Provide explicit functions to create and destroy these instances, so that the caller can determine their lifetime. |
| [“Shared Instance”](Chapter_05_Data_Lifetime_and_Ownership.md) | You want to provide multiple callers or threads access to functionality with functions that depend on one another, and the interaction of the caller with your functions builds up state information, which your callers want to share. Therefore, require the caller to pass an instance, which is used to store resource and state information, along to your functions. Use the same instance for multiple callers and keep the ownership of that instance in your software-module. |

Table P-6. Patterns for data lifetime and ownership

| Pattern name | Summary |
|----|----|
| [“Header Files”](Chapter_06_Flexible_APIs.md) | You want functionality that you implement to be accessible to code from other implementation files, but you want to hide your implementation details from the caller. Therefore, provide function declarations in your API for any functionality you want to provide to your user. Hide any internal functions, internal data, and your function definitions (the implementations) in your implementation file and don’t provide this implementation file to the user. |
| [“Handle”](Chapter_06_Flexible_APIs.md) | You have to share state information or operate on shared resources in your function implementations, but you don’t want your caller to see or even access all that state information and shared resources. Therefore, have a function to create the context on which the caller operates and return an abstract pointer to internal data for that context. Require the caller to pass that pointer to all your functions, which can then use the internal data to store state information and resources. |
| [“Dynamic Interface”](Chapter_06_Flexible_APIs.md) | It should be possible to call implementations with slightly deviating behaviors, but it should not be necessary to duplicate any code, not even the control logic implementation and interface declaration. Therefore, define a common interface for the deviating functionalities in your API and require the caller to provide a callback function for that functionality, which you then call in your function implementation. |
| [“Function Control”](Chapter_06_Flexible_APIs.md) | You want to call implementations with slightly deviating behaviors, but you don’t want to duplicate any code, not even the control logic implementation or the interface declaration. Therefore, add a parameter to your function that passes meta-information about the function call and that specifies the actual functionality to be performed. |

Table P-7. Patterns for flexible APIs

| Pattern name | Summary |
|----|----|
| [“Index Access”](Chapter_07_Flexible_Iterator_Interfaces.md) | You want to make it possible for the user to iterate elements in your data structure in a convenient way, and it should be possible to change internals of the data structure without resulting in changes to the user’s code. Therefore, provide a function that takes an index to address the element in your underlying data structure and return the content of this element. The user calls this function in a loop to iterate over all elements. |
| [“Cursor Iterator”](Chapter_07_Flexible_Iterator_Interfaces.md) | You want to provide an iteration interface to your user which is robust in case the elements change during the iteration and which enables you to change the underlying data structure at a later point without requiring any changes to the user’s code. Therefore, create an iterator instance that points to an element in the underlying data structure. An iteration function takes this iterator instance as argument, retrieves the element the iterator currently points to, and modifies the iteration instance to point to the next element. The user then iteratively calls this function to retrieve one element at a time. |
| [“Callback Iterator”](Chapter_07_Flexible_Iterator_Interfaces.md) | You want to provide a robust iteration interface which does not require the user to implement a loop in the code for iterating over all elements and which enables you to change the underlying data structure at a later point without requiring any changes to the user’s code. Therefore, use your existing data structure—specific operations to iterate over all your elements within your implementation, and call some provided user-function on each element during this iteration. This user-function gets the element content as a parameter and can then perform its operations on this element. The user calls just one function to trigger the iteration, and the whole iteration takes place inside your implementation. |

Table P-8. Patterns for flexible iterator interfaces

| Pattern name | Summary |
|----|----|
| [“Include Guard”](Chapter_08_Organizing_Files_in_Modular_Programs.md) | It’s easy to include a header file multiple times, but including the same header file leads to compile errors if types or certain macros are part of it, because during compilation they get redefined. Therefore, protect the content of your header files against multiple inclusion so that the developer using the header files does not have to care whether it is included multiple times. Use an interlocked `#ifdef` statement or a `#pragma once` statement to achieve this. |
| [“Software-Module Directories”](Chapter_08_Organizing_Files_in_Modular_Programs.md) | Splitting code into different files increases the number of files in your codebase. Having all files in one directory makes it difficult to keep an overview of all the files, particularly for large codebases. Therefore, put header files and implementation files that belong to a tightly coupled functionality into one directory. Name that directory after the functionality that is provided via the header files. |
| [“Global Include Directory”](Chapter_08_Organizing_Files_in_Modular_Programs.md) | To include files from other software-modules, you have to use relative paths like *../othersoftwaremodule/file.h*. You have to know the exact location of the other header file. Therefore, have one global directory in your codebase that contains all software-module APIs. Add this directory to the global include paths in your toolchain. |
| [“Self-Contained Component”](Chapter_08_Organizing_Files_in_Modular_Programs.md) | From the directory structure it is not possible to see the dependencies in the code. Any software-module can simply include the header files from any other software-module, so it’s impossible to check dependencies in the code via the compiler. Therefore, identify software-modules that contain similar functionality and that should be deployed together. Put these software-modules into a common directory and have a designated subdirectory for their header files that are relevant for the caller. |
| [“API Copy”](Chapter_08_Organizing_Files_in_Modular_Programs.md) | You want to develop, version, and deploy the parts of your codebase independently from one another. However, to do that, you need clearly defined interfaces between the code parts and the ability to separate that code into different repositories. Therefore, to use the functionality of another component, copy its API. Build that other component separately and copy the build artifacts and its public header files. Put these files into a directory inside your component and configure that directory as a global include path. |

Table P-9. Patterns for organizing files in modular programs

| Pattern name | Summary |
|----|----|
| [“Avoid Variants”](Chapter_09_Escaping_ifdef_Hell.md) | Using different functions for each platform makes the code harder to read and write. The programmer is required to initially understand, correctly use, and test these multiple functions in order to achieve a single functionality across multiple platforms. Therefore, use standardized functions that are available on all platforms. If there are no standardized functions, consider not implementing the functionality. |
| [“Isolated Primitives”](Chapter_09_Escaping_ifdef_Hell.md) | Having code variants organized with `#ifdef` statements makes the code unreadable. It is very difficult to follow the program flow, because it is implemented multiple times for multiple platforms. Therefore, isolate your code variants. In your implementation file, put the code handling the variants into separate functions and call these functions from your main program logic, which then contains only platform-independent code. |
| [“Atomic Primitives”](Chapter_09_Escaping_ifdef_Hell.md) | The function that contains the variants and is called by the main program is still hard to comprehend because all the complex `#ifdef` code was only put into this function in order to get rid of it in the main program. Therefore, make your primitives atomic. Only handle exactly one kind of variant per function. If you handle multiple kinds of variants, for example, operating system variants and hardware variants, then have separate functions for that. |
| [“Abstraction Layer”](Chapter_09_Escaping_ifdef_Hell.md) | You want to use the functionality which handles platform variants at several places in your codebase, but you do not want to duplicate the code of that functionality. Therefore, provide an API for each functionality that requires platform-specific code. Define only platform-independent functions in the header file and put all platform-specific `#ifdef` code into the implementation file. The caller of your functions includes only your header file and does not have to include any platform-specific files. |
| [“Split Variant Implementations”](Chapter_09_Escaping_ifdef_Hell.md) | The platform-specific implementations still contain `#ifdef` statements to distinguish between code variants. That makes it difficult to see and select which part of the code should be built for which platform. Therefore, put each variant implementation into a separate implementation file and select per file what you want to compile for which platform. |

Table P-10. Patterns for escaping `#ifdef` hell

# Conventions Used in This Book

The following typographical conventions are used in this book:

*Italic*  
Indicates new terms, URLs, email addresses, filenames, and file extensions.

&nbsp;

**Bold**  
Used to highlight the problem and solution for each pattern.

`Constant width`  
Used for program listings, as well as within paragraphs to refer to program elements such as variable or function names, databases, data types, environment variables, statements, and keywords.

###### Note

This element signifies a general note.

###### Warning

This element indicates a warning or caution.

# Using Code Examples

The code examples in this book show short code snippets which focus on the core idea to showcase the patterns and their application. The code snippets by themselves won’t compile, because to keep it simple several things are omitted (for example, include files). If you are interested in getting the full code which does compile, you can download it from GitHub at [*https://github.com/christopher-preschern/fluent-c*](https://github.com/christopher-preschern/fluent-c).

If you have a technical question or a problem using the code examples, please send email to [*bookquestions@oreilly.com*](mailto:bookquestions@oreilly.com).

This book is here to help you get your job done. In general, if example code is offered with this book, you may use it in your programs and documentation. You do not need to contact us for permission unless you’re reproducing a significant portion of the code. For example, writing a program that uses several chunks of code from this book does not require permission. Selling or distributing examples from O’Reilly books does require permission. Answering a question by citing this book and quoting example code does not require permission. Incorporating a significant amount of example code from this book into your product’s documentation does require permission.

We appreciate, but generally do not require, attribution. An attribution usually includes the title, author, publisher, and ISBN. For example: “*Fluent C* by Christopher Preschern (O’Reilly). Copyright 2023 Christopher Preschern, 978-1-492-09733-4.”

If you feel your use of code examples falls outside fair use or the permission given above, feel free to contact us at [*permissions@oreilly.com*](mailto:permissions@oreilly.com).

The patterns in this book all present existing code examples which apply these patterns. The following list shows the references to these code examples:

- [The game NetHack](https://oreil.ly/nzO5W)

- [OpenWrt Project](https://oreil.ly/qeppo)

- [OpenSSL library](https://oreil.ly/zzsMO)

- [Wireshark network sniffer](https://oreil.ly/M55B5)

- [Portland Pattern repository](https://oreil.ly/wkZzb)

- [Git version control system](https://oreil.ly/7F9Oz)

- [Apache Portable Runtime](https://oreil.ly/ysaM6)

- [Apache Webserver](https://oreil.ly/W6SMn)

- B&R Automation Runtime operating system (proprietary and undisclosed code of the company B&R Industrial Automation GmbH)

- B&R Visual Components automation system visualization editor (proprietary and undisclosed code of the company B&R Industrial Automation GmbH)

- [NetDRMS data management system](https://oreil.ly/eR0EV)

- [MATLAB programming and numeric computing platform](https://oreil.ly/UpvJK)

- [GLib library](https://oreil.ly/QoUwT)

- [GoAccess real-time web analyzer](https://oreil.ly/L1Eij)

- [Cloudy physical calculation software](https://oreil.ly/phLBb)

- [GNU Compiler Collection (GCC)](https://oreil.ly/KK4jY)

- [MySQL database system](https://oreil.ly/YKXxs)

- [Android ION memory manager](https://oreil.ly/2JV7h)

- [Windows API](https://oreil.ly/nnzyX)

- [Apple’s Cocoa API](https://oreil.ly/sQuaI)

- [VxWorks real-time operating system](https://oreil.ly/UMUaj)

- [sam text editor](https://oreil.ly/k3SQI)

- [C standard library functions: glibc implementation](https://oreil.ly/9Qr95)

- [Subversion project](https://oreil.ly/sg9sz)

- [Netdata real-time performance monitoring and visualization system](https://oreil.ly/1sDZz)

- [Nmap network tool](https://oreil.ly/8Yz5R)

- [OpenZFS file system](https://oreil.ly/VWeQL)

- [RIOT operating system](https://oreil.ly/LhZM4)

- [Radare reverse engineering framework](https://oreil.ly/TUYfh)

- [Education First digital learning products](https://www.ef.com)

- [VIM text editor](https://github.com/vim/vim)

- [GNUplot graphing utility](https://oreil.ly/PlQPj)

- [SQLite database engine](https://oreil.ly/5Knfz)

- [gzip data compression program](https://oreil.ly/it40Z)

- [lighttpd web server](https://github.com/lighttpd)

- [U-Boot bootloader](https://oreil.ly/IKVYV)

- [Smpl discrete event simulation system](https://oreil.ly/NJnCH)

- [Nokia’s Maemo platform](https://oreil.ly/RwDtt)

# O’Reilly Online Learning

###### Note

For more than 40 years, [*O’Reilly Media*](https://oreilly.com) has provided technology and business training, knowledge, and insight to help companies succeed.

Our unique network of experts and innovators share their knowledge and expertise through books, articles, and our online learning platform. O’Reilly’s online learning platform gives you on-demand access to live training courses, in-depth learning paths, interactive coding environments, and a vast collection of text and video from O’Reilly and 200+ other publishers. For more information, visit [*https://oreilly.com*](https://oreilly.com).

# How to Contact Us

Please address comments and questions concerning this book to the publisher:

- O’Reilly Media, Inc.
- 1005 Gravenstein Highway North
- Sebastopol, CA 95472
- 800-998-9938 (in the United States or Canada)
- 707-829-0515 (international or local)
- 707-829-0104 (fax)

We have a web page for this book, where we list errata, examples, and any additional information. You can access this page at [*https://oreil.ly/fluent-c*](https://oreil.ly/fluent-c).

Email [*bookquestions@oreilly.com*](mailto:bookquestions@oreilly.com) to comment or ask technical questions about this book.

For news and information about our books and courses, visit [*https://oreilly.com*](https://oreilly.com).

Find us on LinkedIn: [*https://linkedin.com/company/oreilly-media*](https://linkedin.com/company/oreilly-media)

Follow us on Twitter: [*https://twitter.com/oreillymedia*](https://twitter.com/oreillymedia)

Watch us on YouTube: [*https://www.youtube.com/oreillymedia*](https://www.youtube.com/oreillymedia)

# Acknowledgments

I want to thank my wife Silke who by now even knows what patterns are :-) and I want to thank my daughter Ylvi. They both make my life happier, and they both make sure that I don’t end up sitting in front of my computer working all the time, but that I instead enjoy life.

This book would not have come to life without the help of many pattern enthusiasts. I want to thank all the participants of Writers’ Workshops at the European Conference on Pattern Languages of Programs for providing me with feedback on the patterns. In particular, I want to thank the following people, who provided me with very helpful feedback during the so-called shepherding process of that conference: Jari Rauhamäki, Tobias Rauter, Andrea Höller, James Coplien, Uwe Zdun, Thomas Raser, Eden Burton, Claudius Link, Valentino Vranić, and Sumit Kalra. Special thanks also to my work colleagues, in particular to Thomas Havlovec, who made sure that I got the C programming details in my patterns right. Robert Hanmer, Michael Weiss, David Griffiths, and Thomas Krug spent a lot of time for reviewing this book and provided me with additional ideas how to improve it—thank you very much! Thanks also to the whole team at O’Reilly who helped me a lot in making this book happen. In particular, I want to thank my development editor, Corbin Collins, and my production editor, Jonathon Owen.

The content of this book is based on the following papers that were accepted at the European Conference on Pattern Languages of Programs and published with ACM. These papers can be accessed for free at the website [*http://www.preschern.com*](http://www.preschern.com).

- “A Pattern Story About C Programming,” EuroPLoP ’21: 26th European Conference on Pattern Languages of Programs, July 2015, article no. 53, 1–10, [*https://dl.acm.org/doi/10.1145/3489449.3489978*](https://dl.acm.org/doi/10.1145/3489449.3489978).

- “Patterns for Organizing Files in Modular C Programs,” EuroPLoP ’20: Proceedings of the European Conference on Pattern Languages of Programs, July 2020, article no. 1, 1–15, [*https://dl.acm.org/doi/10.1145/3424771.3424772*](https://dl.acm.org/doi/10.1145/3424771.3424772).

- “Patterns to Escape the \#ifdef Hell,” EuroPLop ’19: Proceedings of the 24th European Conference on Pattern Languages of Programs, July 2019, article no. 2, 1–12, [*https://dl.acm.org/doi/10.1145/3361149.3361151*](https://dl.acm.org/doi/10.1145/3361149.3361151).

- “Patterns for Returning Error Information in C,” EuroPLop ’19: Proceedings of the 24th European Conference on Pattern Languages of Programs, July 2019, article no. 3, 1–14, [*https://dl.acm.org/doi/10.1145/3361149.3361152*](https://dl.acm.org/doi/10.1145/3361149.3361152).

- “Patterns for Returning Data from C Functions,” EuroPLop ’19: Proceedings of the 24th European Conference on Pattern Languages of Programs, July 2019, article no. 37, 1–13, [*https://dl.acm.org/doi/10.1145/3361149.3361188*](https://dl.acm.org/doi/10.1145/3361149.3361188).

- “C Patterns on Data Lifetime and Ownership,” EuroPLop ’19: Proceedings of the 24th European Conference on Pattern Languages of Programs, July 2019, article no. 36, 1–13, [*https://dl.acm.org/doi/10.1145/3361149.3361187*](https://dl.acm.org/doi/10.1145/3361149.3361187).

- “Patterns for C Iterator Interfaces,” EuroPLoP ’17: Proceedings of the 22nd European Conference on Pattern Languages of Programs, July 2017, article no. 8, 1–14, [*https://dl.acm.org/doi/10.1145/3147704.3147714*](https://dl.acm.org/doi/10.1145/3147704.3147714).

- “API Patterns in C,” EuroPlop ’16: Proceedings of the 21st European Conference on Pattern Languages of Programs, July 2016, article no. 7, 1–11, [*https://dl.acm.org/doi/10.1145/3011784.3011791*](https://dl.acm.org/doi/10.1145/3011784.3011791).

- “Idioms for Error Handling in C,” EuroPLoP ’15: Proceedings of the 20th European Conference on Pattern Languages of Programs, July 2015, article no. 53, 1–10, [*https://dl.acm.org/doi/10.1145/2855321.2855377*](https://dl.acm.org/doi/10.1145/2855321.2855377).

