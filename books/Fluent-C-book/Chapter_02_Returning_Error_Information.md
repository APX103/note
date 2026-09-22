# Chapter 2. Returning Error Information

The previous chapter focused on error handling. This chapter continues this discussion, but focuses on how to inform users of your code about the errors detected.

For every larger program, programmers have to decide how to react to errors arising in their own code, how to react to errors arising in third-party code, how to pass this error information along in the code, and how to present this error information to the user.

Most object-oriented programming languages come with the handy mechanism of exceptions to provide the programmer with an additional channel for returning error information, but C does not natively provide such a mechanism. There are ways to emulate exception handling or even inheritance among exceptions in C, for example as described in the book [*Object-Oriented Programming with ANSI-C*](https://oreil.ly/YK7x1) by Axel-Tobias Schreiner (2011). But for C programmers working on legacy C code or for C programmers who want to stick to the native C style they are used to, introducing such exception mechanisms is not the way to go. Instead, such C programmers need guidance on how to use the mechanisms for error handling already natively present in C.

This chapter provides such guidance on how error information can be transported between functions and across interfaces. [Figure 2-1](#fig_returning_errors) shows an overview of the patterns covered in this chapter and their relationships, and [Table 2-1](#tab_returning_errors) provides a summary of the patterns.

![Overview of patterns on returning error information](images/fluc_0201.png)

###### Figure 2-1. Overview of patterns for returning error information

|  | Pattern name | Summary |
|----|----|----|
|  | Return Status Codes | You want to have a mechanism to return status information to the caller, so that the caller can react to it. You want the mechanism to be simple to use, and the caller should be able to clearly distinguish between different error situations that could occur. Therefore, use the Return Value of a function to return status information. Return a value that represents a specific status. Both of you as the callee and the caller must have a mutual understanding of what the value means. |
|  | Return Relevant Errors | On the one hand, the caller should be able to react to errors; on the other hand, the more error information you return, the more your code and the code of your caller have to deal with error handling, which makes the code longer. Longer code is harder to read and maintain and brings in the risk of additional bugs. Therefore, only return error information to the caller if that information is relevant to the caller. Error information is only relevant to the caller if the caller can react to that information. |
|  | Special Return Values | You want to return error information, but don’t want to explicitly Return Status Codes, because that makes it difficult for your function to return other data. You could add Out-Parameters to your function, but it would make calling the function more difficult. Therefore, use the Return Value of your function to return the data computed by the function. Reserve one or more special values to be returned if an error occurs. |
|  | Log Errors | You want to make sure that in case of an error you can easily find out its cause. However, you don’t want your error-handling code to become complicated because of this. Therefore, use different channels to return error information that is relevant for the calling code and error information that is relevant for the developer. For example, write debug error information into a log file and don’t return the detailed debug error information to the caller. |

Table 2-1. Patterns for returning error information

# Running Example

You want to implement a software-module that provides functionality to store string-values for keys identified via strings. In other words, you want to implement a functionality similar to the Windows registry. To keep things simple, the following code will not contain hierarchical relationships between the keys, and only functions to create registry elements will be discussed:

*Registry API*

```
/* Handle for registry keys */
typedef struct Key* RegKey;

/* Create a new registry key identified via the provided 'key_name' */
RegKey createKey(char* key_name);

/* Store the provided 'value' to the provided 'key' */
void storeValue(RegKey key, char* value);

/* Make the key available for being read (by other
   functions that are not part of this code example) */
void publishKey(RegKey key);
```

*Registry implementation*

```
#define STRING_SIZE 100
#define MAX_KEYS 40

struct Key
{
  char key_name[STRING_SIZE];
  char key_value[STRING_SIZE];
};

/* file-global array holding all registry keys */
static struct Key* key_list[MAX_KEYS];

RegKey createKey(char* key_name)
{
  RegKey newKey = calloc(1, sizeof(struct Key));
  strcpy(newKey->key_name, key_name);
  return newKey;
}

void storeValue(RegKey key, char* value)
{
  strcpy(key->key_value, value);
}

void publishKey(RegKey key)
{
  int i;
  for(i=0; i<MAX_KEYS; i++)
  {
    if(key_list[i] == NULL)
    {
      key_list[i] = key;
      return;
    }
  }
}
```

With the preceding code, you are not sure how you should provide your caller with error information in case of internal errors or, for example, in case of invalid function input parameter values. Your caller does not really know whether the calls succeeded or whether something failed and ends up with the following code:

```
RegKey my_key = createKey("myKey");
storeValue(my_key, "A");
publishKey(my_key);
```

The caller’s code is very short and easy to read, but the caller does not know whether any error occurred and is not able to react to errors. To give the caller that possibilitym you want to introduce error handling in your code and provide your caller with error information. The first idea that comes to your mind is to let the caller know about any errors showing up in your software-module. To do that, you Return Status Codes.

# Return Status Codes

## Context

You implement a software-module that performs some error handling, and you want to return error and other status information to your caller.

## Problem

**You want to have a mechanism to return status information to the caller, so that the caller can react to it. You want the mechanism to be simple to use, and the caller should be able to clearly distinguish between different error situations that could occur.**

In the old days of C, error information was transported by an error code with the global `errno` variable. The global `errno` variable had to be reset by the caller, then a function had to be called, and the function indicated errors by setting the global `errno` variable, which the caller had to check after the function call.

However, compared to using `errno`, you want a way to return status information that makes it easier for the caller to check for errors. The caller should see from the function signature how the status information will be returned and which kind of status information to expect.

Also, the mechanism to return status information should be safe to use in a multi-threaded environment, and only the called function should have the ability to influence the returned status information. In other words, it should be possible to use the mechanism and still have a reentrant function.

## Solution

**Use the Return Value of a function to return status information. Return a value that represents a specific status. Both of you as the callee and the caller must have a mutual understanding of what the value means.**

Usually, the returned value is a numeric identifier. The caller can check the function Return Value against that identifier and react accordingly. If the function has to return other function results, provide them to the caller in the form of Out-Parameters.

Define the numeric status identifiers in your API as an `enum` or by using `#define`. If there are many status codes or if your software-module consists of more than one header file, you could have a separate header file that just contains the status codes and is included by your other header files.

Give the status identifiers a meaningful name and document their meaning with comments. Make sure to name your status codes in a consistent way across your APIs.

The following code shows an example of using status codes:

*Caller’s code using status codes*

```
ErrorCode status = func();
if(status == MAJOR_ERROR)
{
  /* abort program */
}
else if(status == MINOR_ERROR)
{
  /* handle error */
}
else if(status == OK)
{
  /* continue normal execution */
}
```

\
*Callee API providing status codes*

```
typedef enum
{
  MINOR_ERROR,
  MAJOR_ERROR,
  OK
}ErrorCode;

ErrorCode func();
```

\
*Callee implementation providing status codes*

```
ErrorCode func()
{
  if(minorErrorOccurs())
  {
    return MINOR_ERROR;
  }
  else if(majorErrorOccurs())
  {
    return MAJOR_ERROR;
  }
  else
  {
    return OK;
  }
}
```

## Consequences

You now have a way to return status information that makes it very easy for the caller to check for occurring errors. Compared to `errno`, the caller does not have to set and check the error information in steps in addition to the function call. Instead, the caller can check the information directly against the return value of the function call.

Returning status codes can safely be used in multithreaded environments. Callers can be sure that only the called function, and no other side-channels, influences the returned status.

The function signature makes it very clear how the status information is returned. This is made clear for the caller and also clear for the compiler or static code analysis tools, which can check if the caller checked the function return value and against all statuses that could occur.

As the function now provides different results in different error situations, these results have to be tested. Compared to a function without any error handling, more extensive testing has to be done. Also, the caller is burdened with having to check these error situations, which might blow up the size of the caller’s code.

Any C function can return only one object of the type specified in the function signature, and the function now returns the status code. Thus, you have to use more complicated techniques for returning other function results. You could do this using Out-Parameters, which have the drawback that an additional parameter is required, or you could return an Aggregate Instance that contains the status information and other function results.

## Known Uses

The following examples show applications of this pattern:

- Microsoft uses `HRESULT` to return status information. An `HRESULT` is a unique status code. Making the status code unique has the advantage that the status information can be transported across many functions while still making it possible to find out where that status originated. But making the status code unique brings in the additional effort of assigning status numbers and keeping track of who is allowed to use which status numbers. Another specialty of `HRESULT` is that it encodes specific information, such as the severity of an error, into the status code by using some bits dedicated to returning this information.

- The code of the Apache Portable Runtime defines the type `apr_status_t` to return error information. Any function that returns error information in this way returns `APR_SUCCESS` on success or any other value to indicate errors. Other values are uniquely defined error codes specified via `#define` statements.

- The OpenSSL code defines status codes in several header files (*dsaerr.h*, *kdferr.h*, …). As an example, the status codes `KDF_R_MISSING_PARAMETER` or `KDF_R_MISSING_SALT` inform the caller in detail about missing or wrong input parameters. The status codes in each of the files are defined only for a specific set of functions that belong to that file, and the status code values are not unique across the whole OpenSSL code.

- The pattern Error Code is described in the Portland Pattern Repository. It describes the idea of returning error information by explicitly using the function’s return value.

## Applied to Running Example

Now you provide your caller with information in case of errors in your code. In the following code you check for things that could go wrong and provide that information to the caller:

*Registry API*

```
/* Error codes returned by this registry */
typedef enum
{
  OK,
  OUT_OF_MEMORY,
  INVALID_KEY,
  INVALID_STRING,
  STRING_TOO_LONG,
  CANNOT_ADD_KEY
}RegError;

/* Handle for registry keys */
typedef struct Key* RegKey;

/* Create a new registry key identified via the provided 'key_name'.
   Returns OK if no problem occurs, INVALID_KEY if the 'key'
   parameter is NULL, INVALID_STRING if 'key_name' is NULL,
   STRING_TOO_LONG if 'key_name' is too long, or OUT_OF_MEMORY
   if no memory resources are available. */
RegError createKey(char* key_name, RegKey* key);

/* Store the provided 'value' to the provided 'key'.
   Returns OK if no problem occurs, INVALID_KEY if the 'key'
   parameter is NULL, INVALID_STRING if 'value' is NULL, or
   STRING_TOO_LONG if 'value' is too long. */
RegError storeValue(RegKey key, char* value);

/* Make the key available for being read. Returns OK if no
   problem occurs, INVALID_KEY if 'key' is NULL, or CANNOT_ADD_KEY
   if the registry is full and no more keys can be published. */
RegError publishKey(RegKey key);
```

\
*Registry implementation*

```
#define STRING_SIZE 100
#define MAX_KEYS 40

struct Key
{
  char key_name[STRING_SIZE];
  char key_value[STRING_SIZE];
};

/* file-global array holding all registry keys */
static struct Key* key_list[MAX_KEYS];

RegError createKey(char* key_name, RegKey* key)
{
  if(key == NULL)
  {
    return INVALID_KEY;
  }

  if(key_name == NULL)
  {
    return INVALID_STRING;
  }

  if(STRING_SIZE <= strlen(key_name))
  {
    return STRING_TOO_LONG;
  }

  RegKey newKey = calloc(1, sizeof(struct Key));
  if(newKey == NULL)
  {
    return OUT_OF_MEMORY;
  }

  strcpy(newKey->key_name, key_name);
  *key = newKey;
  return OK;
}

RegError storeValue(RegKey key, char* value)
{
  if(key == NULL)
  {
    return INVALID_KEY;
  }

  if(value == NULL)
  {
    return INVALID_STRING;
  }

  if(STRING_SIZE <= strlen(value))
  {
    return STRING_TOO_LONG;
  }

  strcpy(key->key_value, value);
  return OK;
}

RegError publishKey(RegKey key)
{
  int i;
  if(key == NULL)
  {
    return INVALID_KEY;
  }

  for(i=0; i<MAX_KEYS; i++)
  {
    if(key_list[i] == NULL)
    {
      key_list[i] = key;
      return OK;
    }
  }

  return CANNOT_ADD_KEY;
}
```

Now the caller can react to the provided error information and can, for example, provide the user of the application with detailed information about what went wrong:

*Caller’s code*

```
  RegError err;
  RegKey my_key;

  err = createKey("myKey", &my_key);
  if(err == INVALID_KEY || err == INVALID_STRING)
  {
    printf("Internal application error\n");
  }
  if(err == STRING_TOO_LONG)
  {
    printf("Provided registry key name too long\n");
  }
  if(err == OUT_OF_MEMORY)
  {
    printf("Insufficient resources to create key\n");
  }

  err = storeValue(my_key, "A");
  if(err == INVALID_KEY || err == INVALID_STRING)
  {
    printf("Internal application error\n");
  }
  if(err == STRING_TOO_LONG)
  {
    printf("Provided registry value to long to be stored to this key\n");
  }

  err = publishKey(my_key);
  if(err == INVALID_KEY)
  {
    printf("Internal application error\n");
  }
  if(err == CANNOT_ADD_KEY)
  {
    printf("Key cannot be published, because the registry is full\n");
  }
```

The caller can now react to errors, but the code for the registry software-module as well as the code for the caller have more than doubled in size. The caller code could be cleaned up a little by having a separate function for mapping the error code to error texts, but the majority of that code would still cope with error handling.

You can see that error handling did not come for free. A lot of effort was put into implementing error handling. This can also be seen in the registry API. The comments for the functions became a lot longer because they have to describe which error situations can occur. The caller also has to put a lot of effort into thinking about what to do if a specific error occurs.

When providing such detailed error information to the caller, you burden the caller with reacting to these errors and thinking about which errors are relevant to handle and which are irrelevant. Thus, special care has to be taken to on the one hand, provide the caller with the necessary error information, but on the other hand, not to flood the caller with unnecessary information.

Next, you want to make these considerations in your code, and you only want to provide error information that is actually useful to the caller. Thus, you only Return Relevant Errors.

# Return Relevant Errors

## Context

You implement a software-module that performs some error handling, and you want to return error information to your caller.

## Problem

**On the one hand, the caller should be able to react to errors; on the other hand, the more error information you return, the more your code and the code of your caller have to deal with error handling, which makes the code longer. Longer code is harder to read and maintain and brings in the risk of additional bugs.**

In order to return error information to your caller, detecting the error and returning the information are not your only tasks. You also have to document in your API which errors are returned. If you don’t do that, then your caller will not know which errors to expect and handle. Documenting error behavior is work that has to be done. The more types of errors there are, the more documentation work has to be done.

Returning very detailed, implementation-specific error information and adding additional error information later on in your code if the implementation changes implies that with such an implementation change, you have to semantically change your interface that documents the returned error information. Such changes might not be desirable for your existing callers because they would have to adapt their code to react to the newly introduced error information.

Providing detailed error information is also not always a good thing for the caller either. Each error information returned to the caller means additional work for the caller. The caller has to decide if the error information is relevant and how to handle it.

## Solution

**Only return error information to the caller if that information is relevant to the caller. Error information is only relevant to the caller if the caller can react to that information.**

If the caller cannot react to the error information, then it would be unnecessary to provide the caller the opportunity (or the burden) to do so.

There are several ways to return only relevant error information. One extreme way is to simply not return any error information at all. For example, when you have a function `cleanupMemory (void* handle)` that cleans up memory, there is no need to return information if the cleanup succeeded because the caller cannot react in the code to such a cleanup error (retrying to call a cleanup function is in most cases not a solution). Thus the function simply does not return any error information. To make sure that errors within the function do not go unnoticed, aborting the program in case of error (Samurai Principle) might even be an option.

Or imagine the only reason why you return the error to the caller is so the caller can then log this error. In that case, do not return the error to the caller, but instead simply Log Errors yourself in order to make life easier for the caller.

If you already Return Status Codes, then only the error information that is relevant to the caller should be returned. Other errors that occur can be summarized as one internal error code. Also, detailed error codes from the functions you call need not necessarily all be returned by your function. They can be summarized as one internal error code as shown in the following code:

*Caller’s code*

```
ErrorCode status = func();
if(status == MAJOR_ERROR || status == UNKNOWN_ERROR)
{
  /* abort program */
}
else if(status == MINOR_ERROR)
{
  /* handle error */
}
else if(status == OK)
{
  /* continue normal execution*/
}
```

\
*API*

```
typedef enum
{
  MINOR_ERROR,
  MAJOR_ERROR,
  UNKNOWN_ERROR,
  OK
}ErrorCode;

ErrorCode func();
```

\
*Implementation*

```
ErrorCode func()
{
  if(minorErrorOccurs())
  {
    return MINOR_ERROR;
  }
  else if(majorErrorOccurs())
  {
    return MAJOR_ERROR;
  }
  else if(internalError1Occurs() || internalError2Occurs())
  {
    return UNKNOWN_ERROR; 
  }
  else
  {
    return OK;
  }
}
```

[![1](images/1.png)](#co_returning_error_information_CO1-1)  
You return the same error information if `internalError1Occurs` or `internal​Er⁠ror2Occurs` because it is irrelevant to the caller which of the two implementation-specific errors occurs. The caller would react to both errors in the same way (in the preceding example, the reaction is to abort the program).

If more detailed error information is needed for debugging purposes, you could Log Errors. If you realize that there are not many error situations after returning only relevant errors, then instead of error codes, it might be a better solution to simply have Special Return Values to return the error information.

## Consequences

Not returning detailed information about which kind of internal errors occurred is a relief for the caller. The caller is not burdened with thinking about how to handle all possible internal errors that occur, and it is more likely that the caller will react to all the errors that are returned because all of the returned errors are relevant for the caller. Also, testers can be happy, because now that fewer error information is returned by the functions, fewer error situations have to be tested.

If the caller uses very strict compilers or static code analysis tools that verify whether the caller checks for all possible return values, the caller does not have to explicitly handle irrelevant errors (for example, a switch statement with many fallthroughs and one central error-handling code for all internal errors). Instead, the caller only handles one internal error code, or if you abort the program on error, the caller does not have to handle any errors.

Not returning the detailed error information makes it impossible for the caller to show this error information to the user or to save this error information for the developer for debugging purposes. However, for such debugging purposes, it would be better to Log Errors directly in the software-module where they occur and not burden the caller with doing that.

If you don’t return all information about errors occurring in your function, but instead you return only information that you think is relevant to the caller, then there is the chance that you get it wrong. You might forget some information that is necessary for the caller, and maybe that leads to a change request for adding this information. But if you Return Status Codes, additional error codes can easily be added without changing the function signature.

## Known Uses

The following examples show applications of this pattern:

- For security-relevant code it is very common to return only relevant information in case of errors. For example, if a function to authenticate a user returns detailed information about why authentication is not working because the username or password is invalid, then the caller could use this function to check which usernames are already taken. To avoid opening side-channels with this information, it is common to return only the binary information about whether authentication worked or not. For example, the function `rbacAuthenticateUserPassword` used to authenticate users in the B&R Automation Runtime operating system has the return type `bool` and returns `true` if the authentication worked or `false` if it did not work. No detailed information about why the authentication did not work is returned.

- The function `FlushWinFile` of the game NetHack flushes a file to the disk calling the Macintosh function `FSWrite`, which does return error codes. However, the NetHack wrapper explicitly ignores the error code, and `FlushWinFile` is of return type `void` because the code using that function cannot react accordingly if an error occurs. Thus, the error information is not passed along.

- The OpenSSL function `EVP_CIPHER_do_all` initializes cipher suites with the internal function `OPENSSL_init_crypto`, which Returns Status Codes. However, this detailed error information is ignored by the `EVP_CIPHER_do_all` function because it is of return type `void`. So the strategy of returning detailed error information is changed by the wrapping function to only Return Relevant Errors, which in this case is no error information at all.

## Applied to Running Example

When you only Return Relevant Errors, your registry code looks like the following. To keep things simple, only the `createKey` function is shown here:

*Implementation of the function* *`createKey`*

```
RegError createKey(char* key_name, RegKey* key)
{
  if(key == NULL || key_name == NULL)
  {
    return INVALID_PARAMETER; 
  }

  if(STRING_SIZE <= strlen(key_name))
  {
    return STRING_TOO_LONG;
  }

  RegKey newKey = calloc(1, sizeof(struct Key));
  if(newKey == NULL)
  {
    return OUT_OF_MEMORY;
  }

  strcpy(newKey->key_name, key_name);
  *key = newKey;
  return OK;
}
```

[![1](images/1.png)](#co_returning_error_information_CO2-1)  
Instead of returning `INVALID_KEY` or `INVALID_STRING`, you now return `INVALID_PARAMETER` for all these error cases.

Now the caller cannot handle specific invalid parameters differently, which also means the caller does not have to think about how to handle these error situations differently. The caller code becomes simpler because now there is one less error situation to be handled.

That is good, because what would the caller do if the function returns `INVALID_KEY` or `INVALID_STRING`? It wouldn’t make any sense for the caller to try calling the function again. In both cases the caller could just accept that calling the function did not work and report that to the user or abort the program. As there would be no reason for the caller to react differently to the two errors, you have relieved the caller of the burden of thinking about two different error situations. Now the caller only has to think about one error situation and then react accordingly.

To make things even easier, you next apply the Samurai Principle. Instead of returning all of these error codes, you handle some of the errors by aborting the program:

*Declaration of the function* *`createKey`*

```
/* Create a new registry key identified via the provided 'key_name'
   (must not be NULL, max. STRING_SIZE characters). Stores a handle
   to the key in the provided 'key' parameter (must not be NULL).
   Returns OK on success, or OUT_OF_MEMORY in case of insufficient memory. */
RegError createKey(char* key_name, RegKey* key);
```

\
*Implementation of the function* *`createKey`*

```
RegError createKey(char* key_name, RegKey* key)
{
  assert(key != NULL && key_name != NULL); 
  assert(STRING_SIZE > strlen(key_name)); 

  RegKey newKey = calloc(1, sizeof(struct Key));
  if(newKey == NULL)
  {
    return OUT_OF_MEMORY;
  }

  strcpy(newKey->key_name, key_name);
  *key = newKey;
  return OK;
}
```

[![1](images/1.png)](#co_returning_error_information_CO3-1)  
Instead of returning an `INVALID_PARAMETER` or `STRING_TOO_LONG`, you now abort the program if one of the provided parameters is not what you expect it to be.

Aborting in case of too long strings seems a bit drastic at first. However, similar to `NULL` pointers, a too long string is invalid input for your function. If your registry does not get its string input from a user via a GUI, but instead gets a fixed input from the caller’s code, then for too long strings this code only aborts in case of programming errors, which is perfectly fine behavior.

Next, you realize that the `createKey` function returns only two different error codes: `OUT_OF_MEMORY` and `OK`. Your code can be made much more beautiful by simply providing this kind of error information with Special Return Values.

# Special Return Values

## Context

You have a function that computes some result, and you want to provide error information to your caller if an error occurs when executing the function. You only want to Return Relevant Errors.

## Problem

**You want to return error information, but don’t want to explicitly Return Status Codes because that makes it difficult for your function to return other data. You could add Out-Parameters to your function, but this would make calling the function more difficult.**

Returning no error information at all is also not an option for you. You want to provide your caller with some error information, and you want your caller to be able to react to these errors. There is not a lot of error information that you want to provide to your caller. It might be just the binary information about whether the function call worked or not. To Return Status Codes for such simple information would be overkill.

You cannot apply the Samurai Principle and abort the program because the errors occurring in your function are not severe. Or maybe you want to make it possible for the caller to decide how the errors should be handled because the caller can handle the errors gracefully.

## Solution

**Use the Return Value of your function to return the data computed by the function. Reserve one or more special values to be returned if an error occurs.**

If, for example, your function returns a pointer, then you could use the `NULL` pointer as a reserved special value to indicate that some error occurred. The `NULL` pointer is by definition an invalid pointer, so you can be sure that this special value is not confused with a valid pointer calculated by your function as a result. The following code shows how to return error information when using pointers:

*Callee implementation*

```
void* func()
{
  if(somethingGoesWrong())
  {
    return NULL;
  }
  else
  {
    return some_pointer;
  }
}
```

\
*Caller’s code*

```
pointer = func();
if(pointer != NULL)
{
  /* operate on the pointer */
}
else
{
  /* handle error */
}
```

You have to make sure to document in the API which returned special value has which meaning. In some cases, a common convention settles which special values indicate errors. For example, very often negative integer values are used to indicate errors. Still, even in such cases the meaning of the specific return values has to be documented.

You have to make sure that the special value that indicates error information is a value that cannot occur in case of no error. For example, if a function returns a temperature value in degrees Celsius as an integer value, then it would not be a good idea to stay with the UNIX convention where any negative value indicates an error. Instead, it would be better to use, for example, the value –300 to indicate an error, because it is physically impossible that a temperature takes a value below –273 degrees Celsius.

## Consequences

The function can now return error information via the Return Value even though the Return Value is used to return the computation result of the function. No additional Out-Parameters have to be used just to provide error information.

Sometimes you don’t have many special values to encode error information. For example, for pointers there is only the `NULL` pointer to indicate error information. That leads to the situation in which it is only possible to indicate to the caller whether everything worked well or whether anything went wrong. This has the drawback that you cannot return detailed error information. However, this also has the benefit that you are not tempted to return unnecessary error information. In many cases, it is sufficient to provide only the information that something went wrong, and the caller cannot react to more detailed information anyway.

If, at a later point in time, you realize that you have to provide more detailed error information, then perhaps that is not possible anymore because you have no more unused special values left. You’d have to change the whole function signature and instead Return Status Codes to provide that additional error information. Changing the function signature might not always be an option because your API might have to stay compatible for existing callers. If you expect such future changes, don’t use Special Return Values, but instead Return Status Codes right away.

Sometimes programmers assume that it is clear which returned values indicate errors. For example, to some programmers it might be clear that a `NULL` pointer indicates an error. For some other programmers it might be clear that –1 indicates an error. This brings in the dangerous situation in which the programmers assume that it is clear to everybody which values indicate errors. However, these are just assumptions. In any case it should be well documented in the API which values indicate errors, but sometimes programmers forget to do that, wrongly assuming that it is absolutely clear.

## Known Uses

The following examples show applications of this pattern:

- The `getobj` function of the game NetHack returns the pointer to some object if no error occurs and returns `NULL` if an error occurs. To indicate the special case that there is no object to return, the function returns the pointer to a global object called `zeroobj` that is an object of the return type defined for the function and that is also known to the caller. The caller can then check if the returned pointer is the same as the pointer to the global object and can thus distinguish between a pointer to any valid object and a pointer to the `zeroobj` that carries some special meaning.

- The C standard library function `getchar` reads a character from `stdin`. The function has return type `int` which allows returning much more information than simple characters. If no more characters are available, the function returns `EOF`, which is usually defined as −1. As characters cannot take negative integer representations, `EOF` can clearly be distinguished from regular function results and can thus be used to indicate the special situation in which no more characters are available.

- Most UNIX or POSIX function use negative numbers to indicate error information. For example, the POSIX function `write` returns the number of written bytes or −1 on error.

## Applied to Running Example

With Special Return Values, your code looks like the following. To keep it simple, only the `createKey` function is shown:

*Declaration of the function* *`createKey`*

```
/* Create a new registry key identified via the provided 'key_name'
   (must not be NULL, max. STRING_SIZE characters).
   Returns a handle to the key or NULL on error. */
RegKey createKey(char* key_name);
```

\
*Implementation of the function* *`createKey`*

```
RegKey createKey(char* key_name)
{
  assert(key_name != NULL);
  assert(STRING_SIZE > strlen(key_name));

  RegKey newKey = calloc(1, sizeof(struct Key));
  if(newKey == NULL)
  {
    return NULL;
  }

  strcpy(newKey->key_name, key_name);
  return newKey;
}
```

The `createKey` function is much simpler now. It does not Return Status Codes anymore, but instead it directly returns the handle and no Out-Parameter is needed to return this information. The API documentation for the function also becomes much simpler because there is no need to describe the additional parameter and no need to lengthily describe how the function result will be returned to the caller.

Things also are much simpler for your caller. The caller does not have to provide a handle as an Out-Parameter anymore, but instead the caller directly retrieves this handle via the Return Value, which makes the caller’s code a lot more readable and thus easier to maintain.

However, now you have the problem that compared to the detailed error information that you can provide if you Return Status Codes, the only error information that comes out of the function is whether it worked or not. The internal details about the error are thrown away, and if you need these details later on, for example, as debugging information, there is no way to get it. To address that issue, you can Log Errors.

# Log Errors

## Context

You have a function in which you handle errors. You want to only Return Relevant Errors to your caller for reacting to them in the code, but you want to keep detailed error information for later debugging.

## Problem

**You want to make sure that in case of an error you can easily find out its cause. However, you don’t want your error-handling code to become complicated because of this.**

One way to do this would be to return very detailed error information, such as error information indicating programming errors, directly to the caller. To do this you can Return Status Codes to the caller, who then displays the detailed error codes to the user. The user might get back to you (for example, via some service hotline) to ask what the error code means and how to fix the problem. Then you’d have your detailed error information to debug the code, and you could figure out what went wrong.

However, such an approach has the major drawback that the caller, who does not care at all about that error information, has to provide the error information to the user only for the sake of providing this error information to you. The user also does not really care about such detailed error information.

In addition, Return Status Codes has the drawback that you have to use the Return Value of the function to return error information, and you have to use additional Out-Parameters to provide the actual function results. In some cases, instead, you can provide error information via Special Return Values, but this is not always possible. You don’t want to have additional parameters for your function only to provide error information because it makes your caller’s code more complicated.

## Solution

**Use different channels to provide error information that is relevant for the calling code and error information that is relevant for the developer. For example, write debug error information into a log file and don’t return the detailed debug error information to the caller.**

If an error occurs, the user of the program has to provide you with the logged debug information so that you can easily find out the cause of the error. For example, the user has to send you a log file via email.

Alternatively, you could log the error at the interface between you and your caller and also Return Relevant Errors to the caller. For example, the caller could be informed that some internal error occurred, but the caller does not see the details of what kind of error occurred. Thus, the caller could still handle the error in the code without requiring knowledge on how to handle very detailed errors, and you still wouldn’t be losing valuable debug information.

To not lose valuable debug information, you should log information about programming errors and unexpected errors. For such errors it is valuable to store information about their severity and where the error occurred—for example, the source code filename and the line number, or the backtrace. The C language comes with special macros to get information about the current line number (`__LINE__`), the current function (`__func__`), or the current file (`__FILE__`). The following code uses the `__func__` macro for logging:

```
void someFunction()
{
  if(something_goes_wrong)
  {
     logInFile("something went wrong", ERROR_CODE, __func__);
  }
}
```

To get more detailed logging, you could even trace your function calls and log their return information. That makes it easier to reverse-engineer error situations with these logs, but of course that logging also introduces computational overhead. For tracing return values of your function calls, you can use the following code:

```
#define RETURN(x)          \
do {                       \
  logInFile(__func__, x);  \
  return x;                \
} while (0)

int soneFunction()
{
  RETURN(-1);
}
```

The log information can be stored in files, as indicated in the preceding code. You’ll have to take care of special situations like not having enough memory to store the file or a crashing program while writing to the file. Handling such situations is not an easy task, but it is very important to have a robust code for your logging mechanism because later on you’ll rely on the log files for debugging purposes. If the data in these files is not correct, then you might be misled when hunting down coding errors.

##### Multiline Macros

By having a `do/while` loop around the statements in a macro, you can avoid problems like the one shown in the following code:

```
#define MACRO(x) \
x=1;             \
x=2;             \

if(x==0)
  MACRO(x)
```

The code does not use curly braces around its `if` body, and when reading the code you might think that the thing in the macro is only executed in case `x==0`. But actually when the macro expands, you end up with the following code:

```
if(x==0)
  x=1;
x=2;
```

The last line of the code is not inside the body of the `if` statement, which is not what was intended. To avoid problems like this one, it is a best practice to have a `do/while` loop around the statements in a macro.

## Consequences

You can obtain debug information without requiring your caller to handle or transport this information. That makes life for the caller a lot easier, because the caller does not have to handle or transport the detailed error information. Instead, you provide the detailed error information yourself.

In some cases, you might just want to log some error or situation that occurred, but that is completely irrelevant to the caller. Thus, you don’t even have to return any error information to the caller. For example, if you abort the program if the error occurs, the caller does not have to react to the error at all, and you can still make sure to not lose valuable debug information if you Log Errors. So there are no additional required parameters to your function in order to return error information, which makes calling your function a lot easier and helps the caller to keep the code clean.

You don’t lose this valuable error information and can still use it for debugging purposes to hunt down programming errors. To not lose this debug information, you provide it via a different channel, for example, via log files. However, you have to think about how to get to these log files. You could ask the users to send you the log file via email or, more advanced, you could implement some automatic bug report mechanism. Still, with both of these approaches you cannot be 100% sure that the log information really gets back to you. If the users do not want that, they could prevent it.

## Known Uses

The following examples show applications of this pattern:

- The Apache web server code uses the function `ap_log_error` that writes errors related to requests or connections to an error log. Such a log entry contains information about the filename and line of code where the error occurred as well as a custom string provided to the function by the caller. The log information is stored in an `error_log` file on the server.

- The B&R Automation Runtime operating system uses a logging system that allows programmers to provide logging information to the user via calling the function `eventLogWrite` from anywhere in the code. This makes it possible to provide information to the user without having to return this information across the whole calling stack up to some central logging component.

- The pattern Assertion Context from the book *Patterns in C* by Adam Tornhill (Leanpub, 2014) suggests aborting the program in case of errors and also logging information the about the reason for or the position of the crash by adding a string statement inside the `assert` call. If the `assert` fails, then the line of code containing the `assert` statement will be printed, which includes the added string.

## Applied to Running Example

After applying the patterns, you’ll get the following final code for your registry software-module. This code provides the caller with relevant error information, but does not require the caller to handle any internal error situations:

*Registry API*

```
/* max. size of string parameters (including NULL-termination) */
#define STRING_SIZE 100

/* Error codes returned by this registry */
typedef enum
{
  OK,
  CANNOT_ADD_KEY
}RegError;

/* Handle for registry keys */
typedef struct Key* RegKey;

/* Create a new registry key identified via the provided 'key_name'
   (must not be NULL, max. STRING_SIZE characters).  Returns a handle
   to the key or NULL on error. */
RegKey createKey(char* key_name);

/* Store the provided 'value' (must not be NULL, max. STRING_SIZE characters)
   to the 'key' (MUST NOT BE NULL) */
void storeValue(RegKey key, char* value);

/* Make the 'key' (must not be NULL) available for being read.
   Returns OK if no problem occurs or CANNOT_ADD_KEY if the
   registry is full and no more keys can be published. */
RegError publishKey(RegKey key);
```

*Registry implementation*

```
#define MAX_KEYS 40

struct Key
{
  char key_name[STRING_SIZE];
  char key_value[STRING_SIZE];
};

/* macro to log debug info and to assert */
#define logAssert(X)                        \
if(!(X))                                    \
{                                           \
  printf("Error at line %i", __LINE__);     \
  assert(false);                            \
}

/* file-global array holding all registry keys */
static struct Key* key_list[MAX_KEYS];

RegKey createKey(char* key_name)
{
  logAssert(key_name != NULL)
  logAssert(STRING_SIZE > strlen(key_name))

  RegKey newKey = calloc(1, sizeof(struct Key));
  if(newKey == NULL)
  {
    return NULL;
  }

  strcpy(newKey->key_name, key_name);
  return newKey;
}

void storeValue(RegKey key, char* value)
{
  logAssert(key != NULL && value != NULL)
  logAssert(STRING_SIZE > strlen(value))

  strcpy(key->key_value, value);
}

RegError publishKey(RegKey key)
{
  logAssert(key != NULL)

  int i;
  for(i=0; i<MAX_KEYS; i++)
  {
    if(key_list[i] == NULL)
    {
      key_list[i] = key;
      return OK;
    }
  }

  return CANNOT_ADD_KEY;
}
```

This code is shorter compared to the earlier code in the running example for these reasons:

- The code does not check for programming errors but aborts the program in case of programming errors. Invalid parameters like `NULL` pointers are not gracefully handled in the code; instead, the API documents that the handles must not be `NULL`.

- The code returns only errors that are relevant for the caller. For example, the `createKey` function does not Return Status Codes, but instead simply returns a handle and `NULL` in case of error because the caller does not need more detailed error information.

Although the code is shorter, the API comments grew. The comments now specify more clearly how the functions behave in case of errors. Apart from your code, the caller’s code also became simpler because now the caller is not burdened with many decisions on how to react to different kinds of error information:

*Caller’s code*

```
RegKey my_key = createKey("myKey");
if(my_key == NULL)
{
  printf("Cannot create key\n");
}

storeValue(my_key, "A");

RegError err = publishKey(my_key);
if(err == CANNOT_ADD_KEY)
{
  printf("Key cannot be published, because the registry is full\n");
}
```

This is shorter compared to the earlier code in the running example because:

- The return value of functions that abort in case of error does not have to be checked.

- Functions in which no detailed error information is required directly return the requested item. For example, `createKey()` now returns a handle, and the caller no longer has to provide an Out-Parameter.

- Error codes that indicate a programming error, for example, an invalid provided parameter, are not returned anymore and thus do not have to be checked by the caller.

The final code in the running example showed that it is important to think about which kinds of errors should be handled in the code and how these errors should be handled. Simply returning all kinds of errors and requiring the caller to cope with all of them is not always the best solution. The caller might not be interested in the detailed error information, or maybe the caller does not want to react to the error in the application. Maybe the error is severe enough that at the point where the error occurs it can be decided to abort the program. Such measures make the code simpler and have to be considered when designing the API of a software component.

# Summary

This chapter showed you how to handle errors across different functions and different parts of your software. The pattern Return Status Codes provides the caller with numeric codes representing an occurring error. Return Relevant Errors only returns error information to the caller if the caller can react to these errors in the code, and Special Return Value is one way to do that. Log Errors provides an additional channel to provide error information that is not intended for the caller, but for the user or for debugging purposes.

These patterns equip you with more tools for tackling error situations and can guide your first steps when implementing a larger piece of code.

# Further Reading

If you’re ready for more, here are some resources that can help you further your knowledge of returning error information:

- The master’s thesis *Error Handling in Structured and Object-Oriented Programming Languages* by Thomas Aglassinger (University of Oulu, 1999) provides a comprehensive overview of error handling in general and describes error handling best practices, with code examples for several programming languages including C.

- The [Portland Pattern Repository](https://oreil.ly/bs9FX) provides many patterns and discussions on error-handling as well as other topics. Most of the error handling patterns target exception handling, but some C idioms are also presented.

- The articles “Patterns for the Generation, Handling and Management of Errors” and “More Patterns for the Generation, Handling and Management of Errors” by [Andy Longshaw and Eoin Woods](https://oreil.ly/7Yj8h) present patterns for error logging and error handling with a focus on exception-based error handling.

# Outlook

The next chapter gives guidance on how to cope with dynamic memory. In order to return more complex data between your functions and to organize larger data and its lifetime throughout your application, you’ll need to deal with dynamic memory, and you’ll need advice on how to do that.

