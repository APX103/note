# Chapter 9. Escaping \#ifdef Hell

C is widespread, in particular with systems where high-performance or hardware-near programming is required. With hardware-near programming comes the necessity of dealing with hardware variants. Aside from hardware variants, some systems support multiple operating systems or cope with multiple product variants in the code. A commonly used approach to addressing these issues is to use `#ifdef` statements of the C preprocessor to distinguish variants in the code. The C preprocessor comes with this power, but with this power also comes the responsibility to use it in a well-structured way.

However, that is where the weakness of the C preprocessor with its `#ifdef` statements shows up. The C preprocessor does not support any methods to enforce rules regarding its usage. That is a pity, because it can very easily be abused. It is very easy to add another hardware variant or another optional feature in the code by adding yet another `#ifdef`. Also, `#ifdef` statements can easily be abused to add quick bug fixes that only affect a single variant. That makes the code for different variants more diverse and leads to code that increasingly has to be fixed for each of the variants separately.

Using `#ifdef` statements in such an unstructured and ad-hoc way is the certain path to hell. The code becomes unreadable and unmaintainable, which all developers should avoid. This chapter presents approaches to escape from such a situation or avoid it altogether.

This chapter gives detailed guidance on how to implement variants, like operating system variants or hardware variants, in C code. It discusses five patterns on how to cope with code variants as well as how to organize or even get rid of `#ifdef` statements. The patterns can be viewed as an introduction to organizing such code or as a guide on how to refactor unstructured `#ifdef` code.

[Figure 9-1](#fig_ifdef) shows the way out of the `#ifdef` nightmare, and [Table 9-1](#tab_ifdef) provides a short summary of the patterns discussed in this chapter.

![The way out of the \#ifdef nightmare](images/fluc_0901.png)

###### Figure 9-1. The way out of `#ifdef` hell

|  | Pattern name | Summary |
|----|----|----|
|  | Avoid Variants | Using different functions for each platform makes the code harder to read and write. The programmer is required to initially understand, correctly use, and test these multiple functions in order to achieve a single functionality across multiple platforms. Therefore, use standardized functions that are available on all platforms. If there are no standardized functions, consider not implementing the functionality. |
|  | Isolated Primitives | Having code variants organized with `#ifdef` statements makes the code unreadable. It is very difficult to follow the program flow, because it is implemented multiple times for multiple platforms. Therefore, isolate your code variants. In your implementation file, put the code handling the variants into separate functions and call these functions from your main program logic, which then contains only platform-independent code. |
|  | Atomic Primitives | The function that contains the variants and is called by the main program is still hard to comprehend because all the complex `#ifdef` code was only put into this function in order to get rid of it in the main program. Therefore, make your primitives atomic. Only handle exactly one kind of variant per function. If you handle multiple kinds of variants—for example, operating system variants and hardware variants—then have separate functions for each. |
|  | Abstraction Layer | You want to use the functionality that handles platform variants at several places in your codebase, but you do not want to duplicate the code of that functionality. Therefore, provide an API for each functionality that requires platform-specific code. Define only platform-independent functions in the header file and put all platform-specific `#ifdef` code into the implementation file. The caller of your functions includes only your header file and does not have to include any platform-specific files. |
|  | Split Variant Implementations | The platform-specific implementations still contain `#ifdef` statements to distinguish between code variants. That makes it difficult to see and select which part of the code should be built for which platform. Therefore, put each variant implementation into a separate implementation file and select per file what you want to compile for which platform. |

Table 9-1. Patterns on how to escape `#ifdef` hell

# Running Example

Let’s say you want to implement the functionality to write some text into a file to be stored in a newly created directory that, depending on a configuration flag, is either created in the current or in the home-directory. To make things more complicated, your code should run on Windows systems as well as on Linux systems.

Your first attempt is to have one implementation file that contains all the code for all configurations and operating systems. To do that, the file contains many `#ifdef` statements to distinguish between the code variants:

```
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#ifdef __unix__
  #include <sys/stat.h>
  #include <fcntl.h>
  #include <unistd.h>
#elif defined _WIN32
  #include <windows.h>
#endif

int main()
{
  char dirname[50];
  char filename[60];
  char* my_data = "Write this data to the file";
  #ifdef __unix__
    #ifdef STORE_IN_HOME_DIR
      sprintf(dirname, "%s%s", getenv("HOME"), "/newdir/");
      sprintf(filename, "%s%s", dirname, "newfile");
    #elif defined STORE_IN_CWD
      strcpy(dirname, "newdir");
      strcpy(filename, "newdir/newfile");
    #endif
    mkdir(dirname,S_IRWXU);
    int fd = open (filename, O_RDWR | O_CREAT, 0666);
    write(fd, my_data, strlen(my_data));
    close(fd);
  #elif defined _WIN32
    #ifdef STORE_IN_HOME_DIR
      sprintf(dirname, "%s%s%s", getenv("HOMEDRIVE"), getenv("HOMEPATH"),
              "\\newdir\\");
      sprintf(filename, "%s%s", dirname, "newfile");
    #elif defined STORE_IN_CWD
      strcpy(dirname, "newdir");
      strcpy(filename, "newdir\\newfile");
    #endif
    CreateDirectory (dirname, NULL);
    HANDLE hFile = CreateFile(filename, GENERIC_WRITE, 0, NULL,
                              CREATE_NEW, FILE_ATTRIBUTE_NORMAL, NULL);
    WriteFile(hFile, my_data, strlen(my_data), NULL, NULL);
    CloseHandle(hFile);
  #endif
  return 0;
}
```

This code is chaos. The program logic is completely duplicated. This is not operating system-independent code; instead, it is only two different operating system–specific implementations put into one file. In particular, the orthogonal code variants of different operating systems and different places for creating the directory make the code ugly because they lead to nested `#ifdef` statements, which are very hard to understand. When reading the code, you have to constantly jump between the lines. You have to skip the code from other `#ifdef` branches in order to follow the program logic. Such duplicated program logic invites programmers to fix errors or to add new features only in the code variant that they currently work on. That causes the code pieces and the behavior for the variants to drift apart, which makes the code hard to maintain.

Where to start? How to clean this mess up? As a first step, if possible, you can use standardized functions in order to Avoid Variants.

# Avoid Variants

## Context

You write portable code that should be used on multiple operating system platforms or on multiple hardware platforms. Some of the functions you call in your code are available on one platform, but are not available in exactly the same syntax and semantics on another platform. Because of this, you implement code variants—one for each platform. Now you have different pieces of code for your different platforms, and you distinguish between the variants with `#ifdef` statements in your code.

## Problem

**Using different functions for each platform makes the code harder to read and write. The programmer is required to initially understand, correctly use, and test these multiple functions in order to achieve a single functionality across multiple platforms.**

Quite often it is the aim to implement functionality that should behave exactly the same on all platforms, but when using platform-dependent functions, that aim is more difficult to achieve and might require writing additional code. This is because not only the syntax but also the semantics of the functions might differ slightly between the platforms.

Using multiple functions for multiple platforms makes the code more difficult to write, read, and understand. Distinguishing between the different functions with `#ifdef` statements makes the code longer and requires the reader to jump across lines to find out what the code does for a single `#ifdef` branch.

With any piece of code that you have to write, you can ask yourself if it is worth the effort. If the required functionality is not an important one, and if platform-specific functions make it very difficult to implement and support that functionality, then it is an option to not provide that functionality at all.

## Solution

**Use standardized functions that are available on all platforms. If there are no standardized functions, consider not implementing the functionality.**

Good examples of standardized functions that you can use are the C standard library functions and the POSIX functions. Consider which platforms you want to support and check that these standardized functions are available on all your platforms. If possible, such standardized functions should be used instead of more specific platform-dependent functions as shown in the following code:

*Caller’s code*

```
#include <standardizedApi.h>

int main()
{
  /* just a single function is called instead of multiple via
     ifdef distinguished functions */
  somePosixFunction();
  return 0;
}
```

\

*Standardized API*

```
  /* this function is available on all operating systems
     that adhere to the POSIX standard */
  somePosixFunction();
```

Again, if no standardized functions exist for what you want, you probably shouldn’t implement the requested functionality. If there are only platform-dependent functions available for the functionality you want to implement, then it might not be worth the implementation, testing, and maintenance effort.

However, in some cases you do have to provide functionality in your product even if there are no standardized functions available. That means you have to use different functions across different platforms or maybe even implement features on one platform that are already available on another. To do that in a structured way, have Isolated Primitives for your code variants and hide them behind an Abstraction Layer.

To avoid variants you can, for example, use C standard library file access functions like `fopen` instead of using operating system–specific functions like Linux’s `open` or Windows’ `CreateFile` functions. As another example, you can use the C standard library time functions. Avoid using operating system–specific time functions like Windows’ `GetLocalTime` and Linux’s `localtime_r`; use the standardized `localtime` function from *time.h* instead.

## Consequences

The code is simple to write and read because a single piece of code can be used for multiple platforms. The programmer does not have to understand different functions for different platforms when writing the code, and they don’t have to jump between `#ifdef` branches when reading the code.

Since the same piece of code is being used across all platforms, functionality doesn’t differ. But the standardized function might not be the most efficient or high-performance way to achieve the required functionality on each of the platforms. Some platforms might provide other platform-specific functions that, for example, use specialized hardware on that platform to achieve higher performance. These advantages may not be used by the standardized functions.

## Known Uses

The following examples show applications of this pattern:

- The code of the VIM text editor uses the operating system–independent functions `fopen`, `fwrite`, `fread`, and `fclose` to access files.

- The OpenSSL code writes the current local time to its log messages. To do that, it converts the current UTC time to local time using the operating system–independent function `localtime`.

- The OpenSSL function `BIO_lookup_ex` looks up the node and service to connect to. This function is compiled on Windows and Linux and uses the operating system–independent function `htons` to convert a value to network byte order.

## Applied to Running Example

For your functionality to access files, you are in a lucky position because there are operating system–independent functions available. You now have the following code:

```
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#ifdef __unix__
  #include <sys/stat.h>
#elif defined _WIN32
  #include <windows.h>
#endif

int main()
{
  char dirname[50];
  char filename[60];
  char* my_data = "Write this data to the file";
  #ifdef __unix__
    #ifdef STORE_IN_HOME_DIR
      sprintf(dirname, "%s%s", getenv("HOME"), "/newdir/");
      sprintf(filename, "%s%s", dirname, "newfile");
    #elif defined STORE_IN_CWD
      strcpy(dirname, "newdir");
      strcpy(filename, "newdir/newfile");
    #endif
    mkdir(dirname,S_IRWXU);
  #elif defined _WIN32
    #ifdef STORE_IN_HOME_DIR
      sprintf(dirname, "%s%s%s", getenv("HOMEDRIVE"), getenv("HOMEPATH"),
              "\\newdir\\");
      sprintf(filename, "%s%s", dirname, "newfile");
    #elif defined STORE_IN_CWD
      strcpy(dirname, "newdir");
      strcpy(filename, "newdir\\newfile");
    #endif
    CreateDirectory(dirname, NULL);
  #endif
  FILE* f = fopen(filename, "w+"); 
  fwrite(my_data, 1, strlen(my_data), f);
  fclose(f);
  return 0;
}
```

[![1](images/1.png)](#co_escaping__ifdef_hell_CO1-1)  
The functions `fopen`, `fwrite`, and `fclose` are part of the C standard library and are available on Windows as well as on Linux.

The standardized file-related function calls in that code made things a lot simpler already. Instead of having the separate file access calls for Windows and for Linux, you now have one common code. The common code ensures that the calls perform the same functionality for both operating systems, and there is no danger that two different implementations run apart after bug fixes or added features.

However, because your code is still dominated by `#ifdefs`, it is very difficult to read. Therefore, make sure that your main program logic does not get obfuscated by code variants. Have Isolated Primitives separating the code variants from the main program logic.

# Isolated Primitives

## Context

Your code calls platform-specific functions. You have different pieces of code for different platforms, and you distinguish between the code variants with `#ifdef` statements. You cannot simply Avoid Variants because there are no standardized functions available that provide the feature you need in a uniform way on all your platforms.

## Problem

**Having code variants organized with `#ifdef` statements makes the code unreadable. It is very difficult to follow the program flow, because it is implemented multiple times for multiple platforms.**

When trying to understand the code, you usually focus on only one platform, but the `#ifdefs` force you to jump between the lines in the code to find the code variant you are interested in.

The `#ifdef` statements also make the code difficult to maintain. Such statements invite programmers to only fix the code for the one platform they are interested in and to not touch any other code because of the danger of breaking it. But only fixing a bug or introducing a new feature for one platform means that the behavior of the code on the other platforms drifts apart. The alternative—to fix such a bug on all platforms in different ways—requires testing the code on all platforms.

Testing code with many code variants is difficult. Each new kind of `#ifdef` statement doubles the testing effort because all possible combinations have to be tested. Even worse, each such statement doubles the number of binaries that can be built and have to be tested. That brings in a logistic problem because build times increase and the number of binaries provided to the test department and to the customer increases.

## Solution

**Isolate your code variants. In your implementation file, put the code handling the variants into separate functions and call these functions from your main program logic, which then only contains platform-independent code.**

Each of your functions should either only contain program logic or only cope with handling variants. None of your functions should do both. So either there is no `#ifdef` statement at all in a function, or there are `#ifdef` statements with a single variant-dependent function call per `#ifdef` branch. Such a variant could be a software feature that is turned on or off by a build configuration, or it could be a platform variant as shown in the following code:

```
void handlePlatformVariants()
{
  #ifdef PLATFORM_A
    /* call function of platform A */
  #elif defined PLATFORM_B 
    /* call function of platform B */
  #endif
}

int main()
{
  /* program logic goes here */
  handlePlatformVariants();
  /* program logic continues */
}
```

[![1](images/1.png)](#co_escaping__ifdef_hell_CO2-1)  
Similar to `else if` statements, mutually exclusive variants can be expressed nicely using `#elif`.

Utilizing a single function call per `#ifdef` branch should make it possible to find a good abstraction granularity for the functions handling the variants. Usually the granularity is exactly at the level of the available platform-specific or feature-specific functions to be wrapped.

If the functions that handle the variants are still complicated and contain `#ifdef` cascades (nested `#ifdef` statements), it helps to make sure you only have Atomic Variants.

## Consequences

The main program logic is now easy to follow, because the code variants are separated from it. When reading the main code, it is no longer necessary to jump between the lines to find out what the code does on one specific platform.

To determine what the code does on one specific platform, you have to look at the called function that implements this variant. Having that code in a separately called function has the advantage that it can be called from other places in the file, and thus code duplications can be avoided. If the functionality is also required in other implementation files, then an Abstraction Layer has to be implemented.

No program logic should be introduced in the functions handling the variants, so it is easier to pinpoint bugs that do not occur on all platforms, because it is easy to identify the places in the code where the behavior of the platforms differs.

Code duplication becomes less of an issue since the main program logic is well separated from the variant implementations. There is no temptation to duplicate the program logic anymore, so there is no threat of then accidentally only making bug fixes in one of these duplications.

## Known Uses

The following examples show applications of this pattern:

- The code of the VIM text editor isolates the function `htonl2` that converts data to network byte order. The program logic of VIM defines `htonl2` as a macro in the implementation file. The macro is compiled differently depending on the platform endianness.

- The OpenSSL function `BIO_ADDR_make` copies socket information into an internal `struct`. The function uses `#ifdef` statements to handle operating system–specific and feature-specific variants distinguishing between Linux/Windows and IPv4/IPv6. The function isolates these variants from the main program logic.

- The function `load_rcfile` of GNUplot reads data from an initialization file and isolates operating system–specific file access operations from the rest of the code.

## Applied to Running Example

Now that you have Isolated Primitives, your main program logic is a lot easier to read and doesn’t require the reader to jump between the lines to keep the variants apart:

```
void getDirectoryName(char* dirname)
{
  #ifdef __unix__
    #ifdef STORE_IN_HOME_DIR
      sprintf(dirname, "%s%s", getenv("HOME"), "/newdir/");
    #elif defined STORE_IN_CWD
      strcpy(dirname, "newdir/");
    #endif
  #elif defined _WIN32
    #ifdef STORE_IN_HOME_DIR
      sprintf(dirname, "%s%s%s", getenv("HOMEDRIVE"), getenv("HOMEPATH"),
              "\\newdir\\");
    #elif defined STORE_IN_CWD
      strcpy(dirname, "newdir\\");
    #endif
  #endif
}

void createNewDirectory(char* dirname)
{
  #ifdef __unix__
    mkdir(dirname,S_IRWXU);
  #elif defined _WIN32
    CreateDirectory (dirname, NULL);
  #endif
}

int main()
{
  char dirname[50];
  char filename[60];
  char* my_data = "Write this data to the file";
  getDirectoryName(dirname);
  createNewDirectory(dirname);
  sprintf(filename, "%s%s", dirname, "newfile");
  FILE* f = fopen(filename, "w+");
  fwrite(my_data, 1, strlen(my_data), f);
  fclose(f);
  return 0;
}
```

The code variants are now well isolated. The program logic of the `main` function is very easy to read and understand without the variants. However, the new function `getDirectoryName` is still dominated by `#ifdefs` and is not easy to comprehend. It may help to only have Atomic Primitives.

# Atomic Primitives

## Context

You implemented variants in your code with `#ifdef` statements, and you put these variants into separate functions in order to have Isolated Primitives that handle these variants. The primitives separate the variants from the main program flow, which makes the main program well structured and easy to comprehend.

## Problem

**The function that contains the variants and is called by the main program is still hard to comprehend because all the complex `#ifdef` code was only put into this function in order to get rid of it in the main program.**

Handling all kinds of variants in one function becomes difficult as soon as there are many different variants to handle. If, for example, a single function uses `#ifdef` statements to distinguish between different hardware types and operating systems, then adding an additional operating system variant becomes difficult because it has to be added for all hardware variants. Each variant cannot be handled in one place anymore; instead, the effort multiplies with the number of different variants. That is a problem. It should be easy to add new variants at one place in the code.

## Solution

**Make your primitives atomic. Only handle exactly one kind of variant per function. If you handle multiple kinds of variants—for example, operating system variants and hardware variants—then have separate functions for each.**

Let one of these functions call another that already abstracts one kind of variant. If you abstract a platform-dependence and a feature-dependence, then let the feature-dependent function be the one calling the platform-dependent function, because you usually provide features across all platforms. Therefore, platform-dependent functions should be the most atomic functions, as shown in the following code:

```
void handleHardwareOfFeatureX()
{
  #ifdef HARDWARE_A
   /* call function for feature X on hardware A */
  #elif defined HARDWARE_B || defined HARDWARE_C
   /* call function for feature X on hardware B and C */
  #endif
}

void handleHardwareOfFeatureY()
{
  #ifdef HARDWARE_A
   /* call function for feature Y on hardware A */
  #elif defined HARDWARE_B
   /* call function for feature Y on hardware B */
  #elif defined HARDWARE_C
   /* call function for feature Y on hardware C */
  #endif
}

void callFeature()
{
  #ifdef FEATURE_X
    handleHardwareOfFeatureX();
  #elif defined FEATURE_Y
    handleHardwareOfFeatureY();
  #endif
}
```

If there is a function that clearly has to provide a functionality across multiple kinds of variants as well as handle all these kinds of variants, then the function scope might be wrong. Perhaps the function is too general or does more than one thing. Split the function as suggested by the Function Split pattern.

Call Atomic Primitives in your main code containing the program logic. If you want to use the Atomic Primitives in other implementation files with a well-defined interface, then use an Abstraction Layer.

## Consequences

Each function now only handles one kind of variant. That makes each of the functions easy to understand because there are no more cascades of `#ifdef` statements. Each of the functions now only abstracts one kind of variant and does no more than exactly that one thing. So the functions follow the single-responsibility principle.

Having no `#ifdef` cascades makes it less tempting for programmers to simply handle one additional kind of variant in one function, because starting an `#ifdef` cascade is less likely than extending an existing cascade.

With separate functions, each kind of variant can easily be extended for an additional variant. To achieve this, only one `#ifdef` branch has to be added in one function, and the functions which handle other kinds of variants do not have to be touched.

## Known Uses

The following examples show applications of this pattern:

- The OpenSSL implementation file *threads_pthread.c* contains functions for thread handling. There are separate functions to abstract operating systems and separate functions to abstract whether pthreads are available at all.

- The code of SQLite contains functions to abstract operating system–specific file access (for example, the `fileStat` function). The code abstracts file access–related compile-time features with other separate functions.

- The Linux function `boot_jump_linux` calls another function that performs different boot actions depending on the CPU architecture that is handled via `#ifdef` statements in that function. Then the function `boot_jump_linux` calls another function that uses `#ifdef` statements to select which configured resources (USB, network, etc.) have to be cleaned up.

## Applied to Running Example

With Atomic Primitives you now have the following code for your functions to determine the directory path:

```
void getHomeDirectory(char* dirname)
{
  #ifdef __unix__
    sprintf(dirname, "%s%s", getenv("HOME"), "/newdir/");
  #elif defined _WIN32
    sprintf(dirname, "%s%s%s", getenv("HOMEDRIVE"), getenv("HOMEPATH"),
            "\\newdir\\");
  #endif
}

void getWorkingDirectory(char* dirname)
{
  #ifdef __unix__
    strcpy(dirname, "newdir/");
  #elif defined _WIN32
    strcpy(dirname, "newdir\\");
  #endif
}

void getDirectoryName(char* dirname)
{
  #ifdef STORE_IN_HOME_DIR
    getHomeDirectory(dirname);
  #elif defined STORE_IN_CWD
    getWorkingDirectory(dirname);
  #endif
}
```

The code variants are now very well isolated. To obtain the directory name, instead of having one complicated function with many `#ifdefs`, you now have several functions that only have one `#ifdef` each. That makes it a lot easier to understand the code because now each of these functions only performs one thing instead of distinguishing between several kinds of variants with `#ifdef` cascades.

The functions are now very simple and easy to read, but your implementation file is still very long. In addition, one implementation file contains the main program logic as well as code to distinguish between variants. This makes parallel development or separate testing of the variant code next to impossible.

To improve things, split the implementation file up into variant-dependent and variant-independent files. To do that, create an Abstraction Layer.

# Abstraction Layer

## Context

You have platform variants that are distinguished with `#ifdef` statements in your code. You may have Isolated Primitives to separate the variants from the program logic and made sure that you have Atomic Primitives.

## Problem

**You want to use the functionality which handles platform variants at several places in your codebase, but you do not want to duplicate the code of that functionality.**

Your callers might be used to work directly with platform-specific functions, but you don’t want that anymore because each of the callers has to implement platform variants on their own. Generally, callers should not have to cope with platform variants. In the callers’ code, it should not be necessary to know anything about implementation details for the different platforms, and the callers should not have to use any `#ifdef` statements or include any platform-specific header files.

You are even considering working with different programmers (not the ones responsible for the platform-independent code) to separately develop and test the platform-dependent code.

You want to be able to change the platform-specific code later on without requiring the caller of this code to care about this change. If programmers of the platform-dependent code perform a bug fix for one platform or if they add an additional platform, then this must not require changes to the caller’s code.

## Solution

**Provide an API for each functionality that requires platform-specific code. Define only platform-independent functions in the header file and put all platform-specific `#ifdef` code into the implementation file. The caller of your functions only includes your header file and does not have to include any platform-specific files.**

Try to design a stable API for the abstraction layer, because changing the API later on requires changes in your caller’s code and sometimes that is not possible. However, it is very difficult to design a stable API. For platform abstractions, try looking around at different platforms, even ones you don’t yet support. After you have a sense of how they work and what the differences are, you can create an API to abstract features for these platforms. That way, you won’t need to change the API later, even when you’re adding support for different platforms.

Make sure to document the API thoroughly. Add comments to each function describing what the function does. Also, describe on which platforms the functions are supported if that is not clearly defined elsewhere for your whole codebase.

The following code shows a simple Abstraction Layer:

*caller.c*

```
#include "someFeature.h"

int main()
{
  someFeature();
  return 0;
}
```

\
*someFeature.h*

```
/* Provides generic access to someFeature.
   Supported on platform A and platform B. */
void someFeature();
```

\
*someFeature.c*

```
void someFeature()
{
  #ifdef PLATFORM_A
    performFeaturePlatformA();
  #elif defined PLATFORM_B
    performFeaturePlatformB();
  #endif
}
```

## Consequences

The abstracted features can be used from anywhere in the code and not only from one single implementation file. In other words, now you have distinct roles of caller and callee. The callee has to cope with platform variants, and the caller can be platform independent.

The benefit to this setup is the caller does not have to cope with platform-specific code. The caller simply includes the provided header file and does not have to include any platform-specific header files. The downside is the caller cannot directly use all platform-specific functions anymore. If the caller is accustomed to these functions, then the caller might not be satisfied with using the abstracted functionality and may find it difficult to use or suboptimal in functionality.

The platform-specific code can now be developed and even tested separately from the other code. Now the testing effort is manageable, even with many platforms, because you can mock the hardware-specific code in order to write simple tests for the platform-independent code.

When building up such APIs for all platform-specific functions, the sum of these functions and APIs is the platform abstraction layer for the codebase. With a platform abstraction layer, it is very clear which code is platform dependent and which is platform independent. A platform abstraction layer also makes it clear which parts of the code have to be touched in order to support an additional platform.

## Known Uses

The following examples show applications of this pattern:

- Most larger-scale code that runs on multiple platforms has a hardware Abstraction Layer. For example, Nokia’s Maemo platform has such an Abstraction Layer to abstract which actual device drivers are loaded.

- The function `sock_addr_inet_pton` of the lighttpd web server converts an IP address from text to binary form. The implementation uses `#ifdef` statements to distinguish between code variants for IPv4 and IPv6. Callers of the API do not see this distinction.

- The function `getprogname` of the gzip data compression program returns the name of the invoking program. The way to obtain this name depends on the operating system and is distinguished via `#ifdef` statements in the implementation. The caller does not have to care on which operating system the function is called.

- A hardware abstraction is used for the Time-Triggered Ethernet protocol described in the bachelor’s thesis [“Hardware-Abstraction of an Open Source Real-Time Ethernet Stack—Design, Realisation and Evaluation”](https://oreil.ly/hs0Jh) by Flemming Bunzel. The hardware abstraction layer contains functions for accessing interrupts and timers. The functions are marked as `inline` to not lose performance.

## Applied to Running Example

Now you have a much more streamlined piece of code. Each of the functions only performs one action, and you hide implementation details about the variants behind APIs:

*directoryNames.h*

```
/* Copies the path to a new directory with name "newdir"
   located in the user's home directory into "dirname".
   Works on Linux and Windows. */
void getHomeDirectory(char* dirname);


/* Copies the path to a new directory with name "newdir"
   located in the current working directory into "dirname".
   Works on Linux and Windows. */
void getWorkingDirectory(char* dirname);
```

\
*directoryNames.c*

```
#include "directoryNames.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void getHomeDirectory(char* dirname)
{
  #ifdef __unix__
    sprintf(dirname, "%s%s", getenv("HOME"), "/newdir/");
  #elif defined _WIN32
    sprintf(dirname, "%s%s%s", getenv("HOMEDRIVE"), getenv("HOMEPATH"),
            "\\newdir\\");
  #endif
}

void getWorkingDirectory(char* dirname)
{
  #ifdef __unix__
    strcpy(dirname, "newdir/");
  #elif defined _WIN32
    strcpy(dirname, "newdir\\");
  #endif
}
```

\
*directorySelection.h*

```
/* Copies the path to a new directory with name "newdir" into "dirname".
   The directory is located in the user's home directory, if STORE_IN_HOME_DIR
   is set or it is located in the current working directory, if STORE_IN_CWD
   is set. */
void getDirectoryName(char* dirname);
```

\
*directorySelection.c*

```
#include "directorySelection.h"
#include "directoryNames.h"

void getDirectoryName(char* dirname)
{
  #ifdef STORE_IN_HOME_DIR
    getHomeDirectory(dirname);
  #elif defined STORE_IN_CWD
    getWorkingDirectory(dirname);
  #endif
}
```

\
*directoryHandling.h*

```
/* Creates a new directory of the provided name ("dirname").
   Works on Linux and Windows. */
void createNewDirectory(char* dirname);
```

\
*directoryHandling.c*

```
#include "directoryHandling.h"
#ifdef __unix__
  #include <sys/stat.h>
#elif defined _WIN32
  #include <windows.h>
#endif

void createNewDirectory(char* dirname)
{
  #ifdef __unix__
    mkdir(dirname,S_IRWXU);
  #elif defined _WIN32
    CreateDirectory (dirname, NULL);
  #endif
}
```

\
*main.c*

```
#include <stdio.h>
#include <string.h>
#include "directorySelection.h"
#include "directoryHandling.h"

int main()
{
  char dirname[50];
  char filename[60];
  char* my_data = "Write this data to the file";
  getDirectoryName(dirname);
  createNewDirectory(dirname);
  sprintf(filename, "%s%s", dirname, "newfile");
  FILE* f = fopen(filename, "w+");
  fwrite(my_data, 1, strlen(my_data), f);
  fclose(f);
  return 0;
}
```

Your file with the main program logic is finally completely independent from the operating system; operating system–specific header files are not even included here. Separating the implementation files with an Abstraction Layer makes the files easier to comprehend and makes it possible to reuse the functions in other parts of the code. Also, development, maintenance, and testing can be split for the platform-dependent and platform-independent code.

If you have Isolated Primitives behind an Abstraction Layer and you’ve organized them according to the kind of variant that they abstract, then you’ll end up with a hardware abstraction layer or operating system abstraction layer. Now that you have a lot more code files than before—particularly those handling different variants—you may want to consider structuring them into Software-Module Directories.

The code that uses the API of the Abstraction Layer is very clean now, but the implementations below that API still contain `#ifdef` code for different variants. This has the disadvantage that these implementations have to be touched and will grow if, for example, additional operating systems have to be supported. To avoid touching existing implementation files when adding another variant, you could Split Variant Implementations.

# Split Variant Implementations

## Context

You have platform variants hidden behind an Abstraction Layer. In the platform-specific implementation, you distinguish between the code variants with `#ifdef` statements.

## Problem

**The platform-specific implementations still contain `#ifdef` statements to distinguish between code variants. That makes it difficult to see and select which part of the code should be built for which platform.**

Because code for different platforms is put into a single file, it is not possible to select the platform-specific code on a file-basis. However, that is the approach taken by tools such as Make, which are usually responsible for selecting via Makefiles which files should be compiled in order to come up with variants for different platforms.

When looking at the code from a high-level view, it is not possible to see which parts are platform-specific and which are not, but that would be very desirable when porting the code to another platform, in order to quickly see which code has to be touched.

The open-closed principle says that to bring in new features (or to port to a new platform), it should not be necessary to touch existing code. The code should be open for such modifications. However, having platform variants separated with `#ifdef` statements requires that existing implementations have to be touched when introducing a new platform, because another `#ifdef` branch has to be placed into an existing function.

## Solution

**Put each variant implementation into a separate implementation file and select per file what you want to compile for which platform.**

Related functions of the same platform can still be put into the same file. For example, there could be a file gathering all socket handling functions on Windows and one such file doing the same for Linux.

With separate files for each platform, it is OK to use `#ifdef` statements to determine which code is compiled on a specific platform. For example, a *someFeatureWindows.c* file could have an `#ifdef _WIN32` statement across the whole file similar to Include Guards:

*someFeature.h*

```
/* Provides generic access to someFeature.
   Supported on platform A and platform B. */
  someFeature();
```

\
*someFeatureWindows.c*

```
#ifdef _WIN32
  someFeature()
  {
    performWindowsFeature();
  }
#endif
```

\
*someFeatureLinux.c*

```
#ifdef __unix__
  someFeature()
  {
    performLinuxFeature();
  }
#endif
```

Alternatively to using `#ifdef` statements across the whole file, other platform-independent mechanisms such as Make can be used to decide on a file-basis which code to compile on a specific platform. If your IDE helps with generating Makefiles, that alternative might be more comfortable for you, but be aware that when changing the IDE, you might have to reconfigure which files to compile on which platform in the new IDE.

With separate files for the platforms comes the question of where to put these files and how to name them:

- One option is to put platform-specific files per software-module next to each other and name them in a way that makes it clear which platform they cover (for example *fileHandlingWindows.c*). Such Software-Module Directories provide the advantage that the implementations of the software-modules are in the same place.

- Another option is to put all platform-specific files from the codebase into one directory and to have one subdirectory for each platform. The advantage of this is that all files for one platform are in the same place and it becomes easier to configure in your IDE which files to compile on which platform.

## Consequences

Now it is possible to not have any `#ifdef` statements at all in the code but to instead distinguish between the variants on a file-basis with tools such as Make.

In each implementation file there is now just one code variant, so there is no need to jump between the lines when reading the code in order to only read the `#ifdef` branch you are looking for. It is much easier to read and understand the code.

When fixing a bug on one platform, no files for other platforms have to be touched. When porting to a new platform, only new files have to be added, and no existing file or existing code has to be modified.

It is easy to spot which part of the code is platform-dependent and which code has to be added in order to port to a new platform. Either all platform-specific files are in one directory, or the files are named in a way that makes it clear they are platform-dependent.

However, putting each variant into a separate file creates many new files. The more files you have, the more complex your build procedure gets and the longer the compile time for your code gets. You will need to think about structuring the files, for example, with Software-Module Directories.

## Known Uses

The following examples show applications of this pattern:

- The Simple Audio Library presented in the book *Write Portable Code: An Introduction to Developing Software for Multiple Platforms* by Brian Hook (No Starch Press, 2005) uses separate implementation files to provide access to threads and Mutexes for Linux and OS X. The implementation files use `#ifdef` statements to ensure that only the correct code for the platform is compiled.

- The Multi-Processing-Module of the Apache web server, which is responsible for handling accesses to the web server, is implemented in separate implementation files for Windows and Linux. The implementation files use `#ifdef` statements to ensure that only the correct code for the platform is compiled.

- The code of the U-Boot bootloader puts the source code for each hardware platform it supports into a separate directory. Each of these directories contains, among others, the file *cpu.c*, which contains a function to reset the CPU. A Makefile decides which directory (and which *cpu.c* file) has to be compiled—there are no `#ifdef` statements in these files. The main program logic of U-Boot calls the function to reset the CPU and does not have to care about hardware platform details at that point.

## Applied to Running Example

After Splitting Variant Implementations, you’ll end up with the following final code for your functionality to create a directory and write data to a file:

*directoryNames.h*

```
/* Copies the path to a new directory with name "newdir"
   located in the user's home directory into "dirname".
   Works on Linux and Windows. */
void getHomeDirectory(char* dirname);

/* Copies the path to a new directory with name "newdir"
   located in the current working directory into "dirname".
   Works on Linux and Windows. */
void getWorkingDirectory(char* dirname);
```

\
*directoryNamesLinux.c*

```
#ifdef __unix__
  #include "directoryNames.h"
  #include <string.h>
  #include <stdio.h>
  #include <stdlib.h>

  void getHomeDirectory(char* dirname)
  {
    sprintf(dirname, "%s%s", getenv("HOME"), "/newdir/");
  }

  void getWorkingDirectory(char* dirname)
  {
    strcpy(dirname, "newdir/");
  }
#endif
```

\
*directoryNamesWindows.c*

```
#ifdef _WIN32
  #include "directoryNames.h"
  #include <string.h>
  #include <stdio.h>
  #include <windows.h>

  void getHomeDirectory(char* dirname)
  {
    sprintf(dirname, "%s%s%s", getenv("HOMEDRIVE"), getenv("HOMEPATH"),
            "\\newdir\\");
  }

  void getWorkingDirectory(char* dirname)
  {
    strcpy(dirname, "newdir\\");
  }
#endif
```

*directorySelection.h*

```
/* Copies the path to a new directory with name "newdir" into "dirname".
   The directory is located in the user's home directory, if STORE_IN_HOME_DIR
   is set or it is located in the current working directory, if STORE_IN_CWD
   is set. */
void getDirectoryName(char* dirname);
```

*directorySelectionHomeDir.c*

```
#ifdef STORE_IN_HOME_DIR
  #include "directorySelection.h"
  #include "directoryNames.h"

  void getDirectoryName(char* dirname)
  {
    getHomeDirectory(dirname);
  }
#endif
```

*directorySelectionWorkingDir.c*

```
#ifdef STORE_IN_CWD
  #include "directorySelection.h"
  #include "directoryNames.h"

  void getDirectoryName(char* dirname)
  {
    return getWorkingDirectory(dirname);
  }
#endif
```

\
*directoryHandling.h*

```
/* Creates a new directory of the provided name ("dirname").
   Works on Linux and Windows. */
void createNewDirectory(char* dirname);
```

\
*directoryHandlingLinux.c*

```
#ifdef __unix__
  #include <sys/stat.h>

  void createNewDirectory(char* dirname)
  {
    mkdir(dirname,S_IRWXU);
  }
#endif
```

\
*directoryHandlingWindows.c*

```
#ifdef _WIN32
  #include <windows.h>

  void createNewDirectory(char* dirname)
  {
    CreateDirectory(dirname, NULL);
  }
#endif
```

\
*main.c*

```
#include "directorySelection.h"
#include "directoryHandling.h"
#include <string.h>
#include <stdio.h>

int main()
{
  char dirname[50];
  char filename[60];
  char* my_data = "Write this data to the file";
  getDirectoryName(dirname);
  createNewDirectory(dirname);
  sprintf(filename, "%s%s", dirname, "newfile");
  FILE* f = fopen(filename, "w+");
  fwrite(my_data, 1, strlen(my_data), f);
  fclose(f);
  return 0;
}
```

There are still `#ifdef` statements present in this code. Each of the implementation files has one huge `#ifdef` in order to make sure that the correct code is compiled for each platform and variant. Alternatively, the decision regarding which files should be compiled could be put into a Makefile. That would get rid of the `#ifdefs`, but you’d simply use another mechanism to chose between variants. Deciding which mechanism to use is not so important. It is much more important, as described throughout this chapter, to isolate and abstract the variants.

While the code files would look cleaner when using other mechanisms to handle the variants, the complexity would still be there. Putting the complexity into Makefiles can be a good idea because the purpose of Makefiles is to decide which files to build. In other situations, it’s better to use `#ifdef` statements. For example, if you’re building operating system–specific code, maybe a proprietary IDE for Windows and another IDE for Linux is used to decide which files to build. In that circumstance, using the solution with `#ifdef` statements in the code is much cleaner; configuring which files should be built for which operating system is only done once by the `#ifdef` statements, and there is no need to touch that when changing to another IDE.

The final code of the running example showed very clearly how code with operating system–specific variants or other variants can be improved step by step. Compared to the first code example, this final piece of code is readable and can easily be extended with additional features or ported to additional operating systems without touching any of the existing code.

# Summary

This chapter presented patterns on how to handle variants, like hardware or operating system variants, in C code and how to organize and get rid of `#ifdef` statements.

The Avoid Variants pattern suggests using standardized functions instead of self-implemented variants. This pattern should be applied anytime it is applicable, because it resolves issues with code variants in one blow. However, there is not always a standardized function available, and in such cases, programmers have to implement their own function to abstract the variant. As a start, Isolated Primitives suggests putting variants into separate functions, and Atomic Primitives suggests only handling one kind of variant in such functions. Abstraction Layer takes the additional step to hide the implementations of the primitives behind an API. Split Variant Implementations suggests putting each variant into a separate implementation file.

With these patterns as part of the programming vocabulary, a C programmer has a toolbox and step-by-step guidance on how to tackle C code variants in order to structure code and escape from `#ifdef` hell.

For experienced programmers, some of the patterns might look like obvious solutions and that is a good thing. One of the tasks of patterns is to educate people on how to do the right thing; once they know how to do the right thing, the patterns are not necessary anymore because people then intuitively do as suggested by the patterns.

# Further Reading

If you’re ready for more, here are some resources that can help you further your knowledge of platform and variant abstractions.

- The book *Write Portable Code: An Introduction to Developing Software for Multiple Platforms* by Brian Hook (No Starch Press, 2005) describes how to write portable code in C. The book covers operating system variants and hardware variants by giving advice for specific situations, like coping with byte ordering, data type sizes, or line-separator tokens.

- The article [“#ifdef Considered Harmful”](https://oreil.ly/eZ2CW) by Henry Spencer and Geoff Collyer is one of the first that skeptically discusses the use of `#ifdef` statements. The article elaborates on problems that arise when using them in an unstructured way and provides alternatives.

- The article [“Writing Portable Code”](https://oreil.ly/XkTbj) by Didier Malenfant describes how to structure portable code and which functionality should be put below an abstraction layer.

# Outlook

You are now equipped with more patterns. Next, you’ll learn how to apply these patterns as well as the patterns from the previous chapters. The next chapters cover larger code examples that show the application of all these patterns.

