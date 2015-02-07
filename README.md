# Dependency Injection

`di.py` (not to be confused with [dipy](http://nipy.org/dipy/)) is a general purpose dependency injection library for python.

## What is DI?

Simply put, Dependency Injection is a system for managing the *creation* and *distribution* of complex objects.  Let's look at each aspect independently.  

#### Object Creation

Image you have a database client object.  Creating this object in a mature system is actually a complex task: database uris must configurable for Dev vs Prod, the password must be stored securely, and there are several error conditions to handle.  Creating this object is relatively expensive computationally so you want to avoid recreating it.  At the same time, it involves a connection to the external world, so you need to expect it to break over the course of a long-running program.  `di.py` provides simple tools for implementing this type of functionality.

#### Object Distribution

Plumbing instances around a large program is both annoying and time consuming, which often encourage less-than-optimal design decisions.  If you have ever had to add an argument to a chain of function calls, you know the pain.  `di.py` allows objects to be injected into any function or class regardless of the path from the point of creation to the point of use.  This also makes it easy to distribute mock objects without having to write code with this in mind.

## How does DI work?

`di.js` provides two decorators: `provide` and `inject`.  `provide` can be used to decorate a class or function, thus defining the creation process of a **component**.  Any function or method that depends on a component, i.e. wants to recieve it as an argument, is decorated with `inject`.

