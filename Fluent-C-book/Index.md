# Index

### Symbols

- \#ifdef statements
  - avoiding poorly implemented
    - Abstraction Layer pattern, [Context](Chapter_09_Escaping_ifdef_Hell.md)-[Applied to Running Example](Chapter_09_Escaping_ifdef_Hell.md), [Cross-Platform Files](Chapter_10_Implementing_Logging_Functionality.md)
    - Atomic Primitives pattern, [Context](Chapter_09_Escaping_ifdef_Hell.md)-[Applied to Running Example](Chapter_09_Escaping_ifdef_Hell.md), [Cross-Platform Files](Chapter_10_Implementing_Logging_Functionality.md)
    - Avoid Variants pattern, [Context](Chapter_09_Escaping_ifdef_Hell.md)-[Applied to Running Example](Chapter_09_Escaping_ifdef_Hell.md), [Cross-Platform Files](Chapter_10_Implementing_Logging_Functionality.md), [Authentication: Error Logging](Chapter_11_Building_a_User_Management_System.md)
    - further reading on, [Further Reading](Chapter_09_Escaping_ifdef_Hell.md)
    - Isolated Primitives pattern, [Context](Chapter_09_Escaping_ifdef_Hell.md)-[Applied to Running Example](Chapter_09_Escaping_ifdef_Hell.md), [Cross-Platform Files](Chapter_10_Implementing_Logging_Functionality.md)
    - overview of patterns for, [Escaping \#ifdef Hell](Chapter_09_Escaping_ifdef_Hell.md), [Summary](Chapter_09_Escaping_ifdef_Hell.md)
    - running example, [Running Example](Chapter_09_Escaping_ifdef_Hell.md)
    - Split Variant Implementations, [Context](Chapter_09_Escaping_ifdef_Hell.md)-[Applied to Running Example](Chapter_09_Escaping_ifdef_Hell.md), [Cross-Platform Files](Chapter_10_Implementing_Logging_Functionality.md)
  - protecting header files with, [Solution](Chapter_08_Organizing_Files_in_Modular_Programs.md)
  - weaknesses of, [Escaping \#ifdef Hell](Chapter_09_Escaping_ifdef_Hell.md)
- \#include statements, [Solution](Chapter_08_Organizing_Files_in_Modular_Programs.md)
- \#pragma once statements, [Solution](Chapter_08_Organizing_Files_in_Modular_Programs.md)

### A

- abstract data types, [Data Lifetime and Ownership](Chapter_05_Data_Lifetime_and_Ownership.md)
- abstract pointers, [Solution](Chapter_06_Flexible_APIs.md)
- Abstraction Layer pattern, [Context](Chapter_09_Escaping_ifdef_Hell.md)-[Applied to Running Example](Chapter_09_Escaping_ifdef_Hell.md), [Cross-Platform Files](Chapter_10_Implementing_Logging_Functionality.md)
- Aggregate Instance pattern, [Context](Chapter_04_Returning_Data_from_C_Functions.md)-[Applied to Running Example](Chapter_04_Returning_Data_from_C_Functions.md)
- aggregation, versus association, [Solution](Chapter_05_Data_Lifetime_and_Ownership.md)
- Allocation Wrapper pattern, [Context](Chapter_03_Memory_Management.md)-[Applied to Running Example](Chapter_03_Memory_Management.md)
- API Copy pattern, [Context](Chapter_08_Organizing_Files_in_Modular_Programs.md)-[Applied to Running Example](Chapter_08_Organizing_Files_in_Modular_Programs.md)
- APIs, flexible
  - challenges of designing, [Flexible APIs](Chapter_06_Flexible_APIs.md)
  - Dynamic Interface pattern, [Context](Chapter_06_Flexible_APIs.md)-[Applied to Running Example](Chapter_06_Flexible_APIs.md), [Multiple Logging Destinations](Chapter_10_Implementing_Logging_Functionality.md)
  - Function Control pattern, [Context](Chapter_06_Flexible_APIs.md)-[Applied to Running Example](Chapter_06_Flexible_APIs.md)
  - further reading on, [Further Reading](Chapter_06_Flexible_APIs.md)
  - Handle pattern, [Context](Chapter_06_Flexible_APIs.md), [Iterating](Chapter_11_Building_a_User_Management_System.md)
  - Header Files pattern, [Context](Chapter_06_Flexible_APIs.md)-[Applied to Running Example](Chapter_06_Flexible_APIs.md), [File Organization](Chapter_10_Implementing_Logging_Functionality.md), [File Organization](Chapter_11_Building_a_User_Management_System.md)
  - interface compatibility, [Solution](Chapter_08_Organizing_Files_in_Modular_Programs.md)
  - overview of patterns for, [Overview of the Patterns](Preface.md), [Flexible APIs](Chapter_06_Flexible_APIs.md), [Summary](Chapter_06_Flexible_APIs.md)
- application binary interface (ABI), [Solution](Chapter_08_Organizing_Files_in_Modular_Programs.md)
- arrays, variable length, [Solution](Chapter_03_Memory_Management.md)
- assert statements, [Solution](Chapter_01_Error_Handling.md)
- association, versus aggregation, [Solution](Chapter_05_Data_Lifetime_and_Ownership.md)
- Atomic Primitives pattern, [Context](Chapter_09_Escaping_ifdef_Hell.md)-[Applied to Running Example](Chapter_09_Escaping_ifdef_Hell.md), [Cross-Platform Files](Chapter_10_Implementing_Logging_Functionality.md)
- authentication
  - error handling, [Authentication: Error Handling](Chapter_11_Building_a_User_Management_System.md)
  - error logging, [Authentication: Error Logging](Chapter_11_Building_a_User_Management_System.md)
- automatic variables, [Solution](Chapter_03_Memory_Management.md)
- Avoid Variants pattern, [Context](Chapter_09_Escaping_ifdef_Hell.md)-[Applied to Running Example](Chapter_09_Escaping_ifdef_Hell.md), [Cross-Platform Files](Chapter_10_Implementing_Logging_Functionality.md), [Authentication: Error Logging](Chapter_11_Building_a_User_Management_System.md)

### B

- buffers, [Solution](Chapter_04_Returning_Data_from_C_Functions.md)
- build settings, [Solution](Chapter_08_Organizing_Files_in_Modular_Programs.md)
- by-reference arguments, [Solution](Chapter_04_Returning_Data_from_C_Functions.md)

### C

- C functions, returning data from (see also functions)
  - Aggregate Instance pattern, [Context](Chapter_04_Returning_Data_from_C_Functions.md)-[Applied to Running Example](Chapter_04_Returning_Data_from_C_Functions.md)
  - Callee Allocates pattern, [Context](Chapter_04_Returning_Data_from_C_Functions.md)-[Applied to Running Example](Chapter_04_Returning_Data_from_C_Functions.md), [Iterating](Chapter_11_Building_a_User_Management_System.md)
  - Caller-Owned Buffer pattern, [Context](Chapter_04_Returning_Data_from_C_Functions.md)-[Applied to Running Example](Chapter_04_Returning_Data_from_C_Functions.md), [Central Logging Function](Chapter_10_Implementing_Logging_Functionality.md)
  - challenges of, [Returning Data from C Functions](Chapter_04_Returning_Data_from_C_Functions.md)
  - Immutable Instance pattern, [Context](Chapter_04_Returning_Data_from_C_Functions.md)-[Applied to Running Example](Chapter_04_Returning_Data_from_C_Functions.md)
  - Out-Parameters pattern, [Context](Chapter_04_Returning_Data_from_C_Functions.md)-[Applied to Running Example](Chapter_04_Returning_Data_from_C_Functions.md)
  - overview of patterns for, [Overview of the Patterns](Preface.md), [Returning Data from C Functions](Chapter_04_Returning_Data_from_C_Functions.md), [Summary](Chapter_04_Returning_Data_from_C_Functions.md)
  - Return Value pattern, [Context](Chapter_04_Returning_Data_from_C_Functions.md)-[Applied to Running Example](Chapter_04_Returning_Data_from_C_Functions.md), [Logging Source Filter](Chapter_10_Implementing_Logging_Functionality.md), [Authentication: Error Handling](Chapter_11_Building_a_User_Management_System.md)
  - running example, [Running Example](Chapter_04_Returning_Data_from_C_Functions.md)
- C programming language
  - challenges of, [Why I Wrote This Book](Preface.md)-[Why I Wrote This Book](Preface.md)
- Callback Iterator pattern, [Context](Chapter_07_Flexible_Iterator_Interfaces.md)-[Applied to Running Example](Chapter_07_Flexible_Iterator_Interfaces.md)
- Callee Allocates pattern, [Context](Chapter_04_Returning_Data_from_C_Functions.md)-[Applied to Running Example](Chapter_04_Returning_Data_from_C_Functions.md), [Iterating](Chapter_11_Building_a_User_Management_System.md)
- Caller-Owned Buffer pattern, [Context](Chapter_04_Returning_Data_from_C_Functions.md)-[Applied to Running Example](Chapter_04_Returning_Data_from_C_Functions.md), [Central Logging Function](Chapter_10_Implementing_Logging_Functionality.md)
- Caller-Owned Instance pattern, [Context](Chapter_05_Data_Lifetime_and_Ownership.md)-[Applied to Running Example](Chapter_05_Data_Lifetime_and_Ownership.md), [Iterating](Chapter_11_Building_a_User_Management_System.md)
- central logging function, [Central Logging Function](Chapter_10_Implementing_Logging_Functionality.md)
- Cleanup Record pattern, [Context](Chapter_01_Error_Handling.md)-[Applied to Running Example](Chapter_01_Error_Handling.md)
- code examples
  - obtaining and using, [Using Code Examples](Preface.md)
  - references to examples presented in patterns, [Using Code Examples](Preface.md)
- code smells, [Problem](Chapter_01_Error_Handling.md)
- code variants, [Solution](Chapter_09_Escaping_ifdef_Hell.md)
- components, [Solution](Chapter_08_Organizing_Files_in_Modular_Programs.md) (see also Self-Contained Component pattern)
- cross-platform files, [Cross-Platform Files](Chapter_10_Implementing_Logging_Functionality.md)
- Cursor Iterator pattern, [Context](Chapter_07_Flexible_Iterator_Interfaces.md)-[Applied to Running Example](Chapter_07_Flexible_Iterator_Interfaces.md), [Iterating](Chapter_11_Building_a_User_Management_System.md)

### D

- data lifetime and ownership
  - Caller-Owned Instance pattern, [Context](Chapter_05_Data_Lifetime_and_Ownership.md)-[Applied to Running Example](Chapter_05_Data_Lifetime_and_Ownership.md), [Iterating](Chapter_11_Building_a_User_Management_System.md)
  - further reading on, [Further Reading](Chapter_05_Data_Lifetime_and_Ownership.md)
  - overview of patterns for, [Overview of the Patterns](Preface.md), [Data Lifetime and Ownership](Chapter_05_Data_Lifetime_and_Ownership.md), [Summary](Chapter_05_Data_Lifetime_and_Ownership.md)
  - running example, [Data Lifetime and Ownership](Chapter_05_Data_Lifetime_and_Ownership.md)
  - Shared Instance pattern, [Context](Chapter_05_Data_Lifetime_and_Ownership.md)-[Applied to Running Example](Chapter_05_Data_Lifetime_and_Ownership.md)
  - Software-Module with Global State pattern, [Context](Chapter_05_Data_Lifetime_and_Ownership.md)-[Applied to Running Example](Chapter_05_Data_Lifetime_and_Ownership.md), [Logging Source Filter](Chapter_10_Implementing_Logging_Functionality.md), [Data Organization](Chapter_11_Building_a_User_Management_System.md)
  - Stateless Software-Module pattern, [Context](Chapter_05_Data_Lifetime_and_Ownership.md)-[Applied to Running Example](Chapter_05_Data_Lifetime_and_Ownership.md)
  - structuring programs with object-like elements, [Data Lifetime and Ownership](Chapter_05_Data_Lifetime_and_Ownership.md)
- data storage
  - Dedicated Ownership pattern, application of, [Applied to Running Example](Chapter_03_Memory_Management.md)
  - defining and documenting clean up, [Context](Chapter_03_Memory_Management.md)
  - dynamic memory, [Context](Chapter_03_Memory_Management.md)
  - maintaining data for longer periods, [Context](Chapter_03_Memory_Management.md)
  - problems with dynamic memory, [Data Storage and Problems with Dynamic Memory](Chapter_03_Memory_Management.md)-[Data Storage and Problems with Dynamic Memory](Chapter_03_Memory_Management.md), [Problem](Chapter_03_Memory_Management.md)
  - providing large pieces of immutable data, [Context](Chapter_04_Returning_Data_from_C_Functions.md)
  - reacting automatically to error situations, [Context](Chapter_03_Memory_Management.md)
  - selecting patterns for, [Data Organization](Chapter_11_Building_a_User_Management_System.md)
  - sharing data, [Problem](Chapter_04_Returning_Data_from_C_Functions.md), [Context](Chapter_04_Returning_Data_from_C_Functions.md), [Context](Chapter_04_Returning_Data_from_C_Functions.md)
  - stack first approach, [Context](Chapter_03_Memory_Management.md), [Authentication: Error Logging](Chapter_11_Building_a_User_Management_System.md)
  - static memory, [Solution](Chapter_03_Memory_Management.md)
- data, abstract types of, [Data Lifetime and Ownership](Chapter_05_Data_Lifetime_and_Ownership.md)
- debugging (see also error handling; error information, returning)
  - Dedicated Ownership and, [Consequences](Chapter_03_Memory_Management.md)
  - detecting memory leaks, [Consequences](Chapter_03_Memory_Management.md)
  - eliminating memory errors, [Consequences](Chapter_03_Memory_Management.md)
  - Lazy Cleanup pattern and, [Problem](Chapter_03_Memory_Management.md)
  - logging debug information, [Solution](Chapter_03_Memory_Management.md)
  - NULL pointers and, [Solution](Chapter_03_Memory_Management.md)
  - problems with dynamic memory, [Data Storage and Problems with Dynamic Memory](Chapter_03_Memory_Management.md)
  - remote debugging, [The Pattern Story](Chapter_10_Implementing_Logging_Functionality.md)
  - returning error information, [Context](Chapter_02_Returning_Error_Information.md)
  - valgrind debugging tool, [Solution](Chapter_03_Memory_Management.md)
- Dedicated Ownership pattern, [Context](Chapter_03_Memory_Management.md)-[Applied to Running Example](Chapter_03_Memory_Management.md), [Iterating](Chapter_11_Building_a_User_Management_System.md)
- dependency inversion principle, [Flexible APIs](Chapter_06_Flexible_APIs.md)
- design patterns (see also individual patterns)
  - approach to learning, [How to Read This Book](Preface.md)
  - benefits of, [Summary](Chapter_10_Implementing_Logging_Functionality.md), [Closing Remarks](Chapter_12_Conclusion.md)
  - challenges of C programming language, [Preface](Preface.md)
  - definition of term, [Patterns Basics](Preface.md)
  - development of, [Patterns Basics](Preface.md)
  - overview of
    - data lifetime and ownership, [Overview of the Patterns](Preface.md)
    - error handling, [Overview of the Patterns](Preface.md), [Error Handling](Chapter_01_Error_Handling.md)
    - escaping \#ifdef hell, [Overview of the Patterns](Preface.md)
    - flexible APIs, [Overview of the Patterns](Preface.md)
    - iterator interfaces, [Overview of the Patterns](Preface.md)
    - memory management, [Overview of the Patterns](Preface.md)
    - organizing files in modular programs, [Overview of the Patterns](Preface.md)
    - returning data from C functions, [Overview of the Patterns](Preface.md)
    - returning error information, [Overview of the Patterns](Preface.md)
  - purpose of, [Preface](Preface.md)
  - references to examples presented in patterns, [Using Code Examples](Preface.md)
  - references to published papers, [Acknowledgments](Preface.md)
  - selecting, [Patterns Basics](Preface.md), [Implementing Logging Functionality](Chapter_10_Implementing_Logging_Functionality.md), [Data Organization](Chapter_11_Building_a_User_Management_System.md)
  - structure of, [Patterns Basics](Preface.md)
- directories, configuring, [Solution](Chapter_08_Organizing_Files_in_Modular_Programs.md) (see also Software-Module Directories pattern)
- Dynamic Interface pattern, [Context](Chapter_06_Flexible_APIs.md)-[Applied to Running Example](Chapter_06_Flexible_APIs.md), [Multiple Logging Destinations](Chapter_10_Implementing_Logging_Functionality.md)
- dynamic memory, [Data Storage and Problems with Dynamic Memory](Chapter_03_Memory_Management.md)-[Data Storage and Problems with Dynamic Memory](Chapter_03_Memory_Management.md), [Context](Chapter_03_Memory_Management.md), [Problem](Chapter_03_Memory_Management.md)

### E

- error handling
  - challenges of, [Error Handling](Chapter_01_Error_Handling.md)
  - Cleanup Record pattern, [Context](Chapter_01_Error_Handling.md)-[Applied to Running Example](Chapter_01_Error_Handling.md)
  - Function Split pattern, [Context](Chapter_01_Error_Handling.md)-[Applied to Running Example](Chapter_01_Error_Handling.md), [Adding Users: Error Handling](Chapter_11_Building_a_User_Management_System.md)
  - further reading on, [Further Reading](Chapter_01_Error_Handling.md)
  - Goto Error Handling pattern, [Context](Chapter_01_Error_Handling.md)-[Applied to Running Example](Chapter_01_Error_Handling.md)
  - Guard Clause pattern, [Context](Chapter_01_Error_Handling.md)-[Applied to Running Example](Chapter_01_Error_Handling.md), [Adding Users: Error Handling](Chapter_11_Building_a_User_Management_System.md)
  - Object-Based Error Handling pattern, [Context](Chapter_01_Error_Handling.md)-[Applied to Running Example](Chapter_01_Error_Handling.md), [Iterating](Chapter_11_Building_a_User_Management_System.md)
  - overview of patterns for, [Overview of the Patterns](Preface.md), [Error Handling](Chapter_01_Error_Handling.md), [Summary](Chapter_01_Error_Handling.md)
  - running example, [Running Example](Chapter_01_Error_Handling.md)
  - Samurai Principle pattern, [Context](Chapter_01_Error_Handling.md)-[Applied to Running Example](Chapter_01_Error_Handling.md), [Central Logging Function](Chapter_10_Implementing_Logging_Functionality.md), [Authentication: Error Handling](Chapter_11_Building_a_User_Management_System.md)
- error information, returning
  - challenges of, [Returning Error Information](Chapter_02_Returning_Error_Information.md)
  - further reading on, [Further Reading](Chapter_02_Returning_Error_Information.md)
  - Log Errors pattern, [Context](Chapter_02_Returning_Error_Information.md)-[Applied to Running Example](Chapter_02_Returning_Error_Information.md), [Authentication: Error Logging](Chapter_11_Building_a_User_Management_System.md)
  - overview of patterns for, [Overview of the Patterns](Preface.md), [Returning Error Information](Chapter_02_Returning_Error_Information.md), [Summary](Chapter_02_Returning_Error_Information.md)
  - Return Relevant Errors pattern, [Context](Chapter_02_Returning_Error_Information.md)-[Applied to Running Example](Chapter_02_Returning_Error_Information.md), [Logging Source Filter](Chapter_10_Implementing_Logging_Functionality.md), [Authentication: Error Handling](Chapter_11_Building_a_User_Management_System.md)
  - Return Status Codes pattern, [Context](Chapter_02_Returning_Error_Information.md)-[Applied to Running Example](Chapter_02_Returning_Error_Information.md), [Adding Users: Error Handling](Chapter_11_Building_a_User_Management_System.md)
  - running example, [Running Example](Chapter_02_Returning_Error_Information.md)
  - Special Return Values pattern, [Context](Chapter_02_Returning_Error_Information.md)-[Applied to Running Example](Chapter_02_Returning_Error_Information.md), [Iterating](Chapter_11_Building_a_User_Management_System.md)
  - unnoticed errors, [Problem](Chapter_01_Error_Handling.md)
- escaping \#ifdef hell (see \#ifdef statements)
- Eternal Memory pattern, [Context](Chapter_03_Memory_Management.md)-[Applied to Running Example](Chapter_03_Memory_Management.md), [Logging Source Filter](Chapter_10_Implementing_Logging_Functionality.md), [File Logging](Chapter_10_Implementing_Logging_Functionality.md), [Data Organization](Chapter_11_Building_a_User_Management_System.md)

### F

- files, organizing in modular programs
  - API Copy pattern, [Context](Chapter_08_Organizing_Files_in_Modular_Programs.md)-[Applied to Running Example](Chapter_08_Organizing_Files_in_Modular_Programs.md)
  - challenges of, [Organizing Files in Modular Programs](Chapter_08_Organizing_Files_in_Modular_Programs.md)
  - Global Include Directory pattern, [Context](Chapter_08_Organizing_Files_in_Modular_Programs.md)-[Applied to Running Example](Chapter_08_Organizing_Files_in_Modular_Programs.md), [File Organization](Chapter_10_Implementing_Logging_Functionality.md)
  - Include Guard pattern, [Context](Chapter_08_Organizing_Files_in_Modular_Programs.md)-[Applied to Running Example](Chapter_08_Organizing_Files_in_Modular_Programs.md), [Central Logging Function](Chapter_10_Implementing_Logging_Functionality.md), [File Organization](Chapter_11_Building_a_User_Management_System.md)
  - overview of patterns for, [Overview of the Patterns](Preface.md), [Organizing Files in Modular Programs](Chapter_08_Organizing_Files_in_Modular_Programs.md), [Summary](Chapter_08_Organizing_Files_in_Modular_Programs.md)
  - running example, [Running Example](Chapter_08_Organizing_Files_in_Modular_Programs.md)
  - Self-Contained Component pattern, [Context](Chapter_08_Organizing_Files_in_Modular_Programs.md)-[Applied to Running Example](Chapter_08_Organizing_Files_in_Modular_Programs.md)
  - Software-Module Directories pattern, [Context](Chapter_08_Organizing_Files_in_Modular_Programs.md)-[Applied to Running Example](Chapter_08_Organizing_Files_in_Modular_Programs.md), [File Organization](Chapter_10_Implementing_Logging_Functionality.md), [File Organization](Chapter_11_Building_a_User_Management_System.md)
  - Stateless Software-Module pattern, [Central Logging Function](Chapter_10_Implementing_Logging_Functionality.md)
- fragmented memory, [Data Storage and Problems with Dynamic Memory](Chapter_03_Memory_Management.md)
- freed memory, [Data Storage and Problems with Dynamic Memory](Chapter_03_Memory_Management.md)
- Function Control pattern, [Context](Chapter_06_Flexible_APIs.md)-[Applied to Running Example](Chapter_06_Flexible_APIs.md)
- Function Split pattern, [Context](Chapter_01_Error_Handling.md)-[Applied to Running Example](Chapter_01_Error_Handling.md), [Adding Users: Error Handling](Chapter_11_Building_a_User_Management_System.md)
- functions (see also C functions, returning data from)
  - aborting programs in error conditions, [Solution](Chapter_01_Error_Handling.md)
  - cleaning up multiple resources with, [Context](Chapter_01_Error_Handling.md), [Context](Chapter_01_Error_Handling.md), [Context](Chapter_01_Error_Handling.md)
  - global instances and, [Solution](Chapter_05_Data_Lifetime_and_Ownership.md)
  - handling one kind of variant only, [Solution](Chapter_09_Escaping_ifdef_Hell.md)
  - hiding internal, [Solution](Chapter_06_Flexible_APIs.md)
  - improving readability, [Problem](Chapter_01_Error_Handling.md)
  - iterating over elements, [Solution](Chapter_07_Flexible_Iterator_Interfaces.md)
  - maintaining detailed error information, [Context](Chapter_02_Returning_Error_Information.md)
  - passing instances to, [Solution](Chapter_05_Data_Lifetime_and_Ownership.md)
  - passing meta-information about, [Solution](Chapter_06_Flexible_APIs.md)
  - placing only platform-independent in header files, [Solution](Chapter_09_Escaping_ifdef_Hell.md)
  - providing access to multiple threads, [Problem](Chapter_05_Data_Lifetime_and_Ownership.md)
  - retrieving one element at a time, [Solution](Chapter_07_Flexible_Iterator_Interfaces.md)
  - returning multiple pieces of information, [Context](Chapter_04_Returning_Data_from_C_Functions.md), [Context](Chapter_04_Returning_Data_from_C_Functions.md)
  - returning relevant errors only, [Context](Chapter_02_Returning_Error_Information.md)
  - returning status information, [Solution](Chapter_02_Returning_Error_Information.md)
  - separating initialization and cleanup, [Solution](Chapter_01_Error_Handling.md)
  - sharing state information or resources, [Problem](Chapter_06_Flexible_APIs.md)
  - splitting into separate, [Context](Chapter_04_Returning_Data_from_C_Functions.md)
  - splitting responsibilities, [Solution](Chapter_01_Error_Handling.md)
  - using standardized, [Solution](Chapter_09_Escaping_ifdef_Hell.md)

### G

- garbage collection
  - dealing with lack of, [Data Lifetime and Ownership](Chapter_05_Data_Lifetime_and_Ownership.md)
  - memory leaks and, [Known Uses](Chapter_03_Memory_Management.md)
- Global Include Directory pattern, [Context](Chapter_08_Organizing_Files_in_Modular_Programs.md)-[Applied to Running Example](Chapter_08_Organizing_Files_in_Modular_Programs.md), [File Organization](Chapter_10_Implementing_Logging_Functionality.md)
- global variables, [Problem](Chapter_04_Returning_Data_from_C_Functions.md), [Problem](Chapter_04_Returning_Data_from_C_Functions.md), [Problem](Chapter_04_Returning_Data_from_C_Functions.md), [Solution](Chapter_05_Data_Lifetime_and_Ownership.md)
- Goto Error Handling pattern, [Context](Chapter_01_Error_Handling.md)-[Applied to Running Example](Chapter_01_Error_Handling.md)
- Guard Clause pattern, [Context](Chapter_01_Error_Handling.md)-[Applied to Running Example](Chapter_01_Error_Handling.md), [Adding Users: Error Handling](Chapter_11_Building_a_User_Management_System.md)

### H

- Handle pattern, [Context](Chapter_06_Flexible_APIs.md)-[Applied to Running Example](Chapter_06_Flexible_APIs.md), [Iterating](Chapter_11_Building_a_User_Management_System.md)
- header files (see also files, organizing in modular programs)
  - avoiding dependencies, [Solution](Chapter_08_Organizing_Files_in_Modular_Programs.md)
  - placing in subdirectories, [Solution](Chapter_08_Organizing_Files_in_Modular_Programs.md)
  - placing only platform-independent functions in, [Solution](Chapter_09_Escaping_ifdef_Hell.md)
  - placing with implementation files, [Solution](Chapter_08_Organizing_Files_in_Modular_Programs.md)
  - protecting against multiple inclusion, [Context](Chapter_08_Organizing_Files_in_Modular_Programs.md)
- Header Files pattern, [Context](Chapter_06_Flexible_APIs.md)-[Applied to Running Example](Chapter_06_Flexible_APIs.md), [File Organization](Chapter_10_Implementing_Logging_Functionality.md), [File Organization](Chapter_11_Building_a_User_Management_System.md)
- heap memory, [Data Storage and Problems with Dynamic Memory](Chapter_03_Memory_Management.md)

### I

- if statements, [Solution](Chapter_01_Error_Handling.md), [Problem](Chapter_01_Error_Handling.md)
- Immutable Instance pattern, [Context](Chapter_04_Returning_Data_from_C_Functions.md)-[Applied to Running Example](Chapter_04_Returning_Data_from_C_Functions.md)
- implementation details, hiding, [Problem](Chapter_06_Flexible_APIs.md)
- Include Guard pattern, [Context](Chapter_08_Organizing_Files_in_Modular_Programs.md)-[Applied to Running Example](Chapter_08_Organizing_Files_in_Modular_Programs.md), [Central Logging Function](Chapter_10_Implementing_Logging_Functionality.md), [File Organization](Chapter_11_Building_a_User_Management_System.md)
- Index Access pattern, [Context](Chapter_07_Flexible_Iterator_Interfaces.md)-[Applied to Running Example](Chapter_07_Flexible_Iterator_Interfaces.md), [Conditional Logging](Chapter_10_Implementing_Logging_Functionality.md)
- instances
  - definition of term, [Data Lifetime and Ownership](Chapter_05_Data_Lifetime_and_Ownership.md)
  - sharing, [Context](Chapter_05_Data_Lifetime_and_Ownership.md)
  - software-modules and, [Data Lifetime and Ownership](Chapter_05_Data_Lifetime_and_Ownership.md)
- interface compatibility, [Solution](Chapter_08_Organizing_Files_in_Modular_Programs.md) (see also APIs, flexible; Dynamic Interface pattern; iterator interfaces)
- interface segregation principle, [Flexible APIs](Chapter_06_Flexible_APIs.md)
- Isolated Primitives pattern, [Context](Chapter_09_Escaping_ifdef_Hell.md)-[Applied to Running Example](Chapter_09_Escaping_ifdef_Hell.md), [Cross-Platform Files](Chapter_10_Implementing_Logging_Functionality.md)
- iterator interfaces
  - Callback Iterator pattern, [Context](Chapter_07_Flexible_Iterator_Interfaces.md)-[Applied to Running Example](Chapter_07_Flexible_Iterator_Interfaces.md)
  - Cursor Iterator pattern, [Context](Chapter_07_Flexible_Iterator_Interfaces.md)-[Applied to Running Example](Chapter_07_Flexible_Iterator_Interfaces.md), [Iterating](Chapter_11_Building_a_User_Management_System.md)
  - designing flexible, [Flexible Iterator Interfaces](Chapter_07_Flexible_Iterator_Interfaces.md)
  - further reading on, [Further Reading](Chapter_07_Flexible_Iterator_Interfaces.md)
  - Index Access pattern, [Context](Chapter_07_Flexible_Iterator_Interfaces.md)-[Applied to Running Example](Chapter_07_Flexible_Iterator_Interfaces.md), [Conditional Logging](Chapter_10_Implementing_Logging_Functionality.md)
  - overview of patterns for, [Overview of the Patterns](Preface.md), [Flexible Iterator Interfaces](Chapter_07_Flexible_Iterator_Interfaces.md), [Summary](Chapter_07_Flexible_Iterator_Interfaces.md)
  - running example, [Running Example](Chapter_07_Flexible_Iterator_Interfaces.md)

### L

- Lazy Acquisition pattern, [File Logging](Chapter_10_Implementing_Logging_Functionality.md)
- Lazy Cleanup pattern, [Context](Chapter_03_Memory_Management.md)-[Applied to Running Example](Chapter_03_Memory_Management.md)
- lazy evaluation, [Solution](Chapter_01_Error_Handling.md)
- Linux overcommit, [Applied to Running Example](Chapter_03_Memory_Management.md)
- Liskow substitution principle, [Flexible APIs](Chapter_06_Flexible_APIs.md)
- Log Errors pattern, [Context](Chapter_02_Returning_Error_Information.md)-[Applied to Running Example](Chapter_02_Returning_Error_Information.md), [Authentication: Error Logging](Chapter_11_Building_a_User_Management_System.md)
  - implementation example
    - central logging function, [Central Logging Function](Chapter_10_Implementing_Logging_Functionality.md)
    - conditional logging, [Conditional Logging](Chapter_10_Implementing_Logging_Functionality.md)
    - context, [The Pattern Story](Chapter_10_Implementing_Logging_Functionality.md)
    - cross-platform files, [Cross-Platform Files](Chapter_10_Implementing_Logging_Functionality.md)
    - file logging, [File Logging](Chapter_10_Implementing_Logging_Functionality.md)
    - file organization, [File Organization](Chapter_10_Implementing_Logging_Functionality.md)
    - logging source filter, [Logging Source Filter](Chapter_10_Implementing_Logging_Functionality.md)
    - multiple logging destinations, [Multiple Logging Destinations](Chapter_10_Implementing_Logging_Functionality.md)
    - overview of patterns used, [Summary](Chapter_10_Implementing_Logging_Functionality.md)
    - using the logger, [Using the Logger](Chapter_10_Implementing_Logging_Functionality.md)

### M

- macros, multiline, [Solution](Chapter_02_Returning_Error_Information.md)
- Makefiles, [Solution](Chapter_08_Organizing_Files_in_Modular_Programs.md)
- memory fragmentation, [Problem](Chapter_03_Memory_Management.md)
- memory leaks
  - deliberately creating, [Solution](Chapter_03_Memory_Management.md)
  - detecting, [Consequences](Chapter_03_Memory_Management.md)
  - eliminating risk of, [Consequences](Chapter_03_Memory_Management.md)
  - garbage collection and, [Known Uses](Chapter_03_Memory_Management.md)
- memory management
  - Allocation Wrapper pattern, [Context](Chapter_03_Memory_Management.md)-[Applied to Running Example](Chapter_03_Memory_Management.md)
  - challenges of, [Memory Management](Chapter_03_Memory_Management.md)
  - data storage and dynamic memory, [Data Storage and Problems with Dynamic Memory](Chapter_03_Memory_Management.md)-[Data Storage and Problems with Dynamic Memory](Chapter_03_Memory_Management.md)
  - Dedicated Ownership pattern, [Context](Chapter_03_Memory_Management.md)-[Applied to Running Example](Chapter_03_Memory_Management.md), [Iterating](Chapter_11_Building_a_User_Management_System.md)
  - Eternal Memory pattern, [Context](Chapter_03_Memory_Management.md)-[Applied to Running Example](Chapter_03_Memory_Management.md), [Logging Source Filter](Chapter_10_Implementing_Logging_Functionality.md), [File Logging](Chapter_10_Implementing_Logging_Functionality.md), [Data Organization](Chapter_11_Building_a_User_Management_System.md)
  - further reading on, [Further Reading](Chapter_03_Memory_Management.md)
  - Lazy Cleanup pattern, [Context](Chapter_03_Memory_Management.md)-[Applied to Running Example](Chapter_03_Memory_Management.md)
  - Memory Pool pattern, [Context](Chapter_03_Memory_Management.md)-[Applied to Running Example](Chapter_03_Memory_Management.md)
  - overview of patterns for, [Overview of the Patterns](Preface.md), [Memory Management](Chapter_03_Memory_Management.md), [Summary](Chapter_03_Memory_Management.md)
  - Pointer Check pattern, [Context](Chapter_03_Memory_Management.md)-[Applied to Running Example](Chapter_03_Memory_Management.md)
  - running example, [Running Example](Chapter_03_Memory_Management.md)
  - Stack First pattern, [Context](Chapter_03_Memory_Management.md)-[Applied to Running Example](Chapter_03_Memory_Management.md), [Authentication: Error Logging](Chapter_11_Building_a_User_Management_System.md)
- Memory Pool pattern, [Context](Chapter_03_Memory_Management.md)-[Applied to Running Example](Chapter_03_Memory_Management.md)
- modular programs
  - organizing files in
    - overview of patterns for, [Overview of the Patterns](Preface.md)
- modular programs, ease of maintaining, [Context](Chapter_06_Flexible_APIs.md) (see also files, organizing in modular programs)
- multiline macros, [Solution](Chapter_02_Returning_Error_Information.md)
- multithreaded environments, [Solution](Chapter_04_Returning_Data_from_C_Functions.md), [Problem](Chapter_05_Data_Lifetime_and_Ownership.md), [Problem](Chapter_07_Flexible_Iterator_Interfaces.md)

### O

- Object-Based Error Handling pattern, [Context](Chapter_01_Error_Handling.md)-[Applied to Running Example](Chapter_01_Error_Handling.md), [Iterating](Chapter_11_Building_a_User_Management_System.md)
- object-like elements, [Data Lifetime and Ownership](Chapter_05_Data_Lifetime_and_Ownership.md)
- open-closed principle, [Flexible APIs](Chapter_06_Flexible_APIs.md)
- organizing files (see files, organizing in modular programs)
- Out-Parameters pattern, [Context](Chapter_04_Returning_Data_from_C_Functions.md)-[Applied to Running Example](Chapter_04_Returning_Data_from_C_Functions.md)
- overcommit principle, [Applied to Running Example](Chapter_03_Memory_Management.md)

### P

- packages, [Organizing Files in Modular Programs](Chapter_08_Organizing_Files_in_Modular_Programs.md)
- passwords, [Data Organization](Chapter_11_Building_a_User_Management_System.md)
- patterns (see design patterns)
- Pointer Check pattern, [Context](Chapter_03_Memory_Management.md)-[Applied to Running Example](Chapter_03_Memory_Management.md)
- pre-condition checks, [Problem](Chapter_01_Error_Handling.md)

### R

- resources
  - acquiring and cleaning up multiple, [Context](Chapter_01_Error_Handling.md), [Context](Chapter_01_Error_Handling.md), [Context](Chapter_01_Error_Handling.md)
  - lifetime and ownership of, [Data Lifetime and Ownership](Chapter_05_Data_Lifetime_and_Ownership.md)
  - sharing, [Problem](Chapter_06_Flexible_APIs.md)
- Return Relevant Errors pattern, [Context](Chapter_02_Returning_Error_Information.md)-[Applied to Running Example](Chapter_02_Returning_Error_Information.md), [Logging Source Filter](Chapter_10_Implementing_Logging_Functionality.md), [Authentication: Error Handling](Chapter_11_Building_a_User_Management_System.md)
- Return Status Codes pattern, [Context](Chapter_02_Returning_Error_Information.md)-[Applied to Running Example](Chapter_02_Returning_Error_Information.md), [Adding Users: Error Handling](Chapter_11_Building_a_User_Management_System.md)
- Return Value pattern, [Context](Chapter_04_Returning_Data_from_C_Functions.md)-[Applied to Running Example](Chapter_04_Returning_Data_from_C_Functions.md), [Logging Source Filter](Chapter_10_Implementing_Logging_Functionality.md), [Authentication: Error Handling](Chapter_11_Building_a_User_Management_System.md)
- return values, special, [Solution](Chapter_02_Returning_Error_Information.md)
- returning data from C functions (see C functions, returning data from)
- returning error information (see error information, returning)

### S

- salted hash values, [Data Organization](Chapter_11_Building_a_User_Management_System.md)
- Samurai Principle pattern, [Context](Chapter_01_Error_Handling.md)-[Applied to Running Example](Chapter_01_Error_Handling.md), [Central Logging Function](Chapter_10_Implementing_Logging_Functionality.md), [Authentication: Error Handling](Chapter_11_Building_a_User_Management_System.md)
- Self-Contained Component pattern, [Context](Chapter_08_Organizing_Files_in_Modular_Programs.md)-[Applied to Running Example](Chapter_08_Organizing_Files_in_Modular_Programs.md)
- semantic versioning, [Consequences](Chapter_08_Organizing_Files_in_Modular_Programs.md)
- Shared Instance pattern, [Context](Chapter_05_Data_Lifetime_and_Ownership.md)-[Applied to Running Example](Chapter_05_Data_Lifetime_and_Ownership.md)
- single-responsibility principle, [Flexible APIs](Chapter_06_Flexible_APIs.md)
- Singleton pattern/anti-pattern, [Consequences](Chapter_05_Data_Lifetime_and_Ownership.md)
- smart pointers, [Data Storage and Problems with Dynamic Memory](Chapter_03_Memory_Management.md)
- Software-Module Directories pattern, [Context](Chapter_08_Organizing_Files_in_Modular_Programs.md)-[Applied to Running Example](Chapter_08_Organizing_Files_in_Modular_Programs.md), [File Organization](Chapter_10_Implementing_Logging_Functionality.md), [File Organization](Chapter_11_Building_a_User_Management_System.md)
- Software-Module with Global State pattern, [Context](Chapter_05_Data_Lifetime_and_Ownership.md)-[Applied to Running Example](Chapter_05_Data_Lifetime_and_Ownership.md), [Logging Source Filter](Chapter_10_Implementing_Logging_Functionality.md), [Data Organization](Chapter_11_Building_a_User_Management_System.md)
- software-modules, [Data Lifetime and Ownership](Chapter_05_Data_Lifetime_and_Ownership.md)
- SOLID principles, [Flexible APIs](Chapter_06_Flexible_APIs.md)
- Special Return Values pattern, [Context](Chapter_02_Returning_Error_Information.md)-[Applied to Running Example](Chapter_02_Returning_Error_Information.md), [Iterating](Chapter_11_Building_a_User_Management_System.md)
- Split Variant Implementations pattern, [Context](Chapter_09_Escaping_ifdef_Hell.md)-[Applied to Running Example](Chapter_09_Escaping_ifdef_Hell.md), [Cross-Platform Files](Chapter_10_Implementing_Logging_Functionality.md)
- splitting function responsibilities (see Function Split pattern)
- Stack First pattern, [Context](Chapter_03_Memory_Management.md)-[Applied to Running Example](Chapter_03_Memory_Management.md), [Authentication: Error Logging](Chapter_11_Building_a_User_Management_System.md)
- state information, sharing, [Problem](Chapter_06_Flexible_APIs.md)
- Stateless Software-Module pattern, [Context](Chapter_05_Data_Lifetime_and_Ownership.md)-[Applied to Running Example](Chapter_05_Data_Lifetime_and_Ownership.md), [Central Logging Function](Chapter_10_Implementing_Logging_Functionality.md)
- static memory, [Data Storage and Problems with Dynamic Memory](Chapter_03_Memory_Management.md), [Solution](Chapter_03_Memory_Management.md)
- status codes, returning (see Return Status Codes pattern)
- synchronization issues, [Solution](Chapter_04_Returning_Data_from_C_Functions.md)

### U

- user management system example
  - adding users, [Adding Users: Error Handling](Chapter_11_Building_a_User_Management_System.md)
  - authentication
    - error handling, [Authentication: Error Handling](Chapter_11_Building_a_User_Management_System.md)
    - error logging, [Authentication: Error Logging](Chapter_11_Building_a_User_Management_System.md)
  - context, [The Pattern Story](Chapter_11_Building_a_User_Management_System.md)
  - data organization, [Data Organization](Chapter_11_Building_a_User_Management_System.md)
  - file organization, [File Organization](Chapter_11_Building_a_User_Management_System.md)
  - iterating, [Iterating](Chapter_11_Building_a_User_Management_System.md)
  - overview of patterns used, [Summary](Chapter_11_Building_a_User_Management_System.md)
  - using the system, [Using the User Management System](Chapter_11_Building_a_User_Management_System.md)

### V

- valgrind, [Consequences](Chapter_03_Memory_Management.md), [Solution](Chapter_03_Memory_Management.md)
- variable length arrays, [Solution](Chapter_03_Memory_Management.md)
- variables, automatic, [Solution](Chapter_03_Memory_Management.md)
- version numbers, [Consequences](Chapter_08_Organizing_Files_in_Modular_Programs.md)

