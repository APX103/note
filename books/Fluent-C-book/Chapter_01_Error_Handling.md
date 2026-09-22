# Chapter 1. Error Handling

Error handling is a big part of writing software, and when it’s done poorly, the software becomes difficult to extend and to maintain. Programming languages like C++ or Java provide “Exceptions” and “Destructors” that make error handling easier. Such mechanisms are not natively available for C, and literature on good error handling in C is widely scattered over the internet.

This chapter provides collected knowledge on good error handling in the form of C error-handling patterns and a running example that applies the patterns. The patterns provide good practice design decisions and elaborate on when to apply them and which consequences they bring. For a programmer, these patterns remove the burden of making many fine-grained decisions. Instead, a programmer can rely on the knowledge presented in these patterns and use them as a starting point to write good code.

[Figure 1-1](#fig_error_handling) shows an overview of the patterns covered in this chapter and their relationships, and [Table 1-1](#tab_error_handling) provides a summary of the patterns.

![pattern-maps/error-handling.png](images/fluc_0101.png)

###### Figure 1-1. Overview of patterns for error handling

|  | Pattern name | Summary |
|----|----|----|
|  | Function Split | The function has several responsibilities, which makes the function hard to read and maintain. Therefore, split it up. Take a part of a function that seems useful on its own, create a new function with that, and call that function. |
|  | Guard Clause | The function is hard to read and maintain because it mixes pre-condition checks with the main program logic of the function. Therefore, check whether you have mandatory pre-conditions and immediately return from the function if these pre-conditions are not met. |
|  | Samurai Principle | When returning error information, you assume that the caller checks for this information. However, the caller can simply omit this check and the error might go unnoticed. Therefore, return from a function victorious or not at all. If there is a situation for which you know that an error cannot be handled, then abort the program. |
|  | Goto Error Handling | Code gets difficult to read and maintain if it acquires and cleans up multiple resources at different places within a function. Therefore, have all resource cleanup and error handling at the end of the function. If a resource cannot be acquired, use the `goto` statement to jump to the resource cleanup code. |
|  | Cleanup Record | It is difficult to make a piece of code easy to read and maintain if this code acquires and cleans up multiple resources, particularly if those resources depend on one another. Therefore, call resource acquisition functions as long as they succeed, and store which functions require cleanup. Call the cleanup functions depending on these stored values. |
|  | Object-Based Error Handling | Having multiple responsibilities in one function, such as resource acquisition, resource cleanup, and usage of that resource, makes that code difficult to implement, read, maintain, and test. Therefore, put initialization and cleanup into separate functions, similar to the concept of constructors and destructors in object-oriented programming. |

Table 1-1. Patterns for error handling

# Running Example

You want to implement a function that parses a file for certain keywords and that returns information on which of the keywords was found.

The standard way to indicate an error situation in C is to provide this information via the return value of a function. To provide additional error information, legacy C functions often set the `errno` variable (see *errno.h*) to a specific error code. The caller can then check `errno` to get information about the error.

However, in the following code, you simply use return values instead of `errno` because you don’t need very detailed error information. You come up with the following initial piece of code:

```
int parseFile(char* file_name)
{
  int return_value = ERROR;
  FILE* file_pointer = 0;
  char* buffer = 0;

  if(file_name!=NULL)
  {
    if(file_pointer=fopen(file_name, "r"))
    {
      if(buffer=malloc(BUFFER_SIZE))
      {
        /* parse file content*/
        return_value = NO_KEYWORD_FOUND;
        while(fgets(buffer, BUFFER_SIZE, file_pointer)!=NULL)
        {
          if(strcmp("KEYWORD_ONE\n", buffer)==0)
          {
            return_value = KEYWORD_ONE_FOUND_FIRST;
            break;
          }
          if(strcmp("KEYWORD_TWO\n", buffer)==0)
          {
            return_value = KEYWORD_TWO_FOUND_FIRST;
            break;
          }
        }
        free(buffer);
      }
      fclose(file_pointer);
    }
  }
  return return_value;
}
```

In the code, you have to check the return values of the function calls to know whether an error occurred, so you end up with deeply nested `if` statements in your code. That presents the following problems:

- The function is long and mixes error-handling, initialization, cleanup, and functional code. This makes it difficult to maintain the code.

- The main code that reads and interprets the file data is deeply nested inside the `if` clauses, which makes it difficult to follow the program logic.

- The cleanup functions are far separated from their initialization functions, which makes it easy to forget some cleanup. This is particularly true if the function contains multiple return statements.

To make things better, you first perform a Function Split.

# Function Split

## Context

You have a function that performs multiple actions. For example, it allocates a resource (like dynamic memory or some file handle), uses this resource, and cleans it up.

## Problem

**The function has several responsibilities, which makes the function hard to read and maintain.**

Such a function could be responsible for allocating resources, operating on these resources, and cleaning up these resources. Maybe the cleanup is even scattered over the function and duplicated in some places. In particular, error handling of failed resource allocation makes such a function hard to read, because quite often that ends up in nested `if` statements.

Coping with allocation, cleanup, and usage of multiple resources in one function makes it easy to forget cleanup of a resource, particularly if the code is changed later on. For example, if a return statement is added in the middle of the code, then it is easy to forget cleaning up the resources that were already allocated at that point in the function.

## Solution

**Split it up. Take a part of a function that seems useful on its own, create a new function with that, and call that function.**

To find out which part of the function to isolate, simply check whether you can give it its own meaningful name and whether the split isolates responsibilities. That could, for example, result in one function containing just functional code and one containing just error-handling code.

A good indicator for a function to be split is if it contains cleanup of the same resource at multiple places in the function. In such a case, it is a lot better to split the code into one function that allocates and cleans up the resources and one function that uses these resources. The called function that uses the resources can then easily have multiple return statements without the need to clean up the resources before each return statement, because that is done in the other function. This is shown in the following code:

```
void someFunction()
{
  char* buffer = malloc(LARGE_SIZE);
  if(buffer)
  {
    mainFunctionality(buffer);
  }
  free(buffer);
}

void mainFunctionality()
{
  // implementation goes here
}
```

Now, you have two functions instead of one. That means, of course, that the calling function is not self-contained anymore and depends on the other function. You have to define where to put that other function. The first step is to put it right in the same file as the calling function, but if the two functions are not closely coupled, you can consider putting the called function into a separate implementation file and including a Header File declaration of that function.

## Consequences

You improved the code because two short functions are easier to read and maintain compared to one long function. For example, the code is easier to read because the cleanup functions are closer to the functions that need cleanup and because the resource allocation and cleanup do not mix with the main program logic. That makes the main program logic easier to maintain and to extend its functionality later on.

The called function can now easily contain several return statements because it does not have to care about cleanup of the resources before each return statement. That cleanup is done at a single point by the calling function.

If many resources are used by the called function, all these resources also have to be passed to that function. Having a lot of function parameters makes the code hard to read, and accidentally switching the order of the parameters when calling the function might result in programming errors. To avoid that, you can have an Aggregate Instance in such a case.

## Known Uses

The following examples show applications of this pattern:

- Pretty much all C code contains parts that apply this pattern and parts that do not apply this pattern and that are thus difficult to maintain. According to the book *Clean Code: A Handbook of Agile Software Craftsmanship* by Robert C. Martin (Prentice Hall, 2008), each function should have exactly one responsibility (single-responsibility principle), and thus resource handling and other program logic should always be split into different functions.

- This pattern is called Function Wrapper in the Portland Pattern Repository.

- For object-oriented programming, the Template Method pattern also describes a way to structure the code by splitting it up.

- The criteria for when and where to split the function are described in *Refactoring: Improving the Design of Existing Code* by Martin Fowler (Addison-Wesley, 1999) as the Extract Method pattern.

- The game NetHack applies this pattern in its function `read_config_file`, in which resources are handled and in which the function `parse_conf_file` is called, which then works on the resources.

- The OpenWrt code uses this pattern at several places for buffer handling. For example, the code responsible for MD5 calculation allocates a buffer, passes this buffer to another function that works on that buffer, and then cleans that buffer up.

## Applied to Running Example

Your code already looks a lot better. Instead of one huge function you now have two large functions with distinct responsibilities. One function is responsible for retrieving and releasing resources, and the other is responsible for searching for the keywords as shown in the following code:

```
int searchFileForKeywords(char* buffer, FILE* file_pointer)
{
  while(fgets(buffer, BUFFER_SIZE, file_pointer)!=NULL)
  {
    if(strcmp("KEYWORD_ONE\n", buffer)==0)
    {
      return KEYWORD_ONE_FOUND_FIRST;
    }
    if(strcmp("KEYWORD_TWO\n", buffer)==0)
    {
      return KEYWORD_TWO_FOUND_FIRST;
    }
  }
  return NO_KEYWORD_FOUND;
}

int parseFile(char* file_name)
{
  int return_value = ERROR;
  FILE* file_pointer = 0;
  char* buffer = 0;

  if(file_name!=NULL)
  {
    if(file_pointer=fopen(file_name, "r"))
    {
      if(buffer=malloc(BUFFER_SIZE))
      {
        return_value = searchFileForKeywords(buffer, file_pointer);
        free(buffer);
      }
      fclose(file_pointer);
    }
  }
  return return_value;
}
```

The depth of the `if` cascade decreased, but the function `parseFile` still contains three `if` statements that check for resource allocation errors, which is way too many. You can make that function cleaner by implementing a Guard Clause.

# Guard Clause

## Context

You have a function that performs a task that can only be successfully completed under certain conditions (like valid input parameters).

## Problem

**The function is hard to read and maintain because it mixes pre-condition checks with the main program logic of the function.**

Allocating resources always requires their cleanup. If you allocate a resource and then later on realize that another pre-condition of the function was not met, then that resource also has to be cleaned up.

It is difficult to follow the program flow if there are several pre-condition checks scattered across the function, particularly if these checks are implemented in nested `if` statements. When there are many such checks, the function becomes very long, which by itself is a code smell.

# Code Smell

A code “smells” if it is badly structured or programmed in a way that makes the code hard to maintain. Examples of code smells are very long functions or duplicated code. More code smell examples and countermeasures are covered in the book *Refactoring: Improving the Design of Existing Code* by Martin Fowler (Addison-Wesley, 1999).

## Solution

**Check if you have mandatory pre-conditions and immediately return from the function if these pre-conditions are not met.**

For example, check for the validity of input parameters or check if the program is in a state that allows execution of the rest of the function. Carefully think about which kind of pre-conditions for calling your function you want to set. On the one hand, it makes life easier for you to be very strict on what you allow as function input, but on the other hand, it would make life easier for the caller of your function if you are more liberal regarding possible inputs (as described by Postel’s law: “Be conservative in what you do, be liberal in what you accept from others”).

If you have many pre-condition checks, you can call a separate function for performing these checks. In any case, perform the checks before any resource allocation has been done because then it is very easy to return from a function as no cleanup of resources has to be done.

Clearly describe the pre-conditions for your function in the function’s interface. The best place to document that behavior is in the header file where the function is declared.

If it is important for the caller to know which pre-condition was not met, you can provide the caller with error information. For example, you can Return Status Codes, but make sure to only Return Relevant Errors. The following code shows an example without returning error information:

*someFile.h*

```
/* This function operates on the 'user_input', which must not be NULL */
void someFunction(char* user_input);
```

\
*someFile.c*

```
void someFunction(char* user_input)
{
  if(user_input == NULL)
  {
    return;
  }
  operateOnData(user_input);
}
```

## Consequences

Immediately returning when the pre-conditions are not met makes the code easier to read compared to nested `if` constructs. It is made very clear in the code that the function execution is not continued if the pre-conditions are not met. That makes the pre-conditions very well separated from the rest of the code.

However, some coding guidelines forbid returning in the middle of a function. For example, for code that has to be formally proved, return statements are usually only allowed at the very end of the function. In such a case, a Cleanup Record can be kept, which also is a better choice if you want to have a central place for error handling.

## Known Uses

The following examples show applications of this pattern:

- The Guard Clause is described in the Portland Pattern Repository.

- The article “Error Detection” by Klaus Renzel (Proceedings of the 2nd EuroPLoP conference, 1997) describes the very similar Error Detection pattern that suggests introducing pre-condition and post-condition checks.

- The NetHack game uses this pattern at several places in its code, for example, in the `placebc` function. That function puts a chain on the NetHack hero that reduces the hero’s movement speed as punishment. The function immediately returns if no chain objects are available.

- The OpenSSL code uses this pattern. For example, the `SSL_new` function immediately returns in case of invalid input parameters.

- The Wireshark code `capture_stats`, which is responsible for gathering statistics when sniffing network packets, first checks its input parameters for validity and immediately returns in case of invalid parameters.

## Applied to Running Example

The following code shows how the `parseFile` function applies a Guard Clause to check pre-conditions of the function:

```
int parseFile(char* file_name)
{
  int return_value = ERROR;
  FILE* file_pointer = 0;
  char* buffer = 0;

  if(file_name==NULL) 
  {
    return ERROR;
  }
  if(file_pointer=fopen(file_name, "r"))
  {
    if(buffer=malloc(BUFFER_SIZE))
    {
      return_value = searchFileForKeywords(buffer, file_pointer);
      free(buffer);
    }
    fclose(file_pointer);
  }
  return return_value;
}
```

[![1](images/1.png)](#co_error_handling_CO1-1)  
If invalid parameters are provided, we immediately return and no cleanup is required because no resources were acquired yet.

The code Returns Status Codes to implement the Guard Clause. It returns the constant `ERROR` in the specific case of a `NULL` parameter. The caller could now check the Return Value to know whether an invalid `NULL` parameter was provided to the function. But such an invalid parameter usually indicates a programming error, and checking for programming errors and propagating this information within the code is not a good idea. In such a case, it is easier to simply apply the Samurai Principle.

# Samurai Principle

## Context

You have some code with complicated error handling, and some errors are very severe. Your system does not perform safety-critical actions, and high availability is not very important.

## Problem

**When returning error information, you assume that the caller checks for this information. However, the caller can simply omit this check and the error might go unnoticed.**

In C it is not mandatory to check return values of the called functions, and your caller can simply ignore the return value of a function. If the error that occurs in your function is severe and cannot be gracefully handled by the caller, you don’t want your caller to decide whether and how the error should be handled. Instead, you’d want to make sure that an action is definitely taken.

Even if the caller handles an error situation, quite often the program will still crash or some error will still occur. The error might simply show up somewhere else—maybe somewhere in the caller’s caller code that might not handle error situations properly. In such a case, handling the error disguises the error, which makes it much harder to debug the error in order to find out the root cause.

Some errors in your code might only occur very rarely. To Return Status Codes for such situations and handle them in the caller’s code makes that code less readable, because it distracts from the main program logic and the actual purpose of the caller’s code. The caller might have to write many lines of code to handle very rarely occurring situations.

Returning such error information also poses the problem of how to actually return the information. Using the Return Value or Out-Parameters of the function to return error information makes the function’s signature more complicated and makes the code more difficult to understand. Because of this, you don’t want to have additional parameters for your function that only return error information.

## Solution

**Return from a function victorious or not at all (samurai principle). If there is a situation for which you know that an error cannot be handled, then abort the program.**

Don’t use Out-Parameters or the Return Value to return error information. You have all the error information at hand, so handle the error right away. If an error occurs, simply let the program crash. Abort the program in a structured way by using the `assert` statement. Additionally, you can provide debug information with the `assert` statement as shown in the following code:

```
void someFunction()
{
  assert(checkPreconditions() && "Preconditions are not met");
  mainFunctionality();
}
```

This piece of code checks for the condition in the `assert` statement and if it is not true, the `assert` statement including the string on the right will be printed to `stderr` and the program will be aborted. It would be OK to abort the program in a less structured way by not checking for `NULL` pointers and accessing such pointers. Simply make sure that the program crashes at the point where the error occurs.

Quite often, the Guard Clauses are good candidates for aborting the program in case of errors. For example, if you know that a coding error occurred (if the caller provided you a `NULL` pointer), abort the program and log debug information instead of returning error information to the caller. However, don’t abort the program for every kind of error. For example, runtime errors like invalid user input should definitely not lead to a program abort.

The caller has to be well aware of the behavior of your function, so you have to document in the function’s API the cases in which the function aborts the program. For example, the function documentation has to state whether the program crashes if the function is provided a `NULL` pointer as parameter.

Of course, the Samurai Principle is not appropriate for all errors or all application domains. You wouldn’t want to let the program crash in case of some unexpected user input. However, in case of a programming error, it can be appropriate to fail fast and let the program crash. That makes it as simple as possible for the programmers to find the error.

Still, such a crash need not necessarily be shown to the user. If your program is just some noncritical part of a larger application, then you might still want your program to crash. But in the context of the overall application, your program might fail silently so as not not disturb the rest of the application or the user.

# Asserts in Release Executables

When using `assert` statements, the discussion comes up of whether to only have them active in debug executables or whether to also have them active in release executables. `Assert` statements can be deactivated by defining the macro `NDEBUG` in your code before including *assert.h* or by directly defining the macro in your toolchain. A main argument for deactivating `assert` statements for release executables is that you already catch your programming errors that use `asserts` when testing your debug executables, so there is no need to risk aborting programs due to `asserts` in release executables. A main argument for also having `assert` statements active in release executables is that you use them anyway for critical errors that cannot be handled gracefully, and such errors should never go unnoticed, not even in release executables used by your customers.

## Consequences

The error cannot go unnoticed because it is handled right at the point where it shows up. The caller is not burdened with having to check for this error, so the caller code becomes simpler. However, now the caller cannot choose how to react to the error.

In some cases aborting the application is OK because a fast crash is better than unpredictable behavior later on. Still, you have to consider how such an error should be presented to the user. Maybe the user will see it as an abort statement on the screen. However, for embedded applications that use sensors and actors to interact with the environment, you have to take more care and consider the influence an aborting program has on the environment and whether this is acceptable. In many such cases, the application might have to be more robust and simply aborting the application will not be acceptable.

To abort the program and to Log Errors right at the point where the error shows up makes it easier to find and fix the error because the error is not disguised. Thus, in the long term, by applying this pattern you end up with more robust and bug-free software.

## Known Uses

The following examples show applications of this pattern:

- A similar pattern that suggests adding a debug information string to an `assert` statement is called Assertion Context and is described in the book *Patterns in C* by Adam Tornhill (Leanpub, 2014).

- The Wireshark network sniffer applies this pattern all over its code. For example, the function `register_capture_dissector` uses `assert` to check that the registration of a dissector is unique.

- The source code of the Git project uses `assert` statements. For example, the functions for storing SHA1 hash values use `assert` to check whether the path to the file where the hash value should be stored is correct.

- The OpenWrt code responsible for handling large numbers uses `assert` statements to check pre-conditions in its functions.

- A similar pattern with the name Let It Crash is presented by Pekka Alho and Jari Rauhamäki in the article [“Patterns for Light-Weight Fault Tolerance and Decoupled Design in Distributed Control Systems”](https://oreil.ly/x0tQW). The pattern targets distributed control systems and suggests letting single fail-safe processes crash and then restart quickly.

- The C standard library function `strcpy` does not check for valid user input. If you provide the function with a `NULL` pointer, it crashes.

## Applied to Running Example

The `parseFile` function now looks a lot better. Instead of returning an Error Code, you now have a simple `assert` statement. That makes the following code shorter, and the caller of the code does not have the burden of checking against the Return Value:

```
int parseFile(char* file_name)
{
  int return_value = ERROR;
  FILE* file_pointer = 0;
  char* buffer = 0;

  assert(file_name!=NULL && "Invalid filename");
  if(file_pointer=fopen(file_name, "r"))
  {
    if(buffer=malloc(BUFFER_SIZE))
    {
      return_value = searchFileForKeywords(buffer, file_pointer);
      free(buffer);
    }
    fclose(file_pointer);
  }
  return return_value;
}
```

While the `if` statements that don’t require resource cleanup are eliminated, the code still contains nested `if` statements for everything that requires cleanup. Also, you don’t yet handle the error situation if the `malloc` call fails. All of this can be improved by using Goto Error Handling.

# Goto Error Handling

## Context

You have a function that acquires and cleans up multiple resources. Maybe you already tried to reduce the complexity by applying Guard Clause, Function Split, or Samurai Principle, but you still have a deeply nested `if` construct in the code, particularly because of resource acquisition. You might even have duplicated code for resource cleanup.

## Problem

**Code gets difficult to read and maintain if it acquires and cleans up multiple resources at different places within a function.**

Such code becomes difficult because usually each resource acquisition can fail, and each resource cleanup can just be called if the resource was successfully acquired. To implement this, a lot of `if` statements are required, and when implemented poorly, nested `if` statements in a single function make the code hard to read and maintain.

Because you have to clean up the resources, returning in the middle of the function when something goes wrong is not a good option. This is because all resources already acquired have to be cleaned up before each return statement. So you end up with multiple points in the code where the same resource is being cleaned up, but you don’t want to have duplicated error handling and cleanup code.

## Solution

**Have all resource cleanup and error handling at the end of the function. If a resource cannot be acquired, use the `goto` statement to jump to the resource cleanup code.**

Acquire the resources in the order you need them, and at the end of your function clean the resources up in the reverse order. For the resource cleanup, have a separate label to which you can jump for each cleanup function. Simply jump to the label if an error occurs or if a resource cannot be acquired, but don’t jump multiple times and only jump forward as is done in the following code:

```
void someFunction()
{
  if(!allocateResource1())
  {
    goto cleanup1;
  }
  if(!allocateResource2())
  {
    goto cleanup2;
  }
  mainFunctionality();
cleanup2:
  cleanupResource2();
cleanup1:
  cleanupResource1();
}
```

If your coding standard forbids the usage of `goto` statements, you can emulate it with a `do{ ... }while(0);` loop around your code. On error use `break` to jump to the end of the loop where you put your error handling. However, that workaround is usually a bad idea because if `goto` is not allowed by your coding standard, then you should also not be emulating it just to continue programming in your own style. You could use a Cleanup Record as an alternative to `goto`.

In any case, the usage of `goto` might simply be an indicator that your function is already too complex, and splitting the function, for example with Object-Based Error Handling, might be a better idea.

# goto: Good or Evil?

There are many discussions about whether the usage of `goto` is good or bad. The most famous article against the use of `goto` is by [Edsger W. Dijkstra](https://oreil.ly/yXkyq), who argues that it obscures the program flow. That is true if `goto` is being used to jump back and forth in a program, but `goto` in C cannot be as badly abused as in the programming languages Dijkstra wrote about. (In C you can only use `goto` to jump within a function.)

## Consequences

The function is a single point of return, and the main program flow is well separated from the error handling and resource cleanup. No nested `if` statements are required anymore to achieve this, but not everybody is used to and likes reading `goto` statements.

If you use `goto` statements, you have to be careful, because it is tempting to use them for things other than error handling and cleanup, and that definitely makes the code unreadable. Also, you have to be extra careful to have the correct cleanup functions at the correct labels. It is a common pitfall to accidentally put cleanup functions at the wrong label.

## Known Uses

The following examples show applications of this pattern:

- The Linux kernel code uses mostly `goto`-based error handling. For example, the book [*Linux Device Drivers*](https://oreil.ly/linux-device-drivers) by Alessandro Rubini and Jonathan Corbet (O’Reilly, 2001) describes `goto`-based error handling for programming Linux device drivers.

- *The CERT C Coding Standard* by Robert C. Seacord (Addison-Wesley Professional, 2014) suggests the use of `goto` for error handling.

- The `goto` emulation using a `do-while` loop is described in the Portland Pattern Repository as the Trivial Do-While-Loop pattern.

- The OpenSSL code uses the `goto` statement. For example, the functions that handle X509 certificates use `goto` to jump forward to a central error handler.

- The Wireshark code uses `goto` statements to jump from its `main` function to a central error handler at the end of that function.

## Applied to Running Example

Even though quite a few people highly disapprove of the use of `goto` statements, the error handling is better compared to the previous code example. In the following code there are no nested `if` statements, and the cleanup code is well separated from the main program flow:

```
int parseFile(char* file_name)
{
  int return_value = ERROR;
  FILE* file_pointer = 0;
  char* buffer = 0;

  assert(file_name!=NULL && "Invalid filename");
  if(!(file_pointer=fopen(file_name, "r")))
  {
    goto error_fileopen;
  }
  if(!(buffer=malloc(BUFFER_SIZE)))
  {
    goto error_malloc;
  }
  return_value = searchFileForKeywords(buffer, file_pointer);
  free(buffer);
error_malloc:
  fclose(file_pointer);
error_fileopen:
  return return_value;
}
```

Now, let’s say you don’t like `goto` statements or your coding guidelines forbid them, but you still have to clean up your resources. There are alternatives. You can, for example, simply have a Cleanup Record instead.

# Cleanup Record

## Context

You have a function that acquires and cleans up multiple resources. Maybe you already tried to reduce the complexity by applying Guard Clause, Function Split, or Samurai Principle, but you still have a deeply nested `if` construct in the code, because of resource acquisition. You might even have duplicated code for resource cleanup. Your coding standards don’t allow you to implement Goto Error Handling, or you don’t want to use `goto`.

## Problem

**It is difficult to make a piece of code easy to read and maintain if this code acquires and cleans up multiple resources, particularly if those resources depend on one another.**

This is difficult because usually each resource acquisition can fail, and each resource cleanup can just be called if the resource was successfully acquired. To implement this, a lot of `if` statements are required, and when implemented poorly, nested `if` statements in a single function make the code hard to read and maintain.

Because you have to clean up the resources, returning in the middle of the function when something goes wrong is not a good option. This is because all resources already acquired have to be cleaned up before each return statement. So you end up with multiple points in the code where the same resource is being cleaned up, but you don’t want to have duplicated error handling and cleanup code.

## Solution

**Call resource acquisition functions as long as they succeed, and store which functions require cleanup. Call the cleanup functions depending on these stored values.**

In C, lazy evaluation of `if` statements can be used to achieve this. Simply call a sequence of functions inside a single `if` statement as long as these functions succeed. For each function call, store the acquired resource in a variable. Have the code operating on the resources in the body of the `if` statement, and have all resource cleanup after the `if` statement only if the resource was successfully acquired. The following code shows an example of this:

```
void someFunction()
{
  if((r1=allocateResource1()) && (r2=allocateResource2()))
  {
    mainFunctionality();
  }
  if(r1) 
  {
    cleanupResource1();
  }
  if(r2) 
  {
    cleanupResource2();
  }
}
```

[![1](images/1.png)](#co_error_handling_CO2-1)  
To make the code easier to read, you can alternatively put these checks inside the cleanup functions. This is a good approach if you have to provide the resource variable to the cleanup function anyway.

## Consequences

You now have no nested `if` statements anymore, and you still have one central point at the end of the function for resource cleanup. That makes the code a lot easier to read because the main program flow is no longer obscured by error handling.

Also, the function is easy to read because it has a single exit point. However, the fact that you have to have many variables for keeping track of which resources were successfully allocated makes the code more complicated. Maybe an Aggregate Instance can help to structure the resource variables.

If many resources are being acquired, then many functions are being called in the single `if` statement. That makes the `if` statement very hard to read and even harder to debug. Therefore, if many resources are being acquired, it is a much better solution to have Object-Based Error Handling.

Another reason for having Object-Based Error Handling instead is that the preceding code is still complicated because it has a single function that contains the main functionality as well as resource allocation and cleanup. So one function has multiple responsibilities.

## Known Uses

The following examples show applications of this pattern:

- In the Portland Pattern Repository, a similar solution where each of the called functions registers a cleanup handler to a callback list is presented. For cleanup, all functions from the callback list are called.

- The OpenSSL function `dh_key2buf` uses lazy evaluation in an `if` statement to keep track of allocated bytes that are then cleaned up later on.

- The function `cap_open_socket` of the Wireshark network sniffer uses lazy evaluation of an `if` statement and stores the resources allocated in this `if` statement in variables. At cleanup, these variables are then checked, and if the resource allocation was successful, the resource is cleaned up.

- The `nvram_commit` function of the OpenWrt source code allocates its resources inside an `if` statement and stores these resources to a variable right inside that `if` statement.

## Applied to Running Example

Now, instead of `goto` statements and nested `if` statements, you have a single `if` statement. The advantage of not using `goto` statements in the following code is that the error handling is well separated from the main program flow:

```
int parseFile(char* file_name)
{
  int return_value = ERROR;
  FILE* file_pointer = 0;
  char* buffer = 0;

  assert(file_name!=NULL && "Invalid filename");
  if((file_pointer=fopen(file_name, "r")) &&
     (buffer=malloc(BUFFER_SIZE)))
  {
    return_value = searchFileForKeywords(buffer, file_pointer);
  }
  if(file_pointer)
  {
    fclose(file_pointer);
  }
  if(buffer)
  {
    free(buffer);
  }
  return return_value;
}
```

Still, the code does not look nice. This one function has a lot of responsibilities: resource allocation, resource deallocation, file handling, and error handling. These responsibilities should be split into different functions with Object-Based Error Handling.

# Object-Based Error Handling

## Context

You have a function that acquires and cleans up multiple resources. Maybe you already tried to reduce the complexity by applying Guard Clause, Function Split, or Samurai Principle, but you still have a deeply nested `if` construct in the code, because of resource acquisition. You might even have duplicated code for resource cleanup. But maybe you already got rid of nested `if` statements by using Goto Error Handling or a Cleanup Record.

## Problem

**Having multiple responsibilities in one function, such as resource acquisition, resource cleanup, and usage of that resource, makes that code difficult to implement, read, maintain, and test.**

All of that becomes difficult because usually each resource acquisition can fail, and each resource cleanup can just be called if the resource was successfully acquired. To implement this, a lot of `if` statements are required, and when implemented poorly, nested `if` statements in a single function make the code hard to read and maintain.

Because you have to clean up the resources, returning in the middle of the function when something goes wrong is not a good option. This is because all resources already acquired have to be cleaned up before each return statement. So you end up with multiple points in the code where the same resource is being cleaned up, but you don’t want to have duplicated error handling and cleanup code.

Even if you already have a Cleanup Record or Goto Error Handling, the function is still hard to read because it mixes different responsibilities. The function is responsible for acquisition of multiple resources, error handling, and cleanup of multiple resources. However, a function should only have one responsibility.

## Solution

**Put initialization and cleanup into separate functions, similar to the concept of constructors and destructors in object-oriented programming.**

In your main function, simply call one function that acquires all resources, one function that operates in these resources, and one function that cleans up the resources.

If the acquired resources are not global, then you have to pass the resources along the functions. When you have multiple resources, you can pass an Aggregate Instance containing all resources along the functions. If you want to instead hide the actual resources from the caller, you can use a Handle for passing the resource information between the functions.

If resource allocation fails, store this information in a variable (for example, a `NULL` pointer if memory allocation fails). When using or cleaning up the resources, first check whether the resource is valid. Perform that check not in your main function, but rather in the called functions, because that makes your main function a lot more readable:

```
void someFunction()
{
  allocateResources();
  mainFunctionality();
  cleanupResources();
}
```

## Consequences

The function is now easy to read. While it requires allocation and cleanup of multiple resources, as well as the operations on these resources, these different tasks are still well separated into different functions.

Having object-like instances that you pass along functions is known as an “object-based” programming style. This style makes procedural programming more similar to object-oriented programming, and thus code written in such a style is also more familiar to programmers who are used to object-orientation.

In the main function, there is no reason for having multiple return statements anymore, because there are no more nested `if` statements for the logic of resource allocation and cleanup. However, you did not eliminate the logic regarding resource allocation and cleanup, of course. All this logic is still present in the separated functions, but it is not mixed with the operation on the resources anymore.

Instead of having a single function, you now have multiple functions. While that could have a negative impact on performance, it usually does not matter a lot. The performance impact is minor, and for most applications it is not relevant.

## Known Uses

The following examples show applications of this pattern:

- This form of cleanup is used in object-oriented programming where constructors and destructors are implicitly called.

- The OpenSSL code uses this pattern. For example, the allocation and cleanup of buffers is realized with the functions `BUF_MEM_new` and `BUF_MEM_free` that are called across the code to cover buffer handling.

- The `show_help` function of the OpenWrt source code shows help information in a context menu. The function calls an initialization function to create a `struct`, then operates on that `struct` and calls a function to clean up that `struct`.

- The function `cmd__windows_named_pipe` of the Git project uses a Handle to create a pipe, then operates on that pipe and calls a separate function to clean up the pipe.

## Applied to Running Example

You finally end up with the following code, in which the `parseFile` function calls other functions to create and clean up a parser instance:

```
typedef struct
{
  FILE* file_pointer;
  char* buffer;
}FileParser;

int parseFile(char* file_name)
{
  int return_value;
  FileParser* parser = createParser(file_name);
  return_value = searchFileForKeywords(parser);
  cleanupParser(parser);
  return return_value;
}

int searchFileForKeywords(FileParser* parser)
{
  if(parser == NULL)
  {
    return ERROR;
  }
  while(fgets(parser->buffer, BUFFER_SIZE, parser->file_pointer)!=NULL)
  {
    if(strcmp("KEYWORD_ONE\n", parser->buffer)==0)
    {
      return KEYWORD_ONE_FOUND_FIRST;
    }
    if(strcmp("KEYWORD_TWO\n", parser->buffer)==0)
    {
      return KEYWORD_TWO_FOUND_FIRST;
    }
  }
  return NO_KEYWORD_FOUND;
}

FileParser* createParser(char* file_name)
{
  assert(file_name!=NULL && "Invalid filename");
  FileParser* parser = malloc(sizeof(FileParser));
  if(parser)
  {
    parser->file_pointer=fopen(file_name, "r");
    parser->buffer = malloc(BUFFER_SIZE);
    if(!parser->file_pointer || !parser->buffer)
    {
      cleanupParser(parser);
      return NULL;
    }
  }
  return parser;
}

void cleanupParser(FileParser* parser)
{
  if(parser)
  {
    if(parser->buffer)
    {
      free(parser->buffer);
    }
    if(parser->file_pointer)
    {
      fclose(parser->file_pointer);
    }
    free(parser);
  }
}
```

In the code, there is no more `if` cascade in the main program flow. This makes the `parseFile` function a lot easier to read, debug, and maintain. The main function does not cope with resource allocation, resource deallocation, or error handling details anymore. Instead, those details are all put into separate functions, so each function has one responsibility.

Have a look at the beauty of this final code example compared to the first code example. The applied patterns helped step-by-step to make the code easier to read and maintain. In each step, the nested `if` cascade was removed and the method of how to handle errors was improved.

# Summary

This chapter showed you how to perform error handling in C. Function Split tells you to split your functions into smaller parts to make error handling of these parts easier. A Guard Clause for your functions checks pre-conditions of your function and returns immediately if they are not met. This leaves fewer error-handling obligations for the rest of that function. Instead of returning from the function, you could also abort the program, adhering to the Samurai Principle. When it comes to more complex error handling—particularly in combination with acquiring and releasing resources—you have several options. Goto Error Handling makes it possible to jump forward in your function to an error-handling section. Instead of jumping, Cleanup Record stores the info, which resources require cleanup, and performs it by the end of the function. A method of resource acquisition that is closer to object-oriented programming is Object-Based Error Handling, which uses separate initialization and cleanup functions similar to the concept of constructors and destructors.

With these error-handling patterns in your repertoire, you now have the skill to write small programs that handle error situations in a way that ensures the code stays maintainable.

# Further Reading

If you’re ready for more, here are some resources that can help you further your knowledge of error handling.

- The [Portland Pattern Repository](https://oreil.ly/qFLdA) provides many patterns and discussions on error handling as well as other topics. Most of the error-handling patterns target exception handling or how to use assertions, but some C patterns are also presented.

- A comprehensive overview of error handling in general is provided in the master’s thesis “Error Handling in Structured and Object-Oriented Programming Languages” by Thomas Aglassinger (University of Oulu, 1999). This thesis describes how different kinds of errors arise; discusses error-handling mechanisms of the programming languages C, Basic, Java, and Eiffel; and provides best practices for error handling in these languages, such as reversing the cleanup order of resources compared to the order of their allocation. The thesis also mentions several third-party solutions in the form of C libraries providing enhanced error handling features for C, like exception handling by using the commands `setjmp` and `longjmp`.

- Fifteen object-oriented patterns on error handling tailored for business information systems are presented in the article [“Error Handling for Business Information Systems”](https://oreil.ly/bQnfx) by Klaus Renzel, and most of the patterns can be applied for non-object-oriented domains as well. The presented patterns cover error detection, error logging, and error handling.

- Implementations including C code snippets for some Gang of Four design patterns are presented in the book *Patterns in C* by Adam Tornhill (Leanpub, 2014). The book further provides best practices in the form of C patterns, some of them covering error handling.

- A collection of patterns for error logging and error handling is presented in the articles “Patterns for Generation, Handling and Management of Errors” and “More Patterns for the Generation, Handling and Management of Errors” by [Andy Longshaw and Eoin Woods](https://oreil.ly/7Yj8h). Most of the patterns target exception-based error handling.

# Outlook

The next chapter shows you how to handle errors when looking at larger programs that return error information across interfaces to other functions. The patterns tell you which kind of error information to return and how to return it.

