# Chapter 6. Flexible APIs

Designing interfaces with the right level of flexibility and the right level of abstraction is one of the most important things when writing software, because interfaces represent a contract that often cannot be changed once the system is in operation. Because of this it is important to put stable declarations into the interface and to abstract implementation details, which should have the flexibility to change at a later point in time.

For object-oriented programming languages, you’ll find much guidance on how to design interfaces (for example, in the form of design patterns), but there is not much guidance of this kind for procedural programming languages like C. There are the SOLID design principles (see nearby sidebar) that tell you in general how to design good software. However, for the C programming language, detailed design guidance on how to design interfaces is hard to find, and that’s where the patterns from this chapter come in.

##### SOLID

The SOLID principles tell us how to implement good, flexible, and maintainable software.

**S**ingle-responsibility principle  
The code has one responsibility and one reason to be changed in the future.

**O**pen-closed principle  
Code should be open for behavior changes without requiring changes to the existing code.

**L**iskow substitution principle  
Codes that implement the same interface should be interchangable for the caller.

**I**nterface segregation principle  
Interfaces should be slim and tailored for the caller’s needs.

**D**ependency inversion principle  
High-level modules should be independent from low-level modules.

The article [“SOLID Design for Embedded C”](https://oreil.ly/xrCtb) by James Grenning gives you more details on how to implement the SOLID principles in C.

[Figure 6-1](#overview_flexible_api) shows the four patterns covered in this chapter, as well as related patterns, and [Table 6-1](#tab_flexible_api) contains a short description of the four patterns. Keep in mind that not all of the patterns should always be applied in all possible contexts. Generally it is advisable to design a system to not be more complex than it has to be. This means that some of the presented patterns should only be applied if the gained flexibility is already required by your API or will likely be required in the future. If it is not likely to be required, then the pattern should perhaps not be applied to keep the API as simple as possible.

![Overview of the patterns on flexible APIs](images/fluc_0601.png)

###### Figure 6-1. Overview of patterns for flexible APIs

|  | Pattern name | Summary |
|----|----|----|
|  | Header Files | You want a functionality that you implement to be accessible to code from other implementation files, but you want to hide your implementation details from the caller. Therefore, provide function declarations in your API for any functionality you want to provide to your user. Hide any internal functions, internal data, and your function definitions (the implementations) in your implementation file and don’t provide this implementation file to the user. |
|  | Handle | You have to share state information or operate on shared resources in your function implementations, but you don’t want your caller to see or even access all that state information and shared resources. Therefore, have a function to create the context on which the caller operates and return an abstract pointer to internal data for that context. Require the caller to pass that pointer to all your functions, which can then use the internal data to store state information and resources. |
|  | Dynamic Interface | It should be possible to call implementations with slightly deviating behaviors, but it should not be necessary to duplicate any code, not even the control logic implementation and interface declaration. Therefore, define a common interface for the deviating functionalities in your API and require the caller to provide a callback function for that functionality, which you then call in your function implementation. |
|  | Function Control | You want to call implementations with slightly deviating behaviors, but you don’t want to duplicate any code, not even the control logic implementation or the interface declaration. Therefore, add a parameter to your function that passes meta-information about the function call and that specifies the actual functionality to be performed. |

Table 6-1. Patterns for flexible APIs

As a running example, in this chapter you want to implement a device driver for your Ethernet network interface card. The firmware of this card provides several registers with which you can send or receive data and with which you can configure the card. You want to build some abstraction of these hardware details, and you want to make sure that a user of your API is not affected if you change some parts of your implementation. To achieve this, you build an API consisting of Header Files.

# Header Files

## Context

You write a larger piece of software in C. You split that software up into several functions, and you implement these functions in several files because you want to make your program modular and easy to maintain.

## Problem

**You want a functionality that you implement to be accessible to code from other implementation files, but you want to hide your implementation details from the caller.**

Unlike many object-oriented languages, C does not provide any built-in support for defining APIs, abstracting functionality, or enforcing that the caller can only access this abstraction. C only provides a mechanism to include files into other files.

The caller of your code could use that mechanism to simply include your implementation file. But then the caller could access all internal data in that file, such as variables or functions with file scope that you only intend to use internally. Once the caller uses this internal functionality, it might not be easy to change it later on, so the code becomes tightly coupled in places where you might not want that to happen. If the caller includes the implementation file, the names of the internal variables and functions might clash with names used by the caller.

## Solution

**Provide function declarations in your API for any functionality you want to provide to your user. Hide any internal functions, internal data, and your function definitions (the implementations) in your implementation file and don’t provide this implementation file to the user.**

In C, it is a common convention that anybody who uses functions of your software only uses functions defined in your header file (*\*.h* file) and does not use other functions in your implementation (your *\*.c* files). In some cases, this abstraction can be partially enforced (for example, you cannot use a `static` function from another file), but the C language does not support such enforcements to the full extent. Therefore, the convention of not accessing other implementation files is even more important than the enforcement mechanisms.

Within the header file, make sure to include all related artifacts needed by your functions in the header file. It should not be neccessary for your caller to include other header files in order to be able to use the functionality from your header file. If you have common declarations (like data types or `#defines`) that are needed in multiple header files, then put these declarations into a separate header file and include it in the other header files that need the declarations. To ensure that the header files are not included multiple times in a compilation unit, protect them with Include Guards.

Only put functions into the same header file if they are related. If the functions operate on the same Handle or perform an operation in the same domain (like math calculations), then that is an indicator to put them into the same header file. In general, if you can think of a relevant use case that requires all of the functions, then you should put them into the same header file.

Clearly document the behavior of your API in the header file. The user should not be required to have a look at the implementation in order to understand how the functions provided in the API work.

The following code shows an example of a Header File:

*API (h-file)*

```
/* Sorts the numbers of the 'array' in ascending order.
   'length' defines the number of elements in the 'array'. */
void sort(int* array, int length);
```

\
*Implementation (c-file)*

```
void sort(int* array, int length)
{
  /* here goes the implementation*/
}
```

## Consequences

You have a very clear separation between the things relevant for your caller (the *\*.h* file) and the implementation details that the caller does not have to care about (the *\*.c* file). Thus, you abstracted some functionality for the caller.

Having many header files will influence your build times. On the one hand this enables you to split your implementations into separate files, and your toolchain will be able to have an incremental build that only rebuilds files that changed. On the other hand, a complete rebuild will have slightly increased build times compared to having all the code in one file, because all the files have to be opened and read for the build.

If you discover that your functions require more interaction between one another or that they have to be called in different contexts that require different internal state information, then you have to think about how to realize that with your API. A Handle can help in such cases.

The caller of your functions now relies on the abstraction and might rely on the fact that the behavior of these functions does not change. The API might have to be kept stable. To add new functionality, you can always add new functions to the API. But in some cases you might want to extend existing functions, and to be able to cope with such future changes, you have to consider how to make your functions flexible while keeping them stable. Handles, Dynamic Interfaces, or Function Controls can help in such cases.

## Known Uses

The following examples show applications of this pattern:

- Pretty much every C program that is larger than a simple “Hello World” program contains header files.

- Using a header file in C is analogous to using interfaces in Java or abstract classes in C++.

- The Pimpl Idiom describes how to hide private implementation details and not put them into the header file. You can find a description of that idiom in the Portland Pattern Repository.

## Applied to Running Example

Your first device driver API looks like the following:

```
void sendByte(char byte);
char receiveByte();
void setIpAddress(char* ip);
void setMacAddress(char* mac);
```

The user of your API does not have to cope with implementation details like how you access Ethernet registers, and you are free to change these details without affecting the user.

Now your requirements for your driver change. Your system has a second, identical Ethernet network interface card, and it should be possible to operate both of them. Here are two straightforward options to achieve this:

- You copy your code and have one piece of code for each network interface card. In the copied code, you only modify the address of the exact interface to be accessed. However, such code duplication is never a good idea and makes maintenance of your code much more difficult.

- You add a parameter to address the network interface card (for example, a device name string) to each function. But it’s quite likely that more than just one parameter will have to be shared between the functions, and passing each of them to every function makes the usage of your API cumbersome.

A better idea to support multiple Ethernet network interface cards is to introduce Handles to your API.

# Handle

## Context

You want to provide a set of functions to your caller, and these functions operate on shared resources or they share state information.

## Problem

**You have to share state information or operate on shared resources in your function implementations, but you don’t want your caller to see or even access all that state information and shared resources.**

That state information and shared resources should remain invisible to your caller because later on you might want to change it or add to it without requiring any changes to your caller’s code.

In object-oriented programming languages, such data on which functions can operate is realized by class member variables. These class member variables can be made private if the caller should not be able to access them. However, C does not natively support classes and private member variables.

Simply having a Software-Module with Global State holding static global variables in your implementation file for storing shared data between your functions is not an option for you, because it should be possible to call your functions in multiple contexts. The function calls for each of your callers should be able to build up their state information. And even though that information should remain invisible to your callers, you need a way to identify which information belongs to which specific caller and how to access that information in your function implementations.

## Solution

**Have a function to create the context on which the caller operates and return an abstract pointer to internal data for that context. Require the caller to pass that pointer to all your functions, which can then use the internal data to store state information and resources.**

Your functions know how to interpret this abstract pointer, which is an opaque data type also called Handle. However, the data structure that you point to should not be part of the API. The API only provides the functionality to relay hidden data to the functions.

The Handle can be implemented as a pointer to an Aggregate Instance like a `struct`. The `struct` should contain all required state information or other variables—it usually holds variables similar to those you would declare as member variables for objects in object-oriented programming. The `struct` should be hidden in your implementation. The API only contains the definition of a pointer to the `struct` as shown in the following code:

*API*

```
typedef struct SORT_STRUCT* SORT_HANDLE;

SORT_HANDLE prepareSort(int* array, int length);
void sort(SORT_HANDLE context);
```

\
*Implementation*

```
struct SORT_STRUCT
{
  int* array;
  int length;
  /* other parameters like sort order */
};

SORT_HANDLE prepareSort(int* array, int length)
{
  struct SORT_STRUCT* context = malloc(sizeof(struct SORT_STRUCT));
  context->array = array;
  context->length = length;

  /* fill context with required data or state information */

  return context;
}

void sort(SORT_HANDLE context)
{
  /* operate on context data */
}
```

Have one function in your API for creating a Handle. That function returns the Handle to the caller. The caller can then call other functions of your API that require the Handle. In most cases, you also need a function to delete the Handle by cleaning up all the allocated resources.

## Consequences

You can now share state information and resources between your functions without requiring the caller to worry about it and without giving the caller the opportunity to make the code depend on these internals.

Multiple instances of data are supported. You can call the function that creates the Handle multiple times to obtain multiple contexts, and then you can work with these contexts independently from one another.

If your functions that operate on the Handle are changed at a later point in time and have to share different or additional data, the members of the `struct` can simply be changed without requiring any changes to the caller’s code.

The declarations of your functions explicitly show that they are tightly coupled, because they all require the Handle. This makes it, on one hand, easy to see which functions should go into the same Header File, and on the other hand, makes it very easy for the caller to spot which functions should be applied together.

With the Handle, you now require the caller to provide one additional parameter to all function calls, and each additional parameter makes the code harder to read.

## Known Uses

The following examples show applications of this pattern:

- The C standard library contains the definition of `FILE` in *stdio.h*. This `FILE` is defined in most implementations as a pointer to a `struct`, and the `struct` is not part of the header file. The `FILE` handle is created by the function `fopen`, and several other functions can then be called for an opened file (`fwrite`, `fread`, etc.).

- The `struct` `AES_KEY` in the OpenSSL code is used to exchange the context between several functions related to AES encryption (`AES_set_decrypt_key`, `AES_​set_​encrypt_​key`). The `struct` and its members are not hidden in the implementation, but instead they are part of the header file because some parts of other OpenSSL code need to know the size of the `struct`.

- The code for the logging functionality of the Subversion project operates on a Handle. The `struct` `logger_t` is defined in the implementation file of the logging functionality, and a pointer to this `struct` is defined in the corresponding header file.

- This pattern is described in *C Interfaces and Implementations* by David R. Hanson (Addison-Wesley, 1996) as Opaque Pointer Type and in *Patterns in C* by Adam Tornhill (Leanpub, 2014) as “First Class Abstract Data Type Pattern.”

## Applied to Running Example

You can now support as many Ethernet interface cards as you want. Each created instance of your driver produces its own data-context that is then passed to the functions via the Handle. Now you have the following code for your device driver API:

```
/* the INTERNAL_DRIVER_STRUCT contains data shared by the functions (like
   how to select the interface card the driver is responsible for) */
typedef struct INTERNAL_DRIVER_STRUCT* DRIVER_HANDLE;

/* 'initArg' contains information for the implementation to identify
   the exact interface for the driver instance */
DRIVER_HANDLE driverCreate(void* initArg);
void driverDestroy(DRIVER_HANDLE h);
void sendByte(DRIVER_HANDLE h, char byte);
char receiveByte(DRIVER_HANDLE h);
void setIpAddress(DRIVER_HANDLE h, char* ip);
void setMacAddress(DRIVER_HANDLE h, char* mac);
```

Your requirements have changed again. Now you have to support multiple different Ethernet network interface cards, for example, from different vendors. The cards provide similar functionality, but they differ in the details of how the registers have to be accessed, and thus different implementations for the drivers are needed. Two straightforward options to support this would be as follows:

- You have two separate driver APIs. This approach has the drawback that it is cumbersome for the users to build mechanisms for selecting the driver at runtime. Also, having two separate APIs duplicates code because the two device drivers at minimum share a common control flow (for example, for creating or destroying the driver).

- You add functions like `sendByteDriverA` and `sendByteDriverB` to your API. However, you usually want your API to be rather minimal because having all driver functions in a single API can be confusing for the API user. Also, the user’s code depends on all function signatures included via your API, and if code depends on something, that something should be rather minimal (as stated by the interface segregation principle).

A better idea to support different Ethernet network interface cards is to provide a Dynamic Interface.

# Dynamic Interface

## Context

You or your caller want to implement multiple functionalities that follow a similar control logic, but that deviate in their behavior.

## Problem

**It should be possible to call implementations with slightly deviating behaviors, but it should not be necessary to duplicate any code, not even the control logic implementation and interface declaration.**

You want to be able to add additional implementation behaviors to the declared interface later on, without requiring callers who use the existing implementation behaviors to change anything in their code.

Maybe you do not only want to provide differing behaviors to your caller without duplicating your own code, but you also want to provide the callers a mechanism to bring in their own implementation behaviors.

## Solution

**Define a common interface for the deviating functionalities in your API and require the caller to provide a callback function for that functionality, which you then call in your function implementation.**

To implement such an interface in C, define function signatures in your API. The caller then implements functions according to these signatures and attaches them via function pointers. They can either be attached and stored permanently inside your software-module or they can be attached with each function call as shown in the following code:

*API*

```
/* The compare function should return true if x is smaller than y, else false */
typedef bool (*COMPARE_FP)(int x, int y);

void sort(COMPARE_FP compare, int* array, int length);
```

\
*Implementation*

```
void sort(COMPARE_FP compare, int* array, int length)
{
  int i, j;
  for(i=0; i<length; i++)
  {
    for(j=i; j<length; j++)
    {
      /* call provided user function */
      if(compare(array[i], array[j]))
      {
        swap(&array[i], &array[j]);
      }
    }
  }
}
```

*Caller*

```
#define ARRAY_SIZE 4

bool compareFunction(int x, int y)
{
  return x<y;
}

void sortData()
{
  int array[ARRAY_SIZE] = {3, 5, 6, 1};
  sort(compareFunction, array, ARRAY_SIZE);
}
```

Make sure to clearly document, next to the definition of the function signature, what behavior the function implementations should have. Also, document the behavior in case no such function implementation is attached to your function call. Maybe then you’d abort the program (Samurai Principle) or maybe you’d provide some default functionalty as fallback.

## Consequences

The caller can use different implementations and there is still no code duplication. Neither the control logic, the interface, nor the interface documentation is duplicated.

Implementations can be added by the caller at a later point in time without changing the API. This means that the role of the API designer and the implementation provider can be completely separated.

In your code, you now execute the caller’s code. Thus, you must trust that the caller knows what the function has to do. In case of bugs in your caller’s code, it might still happen that your code will initially be suspected because, after all, the faulty behavior occurs in the context of your code.

Using function pointers implies that you have a platform-specific and programming-language-specific interface. You can use this pattern only if the caller’s code is also written in C. You cannot add marshaling functionality to this interface and provide it to a caller who is, for example, writing applications with Java code.

## Known Uses

The following examples show applications of this pattern

- James Grenning describes this pattern and a variant as Dynamic Interface and Per-Type Dynamic Interface in the article [“SOLID Design for Embedded C”](https://oreil.ly/kGZVG).

- The presented solution is a C-version of the Strategy design pattern. You can find alternative C implementations of that pattern in the books *Patterns in C* by Adam Tornhill (Leanpub, 2014) and *C Interfaces and Implementations* by David R. Hanson (Addison-Wesley, 1996).

- Device driver frameworks often use function pointers where the driver inserts its function at startup. The device drivers in the Linux kernel usually work that way.

- The function `svn_sort__hash` of the source code of the Subversion project sorts a list according to some key value. The function takes the function pointer `comparison_func` as a parameter. The `comparison_func` has to return information, namely, which of two provided key values is greater than the other.

- The OpenSSL function `OPENSSL_LH_new` creates a hash table. The caller has to provide a function pointer to a hash function that is used as a callback when operating on the hash table.

- The Wireshark code contains the function pointer `proto_tree_foreach_func` that is provided as a function parameter when traversing tree structures. The function pointer is used to decide which actions to perform on the tree elements.

## Applied to Running Example

Your driver API now supports multiple different Ethernet network interface cards. The specific drivers for these network interface cards have to implement the send and receive functions and provide them in a separate header file. The API user can then include and attach these specific send and receive functions to the API.

You have the benefit that users of your API can bring in their own driver implementation. Thus, you as the API designer are independent from the provider of the driver implementation. Integrating new drivers does not require any API changes, which means it does not require any work from you as the API designer. All that is possible with the following API:

```
typedef struct INTERNAL_DRIVER_STRUCT* DRIVER_HANDLE;
typedef void (*DriverSend_FP)(char byte);      /* this is the           */
typedef char (*DriverReceive_FP)();            /* interface definition */

struct DriverFunctions
{
  DriverSend_FP fpSend;
  DriverReceive_FP fpReceive;
};

DRIVER_HANDLE driverCreate(void* initArg, struct DriverFunctions f);
void driverDestroy(DRIVER_HANDLE h);
void sendByte(DRIVER_HANDLE h, char byte);   /* internally calls fpSend    */
char receiveByte(DRIVER_HANDLE h);           /* internally calls fpReceive */
void setIpAddress(DRIVER_HANDLE h, char* ip);
void setMacAddress(DRIVER_HANDLE h, char* mac);
```

Again, the requirements changed. Now you don’t just have to support Ethernet network interface cards, but also other interface cards (like USB interface cards). From the view of the API, these interfaces have some similar functionalities (the send and receive data functions), but they also have some completely different functionalities (for example, a USB interface has no IP address to set, but might require other configurations).

A straightforward solution for this would be to provide two different APIs for the different driver types. But this would duplicate code for the send/receive and create/destroy functions.

A better solution to support different kinds of device drivers in a single abstract API is to introduce Function Control.

# Function Control

## Context

You want to implement multiple functionalities that follow a similar control logic, but that deviate in their behavior.

## Problem

**You want to call implementations with slightly deviating behaviors, but you don’t want to duplicate any code, not even the control logic implementation or the interface declaration.**

The caller should be able to use specific existing behaviors that you implemented. It should even be possible for you to add new behaviors later on without touching the existing implementations and without requiring changes to the existing caller’s code.

Having a Dynamic Interface is not an option for you because you do not want to offer the callers the flexibility of attaching their own implementation. That might be because the interface should be easier to use for the caller. Or it might be because you cannot easily attach the implementations of your caller, which is the case if your caller, for example, uses another programming language to access your functionality.

## Solution

**Add a parameter to your function that passes meta-information about the function call and that specifies the actual functionality to be performed.**

Compared to a Dynamic Interface, you do not require the caller to provide the implementation, but instead the caller selects from existing implementations.

To implement this pattern, you apply data-based abstraction by adding an additional parameter (for example, an `enum` or `#define` integer value) that specifies the function’s behavior. The parameter is then evaluated in the implementation, and depending on the value of the parameter, different implementations are called:

*API*

```
#define QUICK_SORT 1
#define MERGE_SORT 2
#define RADIX_SORT 3

void sort(int algo, int* array, int length);
```

\
*Implementation*

```
void sort(int algo, int* array, int length)
{
  switch(algo)
  {
    case QUICK_SORT: 
      quicksort(array, length);
    break;
    case MERGE_SORT:
      mergesort(array, length);
    break;
    case RADIX_SORT:
      radixsort(array, length);
    break;
  }
}
```

[![1](images/1.png)](#co_flexible_apis_CO1-1)  
When adding new functionality at a later point in time, you can simply add a new `enum` or `#define` value and select the corresponding new implementation.

## Consequences

The caller can use different implementations and there is still no code duplication. Neither the control logic, the interface, nor the interface documentation is duplicated.

It is easy to add new functionality at a later time. Existing implementations do not have to be touched to do that, and the existing caller’s code is not affected by the change.

Compared to Dynamic Interface, this pattern is easier for selecting functionalities across different programs or platforms (for example, remote procedure calls) because no program-specific pointers are passed via the API.

When providing the selection of different implementation behaviors in one function, you might be tempted to pack multiple functionalities that do not closely belong together into a single function. This violates the single-responsibility principle.

## Known Uses

The following examples show applications of this pattern:

- Device drivers often use Function Control to pass specific functionalities that do not fit into common init/read/write functions. For device drivers this pattern is commonly known as I/O-Control. That concept is described in the book *Making Embedded Systems: Design Patterns for Great Software* by Elecia White (O’Reilly, 2011).

- Some Linux syscalls were extended to have flags that extend the syscalls’ functionality depending on the value of the flag without breaking old code.

- The concept of data-driven APIs in general is described in the book *API Design for *C++** by Martin Reddy (Morgan Kaufmann, 2011).

- The OpenSSL code uses the function `CTerr` to log errors. This function takes an `enum` parameter to specify how and where the error should be logged.

- The POSIX socket function `ioctl` takes a numeric parameter `cmd` that determines which actual action will be performed on a socket. The allowed values for the parameter are defined and documented in a header file, and since the first release of that header file, many additional values and thus function behaviors were added.

- The function `svn_fs_ioctl` of the Subversion project performs some filesystem-specific input or output operations. The function takes the `struct` `svn_fs_ioctl_code_t` as a parameter. This `struct` contains a numeric value that determines which kind of operation should be performed.

## Applied to Running Example

The following code shows the final version of your device driver API:

*Driver.h*

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
/* the parameter "context" is required to pass information like the
   value of the IP address to configure to the implementation */
```

\
*EthIOCTL.h*

```
#define SET_IP_ADDRESS  1
#define SET_MAC_ADDRESS 2
```

\
*UsbIOCTL.h*

```
#define SET_USB_PROTOCOL_TYPE   3
```

Users who want to use the Ethernet- or USB-specific functions (for example, the application actually sending or receiving data via the interface) have to know which driver type they operate on in order to call the right I/O-control and also have to include the *EthIOCTL.h* or *UsbIOCTL.h* files.

[Figure 6-2](#fig_func_ctl) shows the include-relationships of the source code files of this final version of our device driver API. Note that the *EthApplication.c* code does not depend on USB-specific header files. If, for example, an additional USB-IOCTL is added, the *EthApplication.c* shown in the code does not even need to be recompiled, because none of the files it depends on are changed.

![sketches/function-control.png](images/fluc_0602.png)

###### Figure 6-2. File relationships for function control

Keep in mind that of all the code snippets presented in this chapter, this last, most flexible code snippet of the device drivers might not always be what you are looking for. You buy increased flexibility with complexity of your interface, and while you have to make your code as flexible as needed, you should also always try to keep it as simple as possible.

# Summary

This chapter discussed four API patterns for C and showed their application in a running example of how to design a device driver. Header Files tells you the basic concept of hiding implementation details in c-files while providing a well-defined interface in your h-files. The pattern Handle is about the well-known concept of passing opaque data types between functions to share state information. Dynamic Interface makes it possible to not duplicate program logic by allowing the injection of caller-specific code via a callback function. Function Control uses an additional function parameter that specifies the actual action that should be performed by the function call. These patterns showed basic C design options to make an interface more flexible by introducing abstractions.

# Further Reading

If you’re ready for more, here are some resources that can help you further your knowledge of designing APIs.

- The article [“SOLID Design for Embedded C”](https://oreil.ly/07SUX) by James Grenning covers the five SOLID design principles in general and presents ways to implement flexibility for C interfaces. What makes this article unique is that it is the only article that covers the topic of interfaces specifically for C and also includes detailed code snippets.

- The book *Patterns in C* by Adam Tornhill (Leanpub, 2014) presents several patterns that include C code snippets. The patterns include C versions of Gang of Four patterns like Strategy or Observer as well as C-specific patterns and idioms. The book does not explicitly focus on interfaces, but some of the patterns describe interactions on an interface level.

- The book *API Design for *C++** by Martin Reddy (Morgan Kaufmann, 2011) covers design principles for interfaces, object-oriented interface patterns with C++ examples, and interface quality issues with interfaces like testing and documentation. The book addresses C++ design, but some parts of the book are also relevant for C.

- The book *C Interfaces and Implementations* by David R. Hanson (Addison-Wesley, 1996) presents interface design, including C code for specific components implemented in C.

# Outlook

The next chapter goes into detail on how to find the right level of abstraction and the right interface for one very specific kind of application: it describes how to design and implement iterators.

